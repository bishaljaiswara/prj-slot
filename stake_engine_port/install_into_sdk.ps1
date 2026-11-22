$ErrorActionPreference = "Stop"
$SdkRoot = Read-Host "Enter the full path to your cloned engineio/math-sdk folder"
if (-not (Test-Path (Join-Path $SdkRoot "src\config\config.py"))) {
  throw "That folder does not look like the Engine Math SDK root."
}
$Source = Join-Path $PSScriptRoot "games\twinkle_treats"
$Target = Join-Path $SdkRoot "games\twinkle_treats"
if (Test-Path $Target) { throw "Target already exists: $Target. Use a clean SDK checkout." }
Copy-Item -Recurse $Source $Target
Write-Host "Copied Twinkle Treats SDK overlay to $Target"
Write-Host "Next, from SDK root run: python games/twinkle_treats/run.py"
