@echo off
setlocal
title MythosHUD - Executable Builder
echo ========================================================
echo       MYTHOS HUD - STANDALONE COMPILER (.EXE)
echo ========================================================
echo.

cd /d "%~dp0"

set "PYTHON_CMD=python"
if exist "%APPDATA%\uv\tools\windows-mcp\Scripts\python.exe" (
    set "PYTHON_CMD=%APPDATA%\uv\tools\windows-mcp\Scripts\python.exe"
) else (
    where py >nul 2>&1 && (
        py -3.12 --version >nul 2>&1 && set "PYTHON_CMD=py -3.12"
    )
)

echo [1/3] Ensuring PyInstaller is installed...
%PYTHON_CMD% -m pip install pyinstaller --quiet

echo [2/3] Compiling standalone MythosHUD binary...
%PYTHON_CMD% -m PyInstaller --noconfirm --onedir --windowed --name "MythosHUD" --add-data "src\ui;src\ui" --add-data "src\assets;src\assets" --add-data "config.json;." src\main.py

if %errorlevel% neq 0 (
    echo [ERROR] Build failed! Check the output above.
    pause
    exit /b %errorlevel%
)

echo.
echo [3/3] Packaging distribution ZIP archive...
powershell -NoProfile -Command "Compress-Archive -Path '%~dp0dist\MythosHUD\*' -DestinationPath '%~dp0dist\MythosHUD-v1.0.0-windows-x64.zip' -Force"

echo.
echo ========================================================
echo   [SUCCESS] Standalone MythosHUD compiled successfully!
echo   Executable location: dist\MythosHUD\MythosHUD.exe
echo   Zip package:         dist\MythosHUD-v1.0.0-windows-x64.zip
echo ========================================================
echo.
pause
