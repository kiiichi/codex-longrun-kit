[CmdletBinding()]
param(
  [string] $Target = "."
)

$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "normalize_reviews.py"
python $scriptPath --target $Target
