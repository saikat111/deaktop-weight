# ⚡ MythosHUD — Ancient Greek Mythological Desktop Widgets for Windows

[![Windows 10 / 11 Supported](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-00f0ff?style=for-the-badge&logo=windows)](https://github.com/saikat111/deaktop-weight)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![RAM Usage: <30MB](https://img.shields.io/badge/Memory-%3C30MB%20RAM-ff2a5f?style=for-the-badge)](https://github.com/saikat111/deaktop-weight)

**MythosHUD** is a suite of ultra-lightweight, GPU-accelerated desktop widgets engineered with a **Dark Cyber-Hellenic & Tactical Gaming aesthetic**. Inspired by classical Greek mythology (*Hades*, *God of War*, ancient Athenian astrolabes) merged with futuristic cyber telemetry, it replaces bloated desktop software with native, transparent, frameless Windows widgets that consume **under 30MB of RAM total**.

---

## 🏛️ The Mythological Widget Arsenal

```
   ┌──────────────────────────────────────────────────────────────┐
   │                  Ω  MYTHOS COMMAND DOCK                      │
   │  [FORGE]   [CHRONOS]   [ZEUS]   [HERMES]   [ORACLE]  [THEME] │
   └──────────────────────────────────────────────────────────────┘
```

### 1. ⚒️ Hephaestus Core (Hardware Telemetry HUD)
* **Deity:** Hephaestus, Divine Smith & God of Metallurgy.
* **Telemetry:** Real-time CPU usage, clock speed (MHz), active cores/threads, RAM consumption (GB / %), and System Drive (C:) storage progress.
* **Visuals:** High-tech dual circular radial gauges with glowing cyan pulse rings and Spartan chamfered corners.

### 2. ⏳ Chronos Astrolabe (Celestial Clock & Lunar Transit)
* **Deity:** Chronos (Personification of Time) & Apollo (Sun God).
* **Telemetry:** Live 24-hour digital clock, full calendar date, Hellenic Month translation, classical Greek day of the gods (e.g. *Σελήνης*, *Άρεως*), and astronomical moon phase (*Selene*).
* **Visuals:** Deep obsidian astrolabe with subtle celestial rune rings.

### 3. ⚡ Zeus’ Aegis (Atmospheric & Weather Oracle)
* **Deity:** Zeus, Lord of the Sky, Thunder, and Lightning.
* **Telemetry:** Live outdoor temperature, meteorological condition, satellite humidity %, surface barometric pressure (hPa), and wind speed.
* **Visuals:** Lightning sigil glowing in obsidian glass with real-time satellite telemetry (zero API key required!).

### 4. 🪽 Hermes Caduceus (Network Throughput & Portals)
* **Deity:** Hermes, Fleet-Footed Herald of Olympus.
* **Telemetry:** Live network throughput speedometer (KB/s and MB/s download and upload).
* **Divine Portals:** Instant 1-click quick-launchers for **Terminal**, **Chrome**, **Task Manager**, and **Docker Desktop**.

### 5. 📜 Oracle of Delphi (Stoic Codex & Scratchpad)
* **Deity:** Pythia, Oracle of Apollo at Delphi.
* **Stoic Codex:** Rotating daily Stoic and Hellenic philosophical epigrams from Marcus Aurelius, Socrates, Epictetus, and Seneca.
* **Hermetic Parchment:** Instant, persistent desktop scratchpad for quick to-do tasks and notes that auto-saves instantly to local storage.

---

## 🎮 Dark Gaming Theme Presets (Zero Tacky Gold)

Designed strictly with matte dark obsidian glass and neon gaming accents:

| Theme Preset | Color Scheme | Mythological Lore |
| :--- | :--- | :--- |
| **`elysium_cyan`** *(Default)* | Deep Obsidian + Electric Neon Cyan (`#00f0ff`) | Fields of Elysium, lightning & digital ice |
| **`tartarus_crimson`** | Matte Gunmetal + Spartan Crimson (`#ff2a5f`) | Volcanic depths of Tartarus & Ares' fury |
| **`hades_violet`** | Void Black + Ethereal Soulfire Violet (`#a855f7`) | Underworld amethyst & chthonic mystery |
| **`spartan_silver`** | Titanium Slate + Frost White / Diamond Chrome (`#e2e8f0`) | Polished Spartan armor & Olympus peaks |

> **Cycle Themes Instantly:** Click the **THEME** button on the top Command Dock to cycle through all presets live without reloading.

---

## 🚀 Quick Start & Installation

### Option 1: 1-Click Launch (Recommended)
1. Clone or download this repository:
   ```cmd
   git clone https://github.com/saikat111/deaktop-weight.git
   cd deaktop-weight
   ```
2. Double-click **`run.bat`** (or run `install.bat` to create a Desktop shortcut).
3. The transparent widgets will immediately appear on your desktop!

### Option 2: Manual Python Launch
```bash
pip install -r requirements.txt
python src/main.py
```

---

## ⚙️ Configuration & Customization (`config.json`)

All widget positions, active states, and dimensions are automatically stored in `config.json`:

```json
{
  "theme": "elysium_cyan",
  "opacity": 0.92,
  "refresh_rate_ms": 1000,
  "widgets": {
    "hub": { "enabled": true, "x": 20, "y": 40, "width": 380, "height": 95 },
    "hephaestus": { "enabled": true, "x": 20, "y": 150, "width": 360, "height": 380 },
    "chronos": { "enabled": true, "x": 1520, "y": 40, "width": 360, "height": 320 },
    "zeus": { "enabled": true, "x": 1520, "y": 380, "width": 360, "height": 260 },
    "hermes": { "enabled": true, "x": 20, "y": 550, "width": 360, "height": 280 },
    "oracle": { "enabled": true, "x": 1520, "y": 660, "width": 360, "height": 320 }
  }
}
```

* **Repositioning:** Simply click and drag any widget by its top header bar.
* **Toggle Widgets:** Click any button on the top Command Dock (**FORGE**, **CHRONOS**, **ZEUS**, **HERMES**, **ORACLE**) to hide or show individual widgets instantly.

---

## 🛠️ Architecture & Under the Hood

Unlike heavy Electron applications that spawn multiple full Chromium browser instances (eating 500MB+ RAM), **MythosHUD** is built on:
- **Microsoft Edge WebView2**: Pre-installed on Windows 10 & 11 natively, utilizing shared OS runtime libraries.
- **DWM Hardware Blending**: True alpha transparency via `DirectComposition` & `DWM Glass Blur` (`dwmapi.dll`).
- **Low-Overhead Telemetry Subsystem**: Hardware polling running in an isolated lightweight background daemon consuming `<0.2% CPU`.

---

## 📜 License

Distributed under the **MIT License**. Free for personal and commercial modification.
Built with divine precision for gamers, overclockers, and developers.
