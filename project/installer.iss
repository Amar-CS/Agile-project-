; Inno Setup script - builds LoaderStore-Setup.exe (run build-exe.bat first, then open this file in Inno Setup and press Compile)
[Setup]
AppName=Loader Store
AppVersion=1.0
DefaultDirName={autopf}\Loader Store
DefaultGroupName=Loader Store
OutputBaseFilename=LoaderStore-Setup
SetupIconFile=assets\loader-store.ico
UninstallDisplayIcon={app}\LoaderStore.exe
Compression=lzma
WizardStyle=modern
[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"
[Files]
Source: "dist\LoaderStore.exe"; DestDir: "{app}"
[Icons]
Name: "{group}\Loader Store"; Filename: "{app}\LoaderStore.exe"
Name: "{autodesktop}\Loader Store"; Filename: "{app}\LoaderStore.exe"; Tasks: desktopicon
[Run]
Filename: "{app}\LoaderStore.exe"; Description: "Launch Loader Store"; Flags: nowait postinstall skipifsilent
