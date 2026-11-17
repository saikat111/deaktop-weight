@echo off
setlocal
title MythosHUD Installer
echo ========================================================
echo       MYTHOS HUD - INSTALLER & SHORTCUT SETUP
echo ========================================================
echo.

set "PYTHON_CMD=python"
if exist "%APPDATA%\uv\tools\windows-mcp\Scripts\python.exe" (
    set "PYTHON_CMD=%APPDATA%\uv\tools\windows-mcp\Scripts\python.exe"
) else (
    where py >nul 2>&1 && (
        py -3.12 --version >nul 2>&1 && set "PYTHON_CMD=py -3.12"
    )
)

echo [1/2] Checking environment and dependencies...
if not exist "%~dp0dist\MythosHUD\MythosHUD.exe" (
    echo Installing Python dependencies with %PYTHON_CMD%...
    %PYTHON_CMD% -m pip install -r "%~dp0requirements.txt"
)

echo.
echo [2/2] Creating Desktop Shortcut...
set "TARGET_EXE=%~dp0run.bat"
set "WORKING_DIR=%~dp0"
if exist "%~dp0dist\MythosHUD\MythosHUD.exe" (
    set "TARGET_EXE=%~dp0dist\MythosHUD\MythosHUD.exe"
    set "WORKING_DIR=%~dp0dist\MythosHUD"
)

powershell -NoProfile -Command "& { $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\MythosHUD.lnk'); $Shortcut.TargetPath = '%TARGET_EXE%'; $Shortcut.WorkingDirectory = '%WORKING_DIR%'; $Shortcut.Save() }"

echo.
echo ========================================================
echo   [SUCCESS] MythosHUD has been installed!
echo   Double-click the 'MythosHUD' shortcut on your Desktop
echo   to launch the suite anytime.
echo ========================================================
echo.
pause
