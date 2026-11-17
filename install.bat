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

echo [1/2] Installing Python dependencies with %PYTHON_CMD%...
%PYTHON_CMD% -m pip install -r "%~dp0requirements.txt"

echo.
echo [2/2] Creating Desktop Shortcut...
powershell -NoProfile -Command "& { $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\MythosHUD.lnk'); $Shortcut.TargetPath = '%~dp0run.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save() }"

echo.
echo ========================================================
echo   [SUCCESS] MythosHUD has been installed!
echo   Double-click the 'MythosHUD' shortcut on your Desktop
echo   or run 'run.bat' to launch the widgets suite anytime.
echo ========================================================
echo.
pause
