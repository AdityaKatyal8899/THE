[Setup]
AppName=THE Language
AppVersion=0.1.0
DefaultDirName={pf}\THE
DefaultGroupName=THE
OutputDir=output
OutputBaseFilename=THE_Setup
Compression=lzma
SolidCompression=yes
SetupIconFile=the.ico
UninstallDisplayIcon={app}\the.exe
WizardStyle=modern

[Files]
Source: "dist\the.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\THE"; Filename: "{app}\the.exe"
Name: "{userdesktop}\THE"; Filename: "{app}\the.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create Desktop Icon"; Flags: unchecked

[Registry]
; Add THE to PATH
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; \
ValueData: "{olddata};{app}"; Flags: preservestringtype

[Run]
Filename: "{app}\the.exe"; Description: "Launch THE"; Flags: nowait postinstall skipifsilent