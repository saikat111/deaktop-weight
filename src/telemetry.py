import time
import math
import psutil
import requests
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
    {"author": "Homer", "quote": "Even his griefs are a joy long after to one that remembers all that he wrought and endured."},
    {"author": "Pythagoras", "quote": "Do not say a little in many words, but a great deal in a few."},
    {"author": "Zeno of Citium", "quote": "Well-being is realized by small steps, but is no small thing itself."}
]

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
        self._weather_last_fetch = 0
        self._quote_index = 0
        self._quote_last_switch = time.time()

        # Start background weather fetch thread
        threading.Thread(target=self._update_weather_loop, daemon=True).start()

    def _update_weather_loop(self):
        while True:
            try:
                # Fetch public location & weather via ip-api and Open-Meteo (no API key required)
                r_loc = requests.get("http://ip-api.com/json/", timeout=5).json()
                lat = r_loc.get("lat", 37.9838) # Default Athens / Olympus
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
            time.sleep(900) # update every 15 mins

    def get_moon_phase(self):
        # Calculate moon phase (0 to 1 scale)
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

        # CPU
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
            disk_total_gb = round(disk.total / (1024**3), 1)
        except Exception:
            disk_percent = 50
            disk_free_gb = 100
            disk_total_gb = 500

        # Network
        net = psutil.net_io_counters()
        bytes_recv = max(net.bytes_recv - self._last_net.bytes_recv, 0)
        bytes_sent = max(net.bytes_sent - self._last_net.bytes_sent, 0)
        down_speed_kb = round(bytes_recv / dt / 1024, 1)
        up_speed_kb = round(bytes_sent / dt / 1024, 1)

        self._last_net = net
        self._last_time = now

        # Time & Dates
        lt = time.localtime(now)
        time_str = time.strftime("%H:%M:%S", lt)
        time_12h = time.strftime("%I:%M:%S %p", lt)
        date_str = time.strftime("%d %B %Y", lt)
        weekday_greek = GREEK_DAYS[lt.tm_wday]
        month_greek = GREEK_MONTHS[lt.tm_mon - 1]

        # Quotes rotation (every 60s)
        if now - self._quote_last_switch > 60:
            self._quote_index = (self._quote_index + 1) % len(MYTHOS_QUOTES)
            self._quote_last_switch = now

        quote = MYTHOS_QUOTES[self._quote_index]

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
                "free_gb": disk_free_gb,
                "total_gb": disk_total_gb
            },
            "net": {
                "down_kb": down_speed_kb,
                "up_kb": up_speed_kb
            },
            "clock": {
                "time": time_str,
                "time_12h": time_12h,
                "date": date_str,
                "greek_day": weekday_greek,
                "greek_month": month_greek,
                "moon": self.get_moon_phase(),
                "hour": lt.tm_hour,
                "min": lt.tm_min,
                "sec": lt.tm_sec
            },
            "weather": self._weather_cache,
            "quote": quote
        }
