# dev launcher: activates venv and runs the overlay
param([string]$Config = "config/default.yaml")
$ErrorActionPreference = "Stop"
if (Test-Path ".venv\Scripts\Activate.ps1") { . ".venv\Scripts\Activate.ps1" }
python -m arc_esp --config $Config