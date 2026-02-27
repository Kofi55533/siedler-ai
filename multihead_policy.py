import torch as th
import torch.nn as nn

from gymnasium import spaces
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor


class SpatialVectorExtractor(BaseFeaturesExtractor):
    """Combines vector observations with CNN features from spatial channels."""

    def __init__(
        self,
        observation_space: spaces.Dict,
        cnn_channels=(16, 32, 64),
        cnn_out_dim: int = 128,
        vector_out_dim: int = 256,
    ):
        if not isinstance(observation_space, spaces.Dict):
            raise ValueError("SpatialVectorExtractor expects a Dict observation space")
        super().__init__(observation_space, features_dim=1)

        spatial_space = observation_space.spaces["spatial"]
        vector_space = observation_space.spaces["vector"]

        n_channels, height, width = spatial_space.shape
        self.cnn = nn.Sequential(
            nn.Conv2d(n_channels, cnn_channels[0], kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(cnn_channels[0], cnn_channels[1], kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Conv2d(cnn_channels[1], cnn_channels[2], kernel_size=3, stride=2, padding=1),
            nn.ReLU(),
            nn.Flatten(),
        )

        with th.no_grad():
            n_flatten = self.cnn(th.zeros(1, n_channels, height, width)).shape[1]

        self.cnn_out = nn.Sequential(
            nn.Linear(n_flatten, cnn_out_dim),
            nn.ReLU(),
        )

        vector_dim = vector_space.shape[0]
        self.vector_out = nn.Sequential(
            nn.Linear(vector_dim, vector_out_dim),
            nn.ReLU(),
        )

        self._features_dim = cnn_out_dim + vector_out_dim

    def forward(self, obs):
        spatial = obs["spatial"]
        vector = obs["vector"]
        spatial_feat = self.cnn_out(self.cnn(spatial))
        vector_feat = self.vector_out(vector)
        return th.cat((vector_feat, spatial_feat), dim=1)


class MultiHeadMaskablePolicy(MaskableActorCriticPolicy):
    """Maskable policy with separate action heads per phase.

    Expects the phase one-hot to be appended at the end of the observation.
    """

    def __init__(
        self,
        *args,
        action_head_sizes=None,
        phase_dim=None,
        **kwargs,
    ):
        if action_head_sizes is None or phase_dim is None:
            raise ValueError("action_head_sizes and phase_dim must be provided")
        self.action_head_sizes = list(action_head_sizes)
        self.phase_dim = int(phase_dim)
        super().__init__(*args, **kwargs)

    def _build(self, lr_schedule) -> None:
        super()._build(lr_schedule)
        latent_dim = self.mlp_extractor.latent_dim_pi
        self.action_nets = nn.ModuleList(
            [nn.Linear(latent_dim, n) for n in self.action_head_sizes]
        )
        # Keep attribute for compatibility
        self.action_net = self.action_nets[0]

    def _extract_phase_index(self, obs: th.Tensor) -> th.Tensor:
        if isinstance(obs, dict):
            obs_vec = obs["vector"]
        else:
            obs_vec = obs
        phase_one_hot = obs_vec[:, -self.phase_dim :]
        return th.argmax(phase_one_hot, dim=1)

    def _build_logits(self, latent_pi: th.Tensor, phase_idx: th.Tensor) -> th.Tensor:
        batch_size = latent_pi.shape[0]
        device = latent_pi.device
        full = th.full((batch_size, self.action_space.n), -1e9, device=device)
        for head_idx, head in enumerate(self.action_nets):
            mask = phase_idx == head_idx
            if not th.any(mask):
                continue
            idxs = th.nonzero(mask, as_tuple=False).squeeze(1)
            head_logits = head(latent_pi[idxs])
            full[idxs, : head_logits.shape[1]] = head_logits
        return full

    def _get_dist_and_value(self, obs: th.Tensor):
        features = self.extract_features(obs)
        if self.share_features_extractor:
            latent_pi, latent_vf = self.mlp_extractor(features)
        else:
            pi_features, vf_features = features
            latent_pi = self.mlp_extractor.forward_actor(pi_features)
            latent_vf = self.mlp_extractor.forward_critic(vf_features)

        phase_idx = self._extract_phase_index(obs)
        logits = self._build_logits(latent_pi, phase_idx)
        dist = self.action_dist.proba_distribution(action_logits=logits)
        return dist, latent_vf

    def forward(self, obs: th.Tensor, deterministic: bool = False, action_masks=None):
        dist, latent_vf = self._get_dist_and_value(obs)
        if action_masks is not None:
            dist.apply_masking(action_masks)
        actions = dist.get_actions(deterministic=deterministic)
        log_prob = dist.log_prob(actions)
        values = self.value_net(latent_vf)
        actions = actions.reshape((-1, *self.action_space.shape))
        return actions, values, log_prob

    def get_distribution(self, obs: th.Tensor, action_masks=None):
        dist, _ = self._get_dist_and_value(obs)
        if action_masks is not None:
            dist.apply_masking(action_masks)
        return dist

    def evaluate_actions(self, obs: th.Tensor, actions: th.Tensor, action_masks=None):
        dist, latent_vf = self._get_dist_and_value(obs)
        if action_masks is not None:
            dist.apply_masking(action_masks)
        log_prob = dist.log_prob(actions)
        values = self.value_net(latent_vf)
        return values, log_prob, dist.entropy()
