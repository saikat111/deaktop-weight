# ⚡ MythosHUD — Ancient Greek Mythological Desktop Suite for Windows

[![Windows 10 / 11 Supported](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-00f0ff?style=for-the-badge&logo=windows)](https://github.com/saikat111/deaktop-weight)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![RAM Usage: <30MB](https://img.shields.io/badge/Memory-%3C30MB%20RAM-ff2a5f?style=for-the-badge)](https://github.com/saikat111/deaktop-weight)

**MythosHUD** is a suite of ultra-lightweight, GPU-accelerated desktop widgets engineered with a **Dark Cyber-Hellenic Gaming & Developer Cockpit aesthetic**. Inspired by classical Greek mythology (*Hades*, *God of War*, ancient Athenian astrolabes) merged with futuristic cyber telemetry, it replaces bloated desktop software with native, transparent, frameless Windows widgets consuming **under 30MB of RAM total**.

Strictly **NO GOLD / NO TACKY SKINS** — styled in pure matte obsidian glass, neon electric cyan, Spartan crimson, and Hades violet.

---

## 🏛️ Architecture & Widget Arsenal

```
   ┌────────────────────────────────────────────────────────────────────────────────────────┐
   │                                  Ω  MYTHOS COMMAND DOCK                                │
   │  [FORGE] [CHRONOS] [ZEUS] [HERMES] [ORACLE] [DEV DECK] [APPS] [WALLPAPER] [STEALTH]  │
   │  [⏮ ⏯ ⏭ 🔉 🔊]  ılılılı (AUDIO SPECTRUM)                                             │
   └────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1. ⚙️ Hephaestus Dev Cockpit (`devdeck.html`)
* **Local Port Sentinel:** Real-time port beacons for `localhost:3000`, `3050`, `8000`, and `8080`. Green beacon indicates active listener; click any port pill to launch it directly in your browser.
* **Docker Container Monitor:** Displays running vs total container counts with container names and engine health.
* **Git Repository Telemetry:** Displays current branch and uncommitted modified changes in real time.
* **Gaming Ping Radar:** Live latency probe in milliseconds (`ms`) to Cloudflare DNS (`1.1.1.1`) with divine/optimal latency badges.
* **Spartan Combat Focus Mode:** 25-minute Pomodoro deep-work timer with live progress bar and completion alerts.

### 2. ☵ Pantheon App Launcher (`apps.html`)
* **Instant Filter Search:** Filter across applications and CLI tools as you type.
* **Developer Tools:** 1-click launchers for **VS Code**, **Windows Terminal / PowerShell**, **Docker Desktop**, and **Git Bash**.
* **Gaming & Media:** 1-click launchers for **Steam**, **Discord**, **Spotify**, and **OBS Studio**.
* **System Utilities:** Instant access to **Task Manager**, **Calculator**, **File Explorer**, and **Chrome / Edge**.

### 3. 🖼️ In-Built Dynamic Wallpaper Engine (`src/wallpaper.py`)
* Generates 4K procedural Cyber-Hellenic dark obsidian wallpapers on-the-fly with constellation networks, sacred geometry astrolabe sigils, and Greek meander (key) fretwork borders.
* **1-Click Apply:** Click the **WALLPAPER** button on the Command Dock to apply the matching wallpaper directly to your Windows desktop via native Win32 `SystemParametersInfoW`.

### 4. ⚒️ Hephaestus Core Telemetry (`hephaestus.html`)
* **Hardware Gauges:** Dual radial SVG gauges for CPU and RAM load with glow pulses.
* **Frequency & Cores:** Real-time CPU clock frequency (MHz), logical thread count, and RAM allocation in GB.
* **Storage Progress:** Real-time disk space usage for System Drive (`C:`).
* **Process Inspector & Ram Purge:** Displays top memory-consuming background processes with a 1-click **KILL** button for rogue tasks.

### 5. ⏳ Chronos Astrolabe (`chronos.html`)
* **Celestial Clock:** 24-hour digital clock with seconds pulse.
* **Greek Planetary Days:** Displays ancient day names (*Σελήνης*, *Άρεως*, *Ερμού*, *Διός*, *Αφροδίτης*, *Κρόνου*, *Ηλίου*).
* **Lunar Transit:** Astronomical phase calculator (*Selene*, *Hecate*, Gibbous, Crescent).

### 6. ⚡ Zeus’ Aegis Weather Oracle (`zeus.html`)
* **Satellite Weather:** Live temperature (°C), conditions, humidity %, barometric pressure (hPa), and wind speed via Open-Meteo satellite feed. Zero API key required!

### 7. 🪽 Hermes Throughput Speedometer (`hermes.html`)
* **Network Speed:** Live network speedometer with real-time download and upload throughput in KB/s and MB/s.

### 8. 📜 Oracle of Delphi & Hermetic Scratchpad (`oracle.html`)
* **Stoic Codex:** Rotating daily wisdom from Marcus Aurelius, Epictetus, Socrates, and Seneca.
* **Hermetic Parchment:** Persistent desktop scratchpad that saves notes and code snippets automatically.

---

## 🎮 Dark Gaming Theme Presets (Zero Gold)

| Theme Preset | Color Scheme | Lore |
| :--- | :--- | :--- |
| **`elysium_cyan`** *(Default)* | Deep Obsidian + Electric Neon Cyan (`#00f0ff`) | Fields of Elysium, lightning & digital ice |
| **`tartarus_crimson`** | Matte Gunmetal + Spartan Crimson (`#ff2a5f`) | Volcanic depths of Tartarus & Ares' fury |
| **`hades_violet`** | Void Black + Ethereal Soulfire Violet (`#a855f7`) | Underworld amethyst & chthonic mystery |
| **`spartan_silver`** | Titanium Slate + Frost White / Chrome (`#e2e8f0`) | Polished Spartan armor & Olympus peaks |

> **Cycle Themes:** Click **THEME** on the Command Dock to instantly re-theme all widgets simultaneously.

---

## 🚀 10 Community-Requested Power Features

1. **Local Port Sentinel:** Never guess whether your Next.js or FastAPI server is running.
2. **Docker Engine Sentinel:** Instant visibility into container states without opening heavy dashboards.
3. **Audio Spectrum Visualizer:** Reactive frequency visualizer animated on the HUD.
4. **Hardware Multimedia Controls:** Play/Pause, Next, Prev, Volume keys via Windows user32.
5. **Spartan Focus Mode:** Pomodoro timer built right into your HUD.
6. **Hardware & Notification Toasts:** Visual alert banners for high CPU (>85%) or saturated RAM.
7. **Gaming Ping Radar:** Continuous low-overhead latency testing to `1.1.1.1`.
8. **Stealth / Boss Mode:** 1-click button to hide or show all widgets immediately.
9. **RAM Purge & Process Killer:** Quick identification and termination of memory-hungry tasks.
10. **Game Mode Efficiency:** Polling adapts dynamically so widget telemetry never impacts game FPS.

---

## 📥 Quick Start & Installation

### 1-Click Setup (Recommended for any Windows PC)
1. Clone or download this repository:
   ```cmd
   git clone https://github.com/saikat111/deaktop-weight.git
   cd deaktop-weight
   ```
2. Run **`install.bat`** to install dependencies and automatically create a `MythosHUD` shortcut on your Desktop.
3. Double-click the desktop shortcut or run **`run.bat`** anytime!

### Manual Launch
```bash
pip install -r requirements.txt
python src/main.py
```

---

## ⚙️ Configuration (`config.json`)

All widget coordinates, dimensions, and toggle states are saved in `config.json`:

```json
{
  "theme": "elysium_cyan",
  "opacity": 0.92,
  "refresh_rate_ms": 1000,
  "widgets": {
    "hub": { "enabled": true, "x": 20, "y": 30, "width": 860, "height": 75 },
    "hephaestus": { "enabled": true, "x": 20, "y": 120, "width": 360, "height": 430 },
    "hermes": { "enabled": true, "x": 20, "y": 565, "width": 360, "height": 280 },
    "devdeck": { "enabled": true, "x": 395, "y": 120, "width": 370, "height": 440 },
    "apps": { "enabled": true, "x": 395, "y": 575, "width": 370, "height": 380 },
    "chronos": { "enabled": true, "x": 1520, "y": 30, "width": 360, "height": 320 },
    "zeus": { "enabled": true, "x": 1520, "y": 365, "width": 360, "height": 260 },
    "oracle": { "enabled": true, "x": 1520, "y": 640, "width": 360, "height": 340 }
  }
}
```

* **Repositioning:** Simply click and drag any widget by its top title bar.
* **Toggle Widgets:** Click widget buttons on the Command Dock to hide or restore individual panels.

---

## 📜 License

Distributed under the **MIT License**. Free for personal, commercial, and community modification.
Built with divine precision for gamers, overclockers, and developers.
