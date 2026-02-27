param(
    [string]$OutputZip = "..\siedler_ai_colab_bundle.zip"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$outputPath = Resolve-Path (Join-Path $scriptDir ".") | ForEach-Object {
    Join-Path $_ $OutputZip
}

$tmpDir = Join-Path $env:TEMP ("siedler_colab_bundle_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $tmpDir | Out-Null

try {
    $required = @(
        "colab_training.py",
        "environment.py",
        "multihead_policy.py",
        "training_profiles.py",
        "map_config_wintersturm.py",
        "wood_zones_config.py",
        "production_system.py",
        "worker_simulation.py",
        "pathfinding.py",
        "player1_resources.json"
    )

    $walkableCandidates = @(
        "player1_walkable_515.npy",
        "player1_walkable.npy"
    )
    $walkable = $walkableCandidates | Where-Object {
        Test-Path (Join-Path $repoRoot $_)
    } | Select-Object -First 1

    if (-not $walkable) {
        throw "Missing walkable npy file (player1_walkable_515.npy or player1_walkable.npy)."
    }

    foreach ($rel in $required) {
        $src = Join-Path $repoRoot $rel
        if (-not (Test-Path $src)) {
            throw "Missing required file: $rel"
        }
        Copy-Item -Path $src -Destination (Join-Path $tmpDir $rel) -Force
    }

    Copy-Item -Path (Join-Path $repoRoot $walkable) -Destination (Join-Path $tmpDir $walkable) -Force

    $optionalTruth = Join-Path $repoRoot "config\worker_truth_model.json"
    if (Test-Path $optionalTruth) {
        New-Item -ItemType Directory -Path (Join-Path $tmpDir "config") -Force | Out-Null
        Copy-Item -Path $optionalTruth -Destination (Join-Path $tmpDir "config\worker_truth_model.json") -Force
    }

    if (Test-Path $outputPath) {
        Remove-Item -Path $outputPath -Force
    }

    Compress-Archive -Path (Join-Path $tmpDir "*") -DestinationPath $outputPath -CompressionLevel Optimal
    Write-Host "Created bundle: $outputPath"
}
finally {
    if (Test-Path $tmpDir) {
        Remove-Item -Path $tmpDir -Recurse -Force
    }
}

