[CmdletBinding()]
param(
  [string] $Target = ".",
  [ValidateSet("minimal", "standard", "strict")]
  [string] $Profile = "standard",
  [string] $TaskBrief = "",
  [switch] $Force
)

$ErrorActionPreference = "Stop"
$scriptPath = Join-Path $PSScriptRoot "init_longrun.py"
$argsList = @($scriptPath, "--target", $Target, "--profile", $Profile, "--task-brief", $TaskBrief)
if ($Force) { $argsList += "--force" }
python @argsList
