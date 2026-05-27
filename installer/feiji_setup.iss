; 肥鸡桌面宠物 Inno Setup 安装脚本

#define MyAppName "肥鸡桌面宠物"
#define MyAppVersion "1.0.0"
#define MyAppExeName "Feiji.exe"
#define MyAppIcon "..\assets\look-1.ico"
#define DistDir "..\dist\Feiji"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher=Feiji
DefaultDirName={autopf}\Feiji
DefaultGroupName={#MyAppName}
OutputDir=..\installer_output
OutputBaseFilename=FeijiSetup
SetupIconFile={#MyAppIcon}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=no
PrivilegesRequired=admin
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加任务:"
Name: "startmenuicon"; Description: "创建开始菜单快捷方式"; GroupDescription: "附加任务:"

[Files]
Source: "{#DistDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\look-1.ico"; Tasks: desktopicon
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\look-1.ico"; Tasks: startmenuicon
Name: "{group}\卸载 {#MyAppName}"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "立即运行肥鸡桌面宠物"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
