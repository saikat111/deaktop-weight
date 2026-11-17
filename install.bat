@echo off
title MythosHUD Installer
echo ========================================================
echo       MYTHOS HUD - INSTALLER & SHORTCUT SETUP
echo ========================================================
echo.
echo [1/2] Installing Python dependencies...
python -m pip install -r requirements.txt

echo.
echo [2/2] Creating Desktop Shortcut...
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'MythosHUD.lnk')); $s.TargetPath = '%~dp0run.bat'; $s.WorkingDirectory = '%~dp0'; $s.WindowStyle = 7; $s.Save()"

echo.
echo ========================================================
echo   [SUCCESS] MythosHUD has been installed!
echo   Double-click the 'MythosHUD' shortcut on your Desktop
echo   or run 'run.bat' to launch the widgets suite anytime.
echo ========================================================
echo.
pause
