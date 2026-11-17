import os
import math
import random
import ctypes
from PIL import Image, ImageDraw, ImageFilter

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

PALETTES = {
    "elysium_cyan": {
        "bg_top": (8, 11, 16),
        "bg_bottom": (4, 6, 9),
        "primary": (0, 240, 255),
        "secondary": (0, 140, 255),
        "accent": (125, 249, 255),
        "circuit": (0, 240, 255, 60)
    },
    "tartarus_crimson": {
        "bg_top": (16, 8, 10),
        "bg_bottom": (8, 4, 5),
        "primary": (255, 42, 95),
        "secondary": (255, 90, 90),
        "accent": (255, 120, 150),
        "circuit": (255, 42, 95, 60)
    },
    "hades_violet": {
        "bg_top": (14, 8, 18),
        "bg_bottom": (6, 3, 9),
        "primary": (168, 85, 247),
        "secondary": (192, 132, 252),
        "accent": (216, 180, 254),
        "circuit": (168, 85, 247, 60)
    },
    "spartan_silver": {
        "bg_top": (15, 18, 23),
        "bg_bottom": (8, 10, 14),
        "primary": (56, 189, 248),
        "secondary": (226, 232, 240),
        "accent": (248, 250, 252),
        "circuit": (226, 232, 240, 50)
    }
}

def draw_greek_meander(draw, x1, y1, length, step, color):
    """Draws a classical Greek Meander (Key) fret line."""
    x = x1
    y = y1
    while x < x1 + length:
        # Fret pattern
        draw.line([(x, y), (x + step, y)], fill=color, width=2)
        draw.line([(x + step, y), (x + step, y + step)], fill=color, width=2)
        draw.line([(x + step, y + step), (x + step * 0.4, y + step)], fill=color, width=2)
        draw.line([(x + step * 0.4, y + step), (x + step * 0.4, y + step * 0.4)], fill=color, width=2)
        draw.line([(x + step * 0.4, y + step * 0.4), (x + step * 0.7, y + step * 0.4)], fill=color, width=2)
        x += step * 1.5

def generate_mythos_wallpaper(theme_name="elysium_cyan", width=1920, height=1080):
    palette = PALETTES.get(theme_name, PALETTES["elysium_cyan"])
    img = Image.new("RGB", (width, height), palette["bg_top"])
    draw = ImageDraw.Draw(img)

    # 1. Subtle Radial Gradient Vignette
    for y in range(height):
        ratio = y / height
        r = int(palette["bg_top"][0] * (1 - ratio) + palette["bg_bottom"][0] * ratio)
        g = int(palette["bg_top"][1] * (1 - ratio) + palette["bg_bottom"][1] * ratio)
        b = int(palette["bg_top"][2] * (1 - ratio) + palette["bg_bottom"][2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 2. Geometric Constellation & Cyber-Mesh
    random.seed(42) # Consistent divine geometry
    points = [(random.randint(100, width - 100), random.randint(100, height - 100)) for _ in range(35)]
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ol_draw = ImageDraw.Draw(overlay)

    # Connect nearby constellation points
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1, p2 = points[i], points[j]
            dist = math.hypot(p1[0] - p2[0], p1[1] - p2[1])
            if dist < 220:
                alpha = int(max(0, (1 - dist / 220) * 45))
                c = palette["primary"] + (alpha,)
                ol_draw.line([p1, p2], fill=c, width=1)

    for p in points:
        ol_draw.ellipse([p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2], fill=palette["accent"] + (90,))

    # 3. Center Cyber-Hellenic Sigil (Hexagonal Astrolabe)
    cx, cy = width // 2, height // 2
    for r in [280, 240, 180, 120]:
        ol_draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=palette["primary"] + (35,), width=1)

    # Concentric Runes & Ray Lines
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x_outer = cx + int(math.cos(rad) * 280)
        y_outer = cy + int(math.sin(rad) * 280)
        x_inner = cx + int(math.cos(rad) * 240)
        y_inner = cy + int(math.sin(rad) * 240)
        ol_draw.line([(x_inner, y_inner), (x_outer, y_outer)], fill=palette["accent"] + (60,), width=2)

    # Greek Key Fret Borders Top & Bottom
    draw_greek_meander(ol_draw, 100, 40, width - 200, 20, palette["primary"] + (50,))
    draw_greek_meander(ol_draw, 100, height - 50, width - 200, 20, palette["primary"] + (50,))

    # Blend and save
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    
    # Save to wallpapers dir
    wallpapers_dir = os.path.join(os.path.dirname(__file__), "assets", "wallpapers")
    os.makedirs(wallpapers_dir, exist_ok=True)
    out_path = os.path.join(wallpapers_dir, f"mythos_{theme_name}.png")
    img.save(out_path, "PNG")
    return out_path

def apply_windows_wallpaper(image_path):
    """Sets the active Windows desktop wallpaper immediately using Win32 API."""
    try:
        abs_path = os.path.abspath(image_path)
        res = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            abs_path,
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
        return bool(res)
    except Exception as e:
        print(f"Failed to set wallpaper: {e}")
        return False

def set_theme_wallpaper(theme_name):
    """Generates and sets the matching Cyber-Hellenic wallpaper on Windows."""
    wallpapers_dir = os.path.join(os.path.dirname(__file__), "assets", "wallpapers")
    target_file = os.path.join(wallpapers_dir, f"mythos_{theme_name}.png")
    if not os.path.exists(target_file):
        target_file = generate_mythos_wallpaper(theme_name)
    return apply_windows_wallpaper(target_file)

def set_custom_wallpaper(image_path):
    """Applies an arbitrary custom user image as the desktop wallpaper."""
    if not image_path or not os.path.exists(image_path):
        return False
    return apply_windows_wallpaper(image_path)

if __name__ == "__main__":
    path = generate_mythos_wallpaper("elysium_cyan")
    print(f"Generated: {path}")
