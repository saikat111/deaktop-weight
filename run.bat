@echo off
setlocal
title MythosHUD - Greek Mythological Desktop Widgets
echo ========================================================
echo       MYTHOS HUD - CYBER-HELLENIC DESKTOP WIDGETS
echo ========================================================
echo Starting telemetry engine and transparent overlays...

set "PYTHON_CMD=python"
if exist "%APPDATA%\uv\tools\windows-mcp\Scripts\python.exe" (
    set "PYTHON_CMD=%APPDATA%\uv\tools\windows-mcp\Scripts\python.exe"
) else (
    where py >nul 2>&1 && (
        py -3.12 --version >nul 2>&1 && set "PYTHON_CMD=py -3.12"
    )
)

%PYTHON_CMD% src/main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] An error occurred while launching MythosHUD.
    pause
)
