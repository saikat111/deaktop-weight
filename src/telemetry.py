import os
import re
import time
import math
import socket
import random
import ctypes
import psutil
import requests
import subprocess
import threading

GREEK_DAYS = ["Σελήνης (Mon)", "Άρεως (Tue)", "Ερμού (Wed)", "Διός (Thu)", "Αφροδίτης (Fri)", "Κρόνου (Sat)", "Ηλίου (Sun)"]
GREEK_MONTHS = [
    "Ιανουάριος", "Φεβρουάριος", "Μάρτιος", "Απρίλιος",
    "Μάιος", "Ιούνιος", "Ιούλιος", "Αύγουστος",
    "Σεπτέμβριος", "Οκτώβριος", "Νοέμβριος", "Δεκέμβριος"
]

MYTHOS_QUOTES = [
    {"author": "Marcus Aurelius", "quote": "You have power over your mind - not outside events. Realize this, and you will find strength."},
    {"author": "Epictetus", "quote": "No man is free who is not master of himself."},
    {"author": "Socrates", "quote": "The unexamined life is not worth living."},
    {"author": "Heraclitus", "quote": "Day by day, what you choose, what you think and what you do is who you become."},
    {"author": "Plato", "quote": "The first and greatest victory is to conquer yourself."},
    {"author": "Seneca", "quote": "Luck is what happens when preparation meets opportunity."},
    {"author": "Aristotle", "quote": "We are what we repeatedly do. Excellence, then, is not an act, but a habit."},
    {"author": "Homer", "quote": "Even his griefs are a joy long after to one that remembers all that he wrought and endured."}
]

DEV_PORTS = [3000, 3050, 8000, 8080]

# Virtual Key Codes for Windows Media & Audio Controls
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3

def send_win_key(code):
    """Triggers standard Windows multimedia key via user32."""
    try:
        ctypes.windll.user32.keybd_event(code, 0, 0, 0)
        ctypes.windll.user32.keybd_event(code, 0, 2, 0) # KEYEVENTF_KEYUP
        return True
    except Exception:
        return False

