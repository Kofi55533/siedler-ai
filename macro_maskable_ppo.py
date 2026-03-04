# -*- coding: utf-8 -*-
"""
MaskablePPO-Erweiterung fuer Multi-Step-Umgebungen.

Optionaler Modus:
- Zaehlt nur abgeschlossene Aktionen als `num_timesteps`.
- Eine Aktion gilt als "abgeschlossen", wenn `info["multi_step"]` nicht true ist.

Wichtig:
- Die Policy/Buffer-Logik bleibt unveraendert (keine Aenderung am Loss).
- Es wird nur die Timestep-Zaehlung fuer Schedules/Logging angepasst.
"""

from typing import Any, Dict, Optional, Tuple

import numpy as np
import torch as th
from stable_baselines3.common.buffers import RolloutBuffer
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.type_aliases import MaybeCallback
from stable_baselines3.common.utils import obs_as_tensor
from stable_baselines3.common.vec_env import VecEnv
from sb3_contrib.common.maskable.buffers import MaskableDictRolloutBuffer, MaskableRolloutBuffer
from sb3_contrib.common.maskable.utils import get_action_masks, is_masking_supported
from sb3_contrib.ppo_mask.ppo_mask import MaskablePPO
from gymnasium import spaces


class CompletedActionMaskablePPO(MaskablePPO):
    """
    MaskablePPO mit optionaler Timestep-Zaehlung pro abgeschlossener Aktion.
    """

    def __init__(
        self,
        *args,
        count_completed_actions_only: bool = False,
        **kwargs,
    ):
        self.count_completed_actions_only = bool(count_completed_actions_only)
        self._last_rollout_micro_steps = 0
        self._last_rollout_completed_steps = 0
        super().__init__(*args, **kwargs)

    @staticmethod
    def _is_completed_action_info(info: Dict[str, Any]) -> bool:
        if not isinstance(info, dict):
            return True
        return not bool(info.get("multi_step", False))

    def collect_rollouts(  # type: ignore[override]
        self,
        env: VecEnv,
        callback: BaseCallback,
        rollout_buffer: RolloutBuffer,
        n_rollout_steps: int,
        use_masking: bool = True,
    ) -> bool:
        assert isinstance(
            rollout_buffer, (MaskableRolloutBuffer, MaskableDictRolloutBuffer)
        ), "RolloutBuffer doesn't support action masking"
        assert self._last_obs is not None, "No previous observation was provided"

        self.policy.set_training_mode(False)
        n_steps = 0
        action_masks = None
        rollout_buffer.reset()

        if use_masking and not is_masking_supported(env):
            raise ValueError("Environment does not support action masking. Consider using ActionMasker wrapper")

        callback.on_rollout_start()
        self._last_rollout_micro_steps = 0
        self._last_rollout_completed_steps = 0

        while n_steps < n_rollout_steps:
            with th.no_grad():
                obs_tensor = obs_as_tensor(self._last_obs, self.device)
                if use_masking:
                    action_masks = get_action_masks(env)
                actions, values, log_probs = self.policy(obs_tensor, action_masks=action_masks)

            actions = actions.cpu().numpy()
            new_obs, rewards, dones, infos = env.step(actions)

            micro_steps = int(env.num_envs)
            self._last_rollout_micro_steps += micro_steps

            if self.count_completed_actions_only:
                completed_steps = sum(
                    1 for info in infos if self._is_completed_action_info(info)
                )
                self.num_timesteps += int(completed_steps)
                self._last_rollout_completed_steps += int(completed_steps)
            else:
                self.num_timesteps += micro_steps
                self._last_rollout_completed_steps += micro_steps

            callback.update_locals(locals())
            if not callback.on_step():
                return False

            self._update_info_buffer(infos, dones)
            n_steps += 1

            if isinstance(self.action_space, spaces.Discrete):
                actions = actions.reshape(-1, 1)

            for idx, done in enumerate(dones):
                if (
                    done
                    and infos[idx].get("terminal_observation") is not None
                    and infos[idx].get("TimeLimit.truncated", False)
                ):
                    terminal_obs = self.policy.obs_to_tensor(infos[idx]["terminal_observation"])[0]
                    with th.no_grad():
                        terminal_value = self.policy.predict_values(terminal_obs)[0]
                    rewards[idx] += self.gamma * terminal_value

            rollout_buffer.add(
                self._last_obs,
                actions,
                rewards,
                self._last_episode_starts,
                values,
                log_probs,
                action_masks=action_masks,
            )
            self._last_obs = new_obs  # type: ignore[assignment]
            self._last_episode_starts = dones

        with th.no_grad():
            values = self.policy.predict_values(obs_as_tensor(new_obs, self.device))  # type: ignore[arg-type]

        rollout_buffer.compute_returns_and_advantage(last_values=values, dones=dones)

        # Zusatz-Logging fuer Transparenz.
        self.logger.record("rollout/micro_steps", float(self._last_rollout_micro_steps))
        self.logger.record("rollout/completed_steps", float(self._last_rollout_completed_steps))
        if self._last_rollout_micro_steps > 0:
            ratio = float(self._last_rollout_completed_steps) / float(self._last_rollout_micro_steps)
            self.logger.record("rollout/completed_step_ratio", ratio)

        callback.on_rollout_end()
        return True

