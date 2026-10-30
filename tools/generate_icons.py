"""Generate PowerForge launcher icons, splash and Play Store assets from the site's 'PF' favicon design."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "app/src/main/res"
DARK, RED = (15, 15, 15, 255), (230, 57, 70, 255)
FONT = "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"


def draw_pf(size, text_ratio, bg=DARK, circle=False, transparent=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0) if (circle or transparent) else bg)
    d = ImageDraw.Draw(img)
    if circle:
        d.ellipse((0, 0, size - 1, size - 1), fill=bg)
    font = ImageFont.truetype(FONT, int(size * text_ratio))
    d.text((size / 2, size / 2), "PF", font=font, fill=RED, anchor="mm")
    return img


densities = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}
for name, f in densities.items():
    out = RES / f"mipmap-{name}"
    out.mkdir(parents=True, exist_ok=True)
    s = int(48 * f)
    draw_pf(s, 0.42).save(out / "ic_launcher.png")                   # legacy square
    draw_pf(s, 0.42, circle=True).save(out / "ic_launcher_round.png")  # legacy round
    fg = int(108 * f)                                                  # adaptive foreground (safe zone 66dp)
    draw_pf(fg, 0.26, transparent=True).save(out / "ic_launcher_foreground.png")

(RES / "drawable").mkdir(parents=True, exist_ok=True)
draw_pf(512, 0.42, circle=True).save(RES / "drawable/splash.png")

store = ROOT / "store-assets"
store.mkdir(exist_ok=True)
draw_pf(512, 0.42).convert("RGB").save(store / "play_store_icon_512.png")  # Play: 512x512 32-bit PNG, full-bleed

# Feature graphic 1024x500 (required by Play)
fg = Image.new("RGB", (1024, 500), DARK[:3])
d = ImageDraw.Draw(fg)
fg.paste(draw_pf(300, 0.42, circle=True, bg=(30, 30, 30, 255)), (80, 100), draw_pf(300, 0.42, circle=True, bg=(30, 30, 30, 255)))
d.text((430, 200), "PowerForge", font=ImageFont.truetype(FONT, 84), fill=(255, 255, 255), anchor="lm")
d.text((432, 290), "Beginner powerlifting programmes", font=ImageFont.truetype(FONT, 34), fill=RED[:3], anchor="lm")
fg.save(store / "feature_graphic_1024x500.png")
print("icons generated")
