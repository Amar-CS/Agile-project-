# Creates "Loader Store" shortcuts (with the logo) on the Desktop and in the Start Menu.
$ErrorActionPreference = 'Stop'
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$py = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if (-not $py) {
  Write-Host 'Python is not installed. Install it from python.org (tick "Add Python to PATH"), then run install.bat again.'
  exit 1
}
$ws = New-Object -ComObject WScript.Shell
$places = @([Environment]::GetFolderPath('Desktop'), (Join-Path ([Environment]::GetFolderPath('StartMenu')) 'Programs'))
foreach ($p in $places) {
  $s = $ws.CreateShortcut((Join-Path $p 'Loader Store.lnk'))
  $s.TargetPath = $py
  $s.Arguments = '"' + (Join-Path $dir 'desktop.py') + '"'
  $s.WorkingDirectory = $dir
  $s.IconLocation = (Join-Path $dir 'assets\loader-store.ico')
  $s.Description = 'Loader Store Management System'
  $s.Save()
}
Write-Host 'Done. "Loader Store" now appears on your Desktop and in the Start Menu.'
