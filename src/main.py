import os
import sys
import json
import time
import uuid
import shutil
import webbrowser
import subprocess
import threading
import webview

# Add current and parent dir to path
if getattr(sys, 'frozen', False):
    EXE_DIR = os.path.dirname(sys.executable)
    BUNDLE_DIR = getattr(sys, '_MEIPASS', EXE_DIR)
    PROJECT_ROOT = EXE_DIR
    CURR_DIR = os.path.join(BUNDLE_DIR, "src")
else:
    CURR_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(CURR_DIR)
    BUNDLE_DIR = PROJECT_ROOT

sys.path.insert(0, PROJECT_ROOT)
if BUNDLE_DIR not in sys.path:
    sys.path.insert(0, BUNDLE_DIR)

from src.telemetry import TelemetryCollector
from src.wallpaper import set_theme_wallpaper, set_custom_wallpaper

CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.json")

DEFAULT_APPS = [
    { "id": "vscode", "name": "VS Code", "cmd": "vscode", "cat": "dev", "removable": False },
    { "id": "terminal", "name": "Terminal", "cmd": "terminal", "cat": "dev", "removable": False },
    { "id": "docker", "name": "Docker", "cmd": "docker", "cat": "dev", "removable": False },
    { "id": "gitbash", "name": "Git Bash", "cmd": "gitbash", "cat": "dev", "removable": False },
    { "id": "steam", "name": "Steam", "cmd": "steam", "cat": "game", "removable": False },
    { "id": "discord", "name": "Discord", "cmd": "discord", "cat": "game", "removable": False },
    { "id": "spotify", "name": "Spotify", "cmd": "spotify", "cat": "game", "removable": False },
    { "id": "obs", "name": "OBS Studio", "cmd": "obs", "cat": "game", "removable": False },
    { "id": "taskmgr", "name": "Task Mgr", "cmd": "taskmgr", "cat": "sys", "removable": False },
    { "id": "calc", "name": "Calculator", "cmd": "calc", "cat": "sys", "removable": False },
    { "id": "explorer", "name": "Files", "cmd": "explorer", "cat": "sys", "removable": False },
    { "id": "chrome", "name": "Chrome", "cmd": "chrome", "cat": "sys", "removable": False }
]

