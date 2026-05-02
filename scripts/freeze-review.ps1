[CmdletBinding()]
param(
  [string] $Target = ".",
  [string] $Base = "main",
  [switch] $Force
)

$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "freeze_review.py"
$argsList = @($scriptPath, "--target", $Target, "--base", $Base)
if ($Force) { $argsList += "--force" }
python @argsList
