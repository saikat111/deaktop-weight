import os
import sys
import json
import time
import shutil
import webbrowser
import subprocess
import threading
import webview

# Add current and parent dir to path
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURR_DIR)
sys.path.insert(0, PROJECT_ROOT)

from src.telemetry import TelemetryCollector
from src.wallpaper import set_theme_wallpaper

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
    """Exposed JS Bridge for high-performance Native <-> WebView2 interaction."""
    def __init__(self, app_manager):
        self.mgr = app_manager

    def get_config(self):
        return self.mgr.config

    def set_theme(self, theme_name):
        self.mgr.config["theme"] = theme_name
        save_config(self.mgr.config)
        self.mgr.broadcast_theme(theme_name)

    def set_wallpaper(self, theme_name):
        return set_theme_wallpaper(theme_name)

    def toggle_widget(self, name):
        self.mgr.toggle_widget(name)

    def toggle_all_visibility(self):
        self.mgr.toggle_all_visibility()

    def launch_app(self, app_name):
        try:
            if app_name == "vscode":
                code_path = shutil.which("code") or "code"
                subprocess.Popen([code_path], shell=True)
            elif app_name == "terminal":
                wt_path = shutil.which("wt") or shutil.which("powershell") or "powershell"
                subprocess.Popen([wt_path])
            elif app_name == "powershell":
                subprocess.Popen(["powershell.exe"])
            elif app_name == "taskmgr":
                subprocess.Popen(["taskmgr.exe"])
            elif app_name == "calc":
                subprocess.Popen(["calc.exe"])
            elif app_name == "explorer":
                subprocess.Popen(["explorer.exe"])
            elif app_name == "docker":
                subprocess.Popen(["cmd.exe", "/c", "start", "docker desktop"], shell=True)
            elif app_name == "chrome":
                subprocess.Popen(["cmd.exe", "/c", "start", "chrome"], shell=True)
            elif app_name == "gitbash":
                git_path = r"C:\Program Files\Git\git-bash.exe"
                if os.path.exists(git_path):
                    subprocess.Popen([git_path])
                else:
                    subprocess.Popen(["cmd.exe", "/c", "start", "git-bash"], shell=True)
            elif app_name == "steam":
                subprocess.Popen(["cmd.exe", "/c", "start", "steam://"], shell=True)
            elif app_name == "discord":
                subprocess.Popen(["cmd.exe", "/c", "start", "discord://"], shell=True)
            elif app_name == "spotify":
                subprocess.Popen(["cmd.exe", "/c", "start", "spotify:"], shell=True)
            elif app_name == "obs":
                subprocess.Popen(["cmd.exe", "/c", "start", "obs64"], shell=True)
            else:
                subprocess.Popen(["cmd.exe", "/c", "start", app_name], shell=True)
            return True
        except Exception as e:
            print(f"Error launching {app_name}: {e}")
            return False

    def open_url(self, url):
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error opening URL {url}: {e}")
            return False

    def media_control(self, action):
        return self.mgr.collector.trigger_media(action)

    def kill_process(self, pid):
        return self.mgr.collector.kill_process(pid)

    def toggle_focus(self):
        return self.mgr.collector.toggle_focus_timer()

    def reset_focus(self):
        return self.mgr.collector.reset_focus_timer()

    def toggle_game_mode(self):
        return self.mgr.collector.toggle_game_mode()

    def close_all(self):
        self.mgr.close_all()

class MythosWindowManager:
    def __init__(self):
        self.config = load_config()
        self.collector = TelemetryCollector()
        self.windows = {}
        self.api = WidgetApi(self)
        self._running = True
        self._stealth_active = False

    def build_url(self, filename):
        path = os.path.join(CURR_DIR, "ui", filename)
        return "file:///" + path.replace("\\", "/")

    def broadcast_theme(self, theme_name):
        for name, win in self.windows.items():
            try:
                win.evaluate_js(f"updateTheme('{theme_name}');")
            except Exception:
                pass

    def toggle_all_visibility(self):
        """Boss / Stealth mode toggle."""
        self._stealth_active = not self._stealth_active
        for name, win in self.windows.items():
            if name == "hub":
                continue # Keep the Hub visible to un-stealth
            try:
                if self._stealth_active:
                    win.hide()
                else:
                    win.show()
            except Exception:
                pass

    def toggle_widget(self, name):
        win = self.windows.get(name)
        if win:
            try:
                win.destroy()
            except Exception:
                pass
            del self.windows[name]
            if name in self.config.get("widgets", {}):
                self.config["widgets"][name]["enabled"] = False
                save_config(self.config)
        else:
            if name in self.config.get("widgets", {}):
                self.config["widgets"][name]["enabled"] = True
                save_config(self.config)
            self._create_single_widget(name)

    def _create_single_widget(self, name):
        cfg = self.config.get("widgets", {}).get(name, {})
        url = self.build_url(f"{name}.html")
        win = webview.create_window(
            title=f"MythosHUD - {name.capitalize()}",
            url=url,
            width=cfg.get("width", 360),
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
            time.sleep(1.2)
            while self._running:
                data = self.collector.get_telemetry()
                json_str = json.dumps(data)
                for name, win in list(self.windows.items()):
                    try:
                        win.evaluate_js(f"if (typeof updateTelemetry === 'function') updateTelemetry({json_str});")
                    except Exception:
                        pass
                # Adapt poll interval if game mode is active for ultra low latency
                poll_interval = 4.0 if self.collector._game_mode else 1.0
                time.sleep(poll_interval)
        t = threading.Thread(target=loop, daemon=True)
        t.start()

    def run(self):
        widgets_cfg = self.config.get("widgets", {})
        for name, wcfg in widgets_cfg.items():
            if wcfg.get("enabled", True):
                self._create_single_widget(name)

        self.start_telemetry_loop()
        webview.start()

if __name__ == "__main__":
    manager = MythosWindowManager()
    manager.run()