def load_config():
    try:
        target_path = CONFIG_PATH
        if not os.path.exists(target_path) and os.path.exists(os.path.join(BUNDLE_DIR, "config.json")):
            target_path = os.path.join(BUNDLE_DIR, "config.json")
        with open(target_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            if "apps" not in cfg or not cfg["apps"]:
                cfg["apps"] = DEFAULT_APPS
            return cfg
    except Exception:
        return {
            "theme": "elysium_cyan",
            "opacity": 0.92,
            "auto_wallpaper": True,
            "apps": DEFAULT_APPS,
            "widgets": {}
        }

def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
    except Exception as e:
        print(f"Error saving config: {e}")

class WidgetApi:
    """Exposed JS Bridge for high-performance Native <-> WebView2 interaction."""
    def __init__(self, app_manager):
        self.mgr = app_manager

    def get_config(self):
        return self.mgr.config

    def set_config_value(self, key, val):
        self.mgr.config[key] = val
        save_config(self.mgr.config)
        return True

    def set_theme(self, theme_name):
        self.mgr.config["theme"] = theme_name
        save_config(self.mgr.config)
        self.mgr.broadcast_theme(theme_name)
        if self.mgr.config.get("auto_wallpaper", True):
            set_theme_wallpaper(theme_name)
        return True

    def set_wallpaper(self, path_or_theme):
        if path_or_theme in ["elysium_cyan", "tartarus_crimson", "hades_violet", "spartan_silver"]:
            return set_theme_wallpaper(path_or_theme)
        else:
            success = set_custom_wallpaper(path_or_theme)
            if success:
                self.mgr.config["custom_wallpaper_path"] = path_or_theme
                save_config(self.mgr.config)
            return success

    def browse_and_set_wallpaper(self):
        """Opens native Windows file dialog to choose a custom wallpaper."""
        for win in self.mgr.windows.values():
            try:
                res = win.create_file_dialog(
                    webview.OPEN_DIALOG,
                    allow_multiple=False,
                    file_types=('Image Files (*.png;*.jpg;*.jpeg;*.bmp)', 'All files (*.*)')
                )
                if res and len(res) > 0:
                    path = res[0]
                    if set_custom_wallpaper(path):
                        self.mgr.config["custom_wallpaper_path"] = path
                        save_config(self.mgr.config)
                        return path
            except Exception as e:
                print(f"Error in file dialog: {e}")
        return None

    def set_opacity(self, alpha):
        self.mgr.config["opacity"] = alpha
        save_config(self.mgr.config)
        self.mgr.broadcast_opacity(alpha)
        return True

    def get_apps(self):
        return self.mgr.config.get("apps", DEFAULT_APPS)

    def add_app(self, name, cmd, cat):
        app_id = f"custom_{uuid.uuid4().hex[:6]}"
        new_app = {
            "id": app_id,
            "name": name,
            "cmd": cmd,
            "cat": cat or "custom",
            "removable": True
        }
        if "apps" not in self.mgr.config:
            self.mgr.config["apps"] = list(DEFAULT_APPS)
        self.mgr.config["apps"].append(new_app)
        save_config(self.mgr.config)
        return True

    def remove_app(self, app_id):
        if "apps" in self.mgr.config:
            self.mgr.config["apps"] = [a for a in self.mgr.config["apps"] if a["id"] != app_id]
            save_config(self.mgr.config)
            return True
        return False

    def toggle_widget(self, name):
        self.mgr.toggle_widget(name)

    def toggle_all_visibility(self):
        self.mgr.toggle_all_visibility()

    def launch_app(self, app_name_or_cmd):
        try:
            target = app_name_or_cmd.strip()
            # If it's a URL
            if target.startswith("http://") or target.startswith("https://"):
                webbrowser.open(target)
                return True

            # Predefined quick aliases
            if target == "vscode":
                code_path = shutil.which("code") or "code"
                subprocess.Popen([code_path], shell=True)
            elif target == "terminal":
                wt_path = shutil.which("wt") or shutil.which("powershell") or "powershell"
                subprocess.Popen([wt_path])
            elif target == "powershell":
                subprocess.Popen(["powershell.exe"])
            elif target == "taskmgr":
                subprocess.Popen(["taskmgr.exe"])
            elif target == "calc":
                subprocess.Popen(["calc.exe"])
            elif target == "explorer":
                subprocess.Popen(["explorer.exe"])
            elif target == "docker":
                subprocess.Popen(["cmd.exe", "/c", "start", "docker desktop"], shell=True)
            elif target == "chrome":
                subprocess.Popen(["cmd.exe", "/c", "start", "chrome"], shell=True)
            elif target == "gitbash":
                git_path = r"C:\Program Files\Git\git-bash.exe"
                if os.path.exists(git_path):
                    subprocess.Popen([git_path])
                else:
                    subprocess.Popen(["cmd.exe", "/c", "start", "git-bash"], shell=True)
            elif target == "steam":
                subprocess.Popen(["cmd.exe", "/c", "start", "steam://"], shell=True)
            elif target == "discord":
                subprocess.Popen(["cmd.exe", "/c", "start", "discord://"], shell=True)
            elif target == "spotify":
                subprocess.Popen(["cmd.exe", "/c", "start", "spotify:"], shell=True)
            elif target == "obs":
                subprocess.Popen(["cmd.exe", "/c", "start", "obs64"], shell=True)
            else:
                # Custom command, file, or executable path
                subprocess.Popen([target], shell=True)
            return True
        except Exception as e:
            print(f"Error launching {app_name_or_cmd}: {e}")
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
        if not os.path.exists(path):
            path = os.path.join(BUNDLE_DIR, "src", "ui", filename)
        if not os.path.exists(path):
            path = os.path.join(PROJECT_ROOT, "src", "ui", filename)
        return "file:///" + os.path.abspath(path).replace("\\", "/")

    def broadcast_theme(self, theme_name):
        for name, win in self.windows.items():
            try:
                win.evaluate_js(f"if (typeof updateTheme === 'function') updateTheme('{theme_name}');")
            except Exception:
                pass

    def broadcast_opacity(self, alpha):
        for name, win in self.windows.items():
            try:
                win.evaluate_js(f"if (typeof updateOpacity === 'function') updateOpacity({alpha});")
            except Exception:
                pass

    def toggle_all_visibility(self):
        """Boss / Stealth mode toggle."""
        self._stealth_active = not self._stealth_active
        for name, win in self.windows.items():
            if name == "hub":
                continue # Keep the Hub visible so user can un-stealth
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