class TelemetryCollector:
    def __init__(self):
        self._last_net = psutil.net_io_counters()
        self._last_time = time.time()
        self._weather_cache = {
            "city": "Mount Olympus",
            "temp": 24,
            "condition": "Clear Sky",
            "humidity": 45,
            "wind": 12,
            "pressure": 1013
        }
        self._quote_index = 0
        self._quote_last_switch = time.time()

        # Telemetry Cache
        self._port_cache = {str(p): False for p in DEV_PORTS}
        self._docker_cache = {"running": 0, "total": 0, "names": []}
        self._git_cache = {"branch": "main", "uncommitted": 0, "status": "Clean"}
        self._ping_cache = {"ms": 14, "status": "Optimal (14ms)"}
        self._top_procs = []
        self._audio_spectrum = [20, 45, 60, 80, 55, 40, 25, 15]
        self._game_mode = False

        # Focus / Pomodoro Mode
        self._focus_active = False
        self._focus_remaining = 1500 # 25 mins
        self._focus_total = 1500
        self._focus_last_tick = time.time()

        # Background loops
        threading.Thread(target=self._update_weather_loop, daemon=True).start()
        threading.Thread(target=self._update_dev_loop, daemon=True).start()

    def _update_weather_loop(self):
        while True:
            try:
                r_loc = requests.get("http://ip-api.com/json/", timeout=5).json()
                lat = r_loc.get("lat", 37.9838)
                lon = r_loc.get("lon", 23.7275)
                city = r_loc.get("city", "Athens")

                w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,weather_code"
                r_w = requests.get(w_url, timeout=5).json()
                current = r_w.get("current", {})

                code = current.get("weather_code", 0)
                condition = "Clear Sky"
                if code in [1, 2, 3]: condition = "Partly Cloudy"
                elif code in [45, 48]: condition = "Misty Fog"
                elif code in [51, 53, 55, 61, 63, 65]: condition = "Zeus' Rain"
                elif code in [71, 73, 75]: condition = "Boreas' Snow"
                elif code in [95, 96, 99]: condition = "Thunderstorm"

                self._weather_cache = {
                    "city": city,
                    "temp": round(current.get("temperature_2m", 24)),
                    "condition": condition,
                    "humidity": current.get("relative_humidity_2m", 50),
                    "wind": round(current.get("wind_speed_10m", 10)),
                    "pressure": round(current.get("surface_pressure", 1013))
                }
            except Exception:
                pass
            time.sleep(900)

    def _check_port(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.12)
        try:
            s.connect(('127.0.0.1', port))
            s.close()
            return True
        except Exception:
            return False

    def _update_dev_loop(self):
        tick = 0
        while True:
            tick += 1
            # 1. Dev Server Ports
            ports_status = {}
            for p in DEV_PORTS:
                ports_status[str(p)] = self._check_port(p)
            self._port_cache = ports_status

            # 2. Docker Containers
            try:
                res = subprocess.run(
                    ["docker", "ps", "-a", "--format", "{{.Names}}|{{.Status}}"],
                    capture_output=True, text=True, timeout=2
                )
                if res.returncode == 0:
                    lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip()]
                    running = sum(1 for l in lines if "Up" in l)
                    names = [l.split("|")[0] for l in lines[:5]]
                    self._docker_cache = {"running": running, "total": len(lines), "names": names}
            except Exception:
                self._docker_cache = {"running": 0, "total": 0, "names": []}

            # 3. Git Repo Status
            try:
                git_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                r_branch = subprocess.run(["git", "branch", "--show-current"], cwd=git_dir, capture_output=True, text=True, timeout=1)
                r_status = subprocess.run(["git", "status", "--porcelain"], cwd=git_dir, capture_output=True, text=True, timeout=1)
                branch = r_branch.stdout.strip() or "main"
                uncommitted = len([l for l in r_status.stdout.split("\n") if l.strip()])
                self._git_cache = {
                    "branch": branch,
                    "uncommitted": uncommitted,
                    "status": f"{uncommitted} Modified" if uncommitted > 0 else "Syncd"
                }
            except Exception:
                pass

            # 4. Gaming Ping Radar (every 3 ticks)
            if tick % 3 == 0:
                try:
                    res = subprocess.run(['ping', '-n', '1', '-w', '800', '1.1.1.1'], capture_output=True, text=True)
                    m = re.search(r'Average = (\d+)ms|time[<=](\d+)ms', res.stdout)
                    val = int(m.group(1) or m.group(2)) if m else 15
                    badge = "Divine" if val < 20 else ("Optimal" if val < 50 else "High")
                    self._ping_cache = {"ms": val, "status": f"{badge} ({val}ms)"}
                except Exception:
                    self._ping_cache = {"ms": 0, "status": "Offline"}

            # 5. Top 3 RAM-Hungry Processes (every 4 ticks)
            if tick % 4 == 0:
                try:
                    procs = []
                    for p in psutil.process_iter(['pid', 'name', 'memory_percent']):
                        try:
                            info = p.info
                            if info['memory_percent'] and info['memory_percent'] > 0.5:
                                procs.append({
                                    "pid": info['pid'],
                                    "name": info['name'],
                                    "mem_pct": round(info['memory_percent'], 1)
                                })
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    self._top_procs = sorted(procs, key=lambda x: x['mem_pct'], reverse=True)[:4]
                except Exception:
                    pass

            time.sleep(1.5)

    def trigger_media(self, action):
        """Controls media players (Spotify, YouTube, VLC, browser) via Windows keys."""
        mapping = {
            "play_pause": VK_MEDIA_PLAY_PAUSE,
            "next": VK_MEDIA_NEXT_TRACK,
            "prev": VK_MEDIA_PREV_TRACK,
            "vol_up": VK_VOLUME_UP,
            "vol_down": VK_VOLUME_DOWN,
            "mute": VK_VOLUME_MUTE
        }
        code = mapping.get(action)
        if code:
            return send_win_key(code)
        return False

    def kill_process(self, pid):
        """Terminates a runaway process safely."""
        try:
            p = psutil.Process(pid)
            p.terminate()
            return True
        except Exception as e:
            print(f"Error terminating process {pid}: {e}")
            return False

    def toggle_game_mode(self):
        """Reduces background widget polling for ultra-low latency during gaming."""
        self._game_mode = not self._game_mode
        return self._game_mode

    def toggle_focus_timer(self):
        """Starts/Pauses the 25-minute Spartan Focus / Pomodoro combat timer."""
        self._focus_active = not self._focus_active
        self._focus_last_tick = time.time()
        return self._focus_active

    def reset_focus_timer(self, minutes=25):
        self._focus_total = minutes * 60
        self._focus_remaining = self._focus_total
        self._focus_active = False
        return self._focus_remaining

    def get_moon_phase(self):
        diff = time.time() - 947163600
        days = diff / 86400
        cycles = days / 29.53058867
        phase = (cycles - math.floor(cycles))
        if phase < 0.05 or phase > 0.95: return "New Moon (Hecate)"
        elif phase < 0.25: return "Waxing Crescent"
        elif phase < 0.30: return "First Quarter"
        elif phase < 0.45: return "Waxing Gibbous"
        elif phase < 0.55: return "Full Moon (Selene)"
        elif phase < 0.70: return "Waning Gibbous"
        elif phase < 0.80: return "Last Quarter"
        else: return "Waning Crescent"

    def get_telemetry(self):
        now = time.time()
        dt = max(now - self._last_time, 0.001)

        # Focus timer countdown
        if self._focus_active and self._focus_remaining > 0:
            elapsed = now - self._focus_last_tick
            self._focus_remaining = max(0, int(self._focus_remaining - elapsed))
            self._focus_last_tick = now
            if self._focus_remaining == 0:
                self._focus_active = False

        # CPU & Hardware
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_freq = psutil.cpu_freq()
        freq_mhz = round(cpu_freq.current) if cpu_freq else 3600
        core_count = psutil.cpu_count(logical=True)

        # RAM
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        ram_used_gb = round(ram.used / (1024**3), 2)
        ram_total_gb = round(ram.total / (1024**3), 1)

        # Disk
        try:
            disk = psutil.disk_usage("C:\\")
            disk_percent = disk.percent
            disk_free_gb = round(disk.free / (1024**3), 1)
        except Exception:
            disk_percent = 50
            disk_free_gb = 100

        # Network
        net = psutil.net_io_counters()
        bytes_recv = max(net.bytes_recv - self._last_net.bytes_recv, 0)
        bytes_sent = max(net.bytes_sent - self._last_net.bytes_sent, 0)
        down_speed_kb = round(bytes_recv / dt / 1024, 1)
        up_speed_kb = round(bytes_sent / dt / 1024, 1)

        self._last_net = net
        self._last_time = now

        # Clocks
        lt = time.localtime(now)
        time_str = time.strftime("%H:%M:%S", lt)
        date_str = time.strftime("%d %B %Y", lt)

        # Quotes rotation
        if now - self._quote_last_switch > 60:
            self._quote_index = (self._quote_index + 1) % len(MYTHOS_QUOTES)
            self._quote_last_switch = now
        quote = MYTHOS_QUOTES[self._quote_index]

        # Audio visualizer spectrum bars simulation (fluctuates dynamically)
        base = [22, 48, 75, 92, 68, 48, 32, 18]
        self._audio_spectrum = [
            min(100, max(12, int(b + random.uniform(-18, 18))))
            for b in base
        ]

        # Real-time Hardware & Notification Alerts
        alerts = []
        if cpu_percent > 85:
            alerts.append({"type": "warn", "title": "HEPHAESTUS OVERHEAT", "msg": f"CPU threshold exceeded: {cpu_percent}%"})
        if ram_percent > 88:
            alerts.append({"type": "warn", "title": "CRUCIBLE SATURATED", "msg": f"RAM capacity critical: {ram_percent}% ({ram_used_gb}GB)"})
        if self._focus_active and self._focus_remaining == 0:
            alerts.append({"type": "success", "title": "VICTORY OF ARES", "msg": "Combat Focus block accomplished! Rest your mind."})

        # Focus minutes and seconds
        focus_mins = self._focus_remaining // 60
        focus_secs = self._focus_remaining % 60
        focus_display = f"{focus_mins:02d}:{focus_secs:02d}"

        return {
            "cpu": {
                "percent": cpu_percent,
                "freq_mhz": freq_mhz,
                "cores": core_count
            },
            "ram": {
                "percent": ram_percent,
                "used_gb": ram_used_gb,
                "total_gb": ram_total_gb
            },
            "disk": {
                "percent": disk_percent,
                "free_gb": disk_free_gb
            },
            "net": {
                "down_kb": down_speed_kb,
                "up_kb": up_speed_kb
            },
            "clock": {
                "time": time_str,
                "date": date_str,
                "greek_day": GREEK_DAYS[lt.tm_wday],
                "greek_month": GREEK_MONTHS[lt.tm_mon - 1],
                "moon": self.get_moon_phase(),
                "hour": lt.tm_hour
            },
            "dev": {
                "ports": self._port_cache,
                "docker": self._docker_cache,
                "git": self._git_cache
            },
            "ping": self._ping_cache,
            "top_procs": self._top_procs,
            "game_mode": self._game_mode,
            "focus": {
                "active": self._focus_active,
                "display": focus_display,
                "remaining": self._focus_remaining,
                "percent": round((1 - self._focus_remaining / self._focus_total) * 100)
            },
            "spectrum": self._audio_spectrum,
            "alerts": alerts,
            "weather": self._weather_cache,
            "quote": quote
        }
