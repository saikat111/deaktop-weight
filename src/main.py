import os
import sys
import json
import time
import subprocess
import threading
import webview

# Add current dir to path
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURR_DIR)
sys.path.insert(0, PROJECT_ROOT)

from src.telemetry import TelemetryCollector

CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.json")

def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"theme": "elysium_cyan", "opacity": 0.92, "widgets": {}}

def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass

class WidgetApi:
    def __init__(self, app_manager):
        self.mgr = app_manager

    def get_config(self):
        return self.mgr.config

    def set_theme(self, theme_name):
        self.mgr.config["theme"] = theme_name
        save_config(self.mgr.config)
        self.mgr.broadcast_theme(theme_name)

    def toggle_widget(self, name):
        self.mgr.toggle_widget(name)

    def launch_app(self, app_name):
        try:
            if app_name == "powershell":
                subprocess.Popen(["powershell.exe"])
            elif app_name == "chrome":
                subprocess.Popen(["cmd.exe", "/c", "start", "chrome"])
            elif app_name == "taskmgr":
                subprocess.Popen(["taskmgr.exe"])
            elif app_name == "docker":
                subprocess.Popen(["cmd.exe", "/c", "start", "docker desktop"])
        except Exception as e:
            print(f"Error launching {app_name}: {e}")

    def close_all(self):
        self.mgr.close_all()

class MythosWindowManager:
    def __init__(self):
        self.config = load_config()
        self.collector = TelemetryCollector()
        self.windows = {}
        self.api = WidgetApi(self)
        self._running = True

    def build_url(self, filename):
        path = os.path.join(CURR_DIR, "ui", filename)
        return "file:///" + path.replace("\\", "/")

    def broadcast_theme(self, theme_name):
        for name, win in self.windows.items():
            try:
                win.evaluate_js(f"updateTheme('{theme_name}');")
            except Exception:
                pass

    def toggle_widget(self, name):
        win = self.windows.get(name)
        if win:
            # If open, close it
            try:
                win.destroy()
            except Exception:
                pass
            del self.windows[name]
            self.config["widgets"][name]["enabled"] = False
            save_config(self.config)
        else:
            # Reopen
            self.config["widgets"][name]["enabled"] = True
            save_config(self.config)
            self._create_single_widget(name)

    def _create_single_widget(self, name):
        cfg = self.config.get("widgets", {}).get(name, {})
        url = self.build_url(f"{name}.html")
        win = webview.create_window(
            title=f"MythosHUD - {name.capitalize()}",
            url=url,
            width=cfg.get("width", 340),
            height=cfg.get("height", 300),
            x=cfg.get("x", 100),
            y=cfg.get("y", 100),
            frameless=True,
            easy_drag=True,
            transparent=True,
            on_top=False,
            js_api=self.api
        )
        self.windows[name] = win

    def close_all(self):
        self._running = False
        for win in list(self.windows.values()):
            try:
                win.destroy()
            except Exception:
                pass
        sys.exit(0)

    def start_telemetry_loop(self):
        def loop():
            # Initial wait for DOM readiness
            time.sleep(1.5)
            while self._running:
                data = self.collector.get_telemetry()
                json_str = json.dumps(data)
                for name, win in list(self.windows.items()):
                    try:
                        win.evaluate_js(f"if (typeof updateTelemetry === 'function') updateTelemetry({json_str});")
                    except Exception:
                        pass
                time.sleep(1.0)
        t = threading.Thread(target=loop, daemon=True)
        t.start()

    def run(self):
        widgets_cfg = self.config.get("widgets", {})
        # Create all enabled widgets
        for name, wcfg in widgets_cfg.items():
            if wcfg.get("enabled", True):
                self._create_single_widget(name)

        self.start_telemetry_loop()
        webview.start()

if __name__ == "__main__":
    manager = MythosWindowManager()
    manager.run()
