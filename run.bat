@echo off
title MythosHUD - Greek Mythological Desktop Widgets
echo ========================================================
echo       MYTHOS HUD - CYBER-HELLENIC DESKTOP WIDGETS
echo ========================================================
echo Starting telemetry engine and transparent overlays...

python -m pip install -r requirements.txt --quiet
python src/main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] An error occurred while launching MythosHUD.
    pause
)
