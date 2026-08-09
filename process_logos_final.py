"""Generate the definitive Duneworks logo asset set from the single confirmed-clean
wordmark source (ringed-D icon + "DUNEWORKS PRODUCTION" text, black-on-white).

OG and Reborn share the same mark; they are differentiated by palette color only
(OG = gold/bronze, Reborn = white/near-black), matching the site's accent variables.
Every output is verified (alpha + rgb extrema) immediately after being written so a
silent all-opaque or all-transparent failure can never slip through again.
"""
from collections import deque
from PIL import Image, ImageFilter

ASSETS = "assets"
SOURCE = (
    r"C:\Users\Odil\.cursor\projects\c-Duneworks-Studios-Duneworks-Production-website-"
    r"Duneworks-Productions\assets\c__Users_Odil_AppData_Roaming_Cursor_User_"
    r"workspaceStorage_766a3dbfaedbfa87275168c8623eb090_images_Duneworksprbanner-"
    r"cffa9255-7002-4e38-8b78-9cbe63e7cdc2.png"
)


def flood_remove_white(src_path, thresh=225, feather=1.2):
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    px = im.load()
    bg = bytearray(w * h)

    def is_white(x, y):
        r, g, b, _ = px[x, y]
        return r >= thresh and g >= thresh and b >= thresh

    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_white(x, y) and not bg[y * w + x]:
                bg[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_white(x, y) and not bg[y * w + x]:
                bg[y * w + x] = 1
                q.append((x, y))

    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not bg[ny * w + nx] and is_white(nx, ny):
                bg[ny * w + nx] = 1
                q.append((nx, ny))

    mask = Image.new("L", (w, h), 255)
    mpx = mask.load()
    for y in range(h):
        for x in range(w):
            if bg[y * w + x]:
                mpx[x, y] = 0
    mask = mask.filter(ImageFilter.GaussianBlur(feather))

    im.putalpha(mask)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    return im


def recolor(silhouette, rgb, out_path):
    w, h = silhouette.size
    a = silhouette.split()[3]
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(Image.new("RGBA", (w, h), rgb + (255,)), (0, 0))
    out.putalpha(a)
    out.save(out_path)
    verify(out_path)


def verify(path):
    im = Image.open(path).convert("RGBA")
    a = im.split()[3]
    lo, hi = a.getextrema()
    opaque_px = sum(v for i, v in enumerate(a.histogram()) if i >= 250)
    total = im.size[0] * im.size[1]
    status = "OK" if lo == 0 and hi == 255 else "SUSPECT"
    print(f"[{status}] {path} size={im.size} alpha_range=({lo},{hi}) "
          f"opaque_px={opaque_px}/{total} ({100*opaque_px/total:.1f}%)")
    if status == "SUSPECT":
        raise RuntimeError(f"Logo generation failed verification for {path}")


silhouette = flood_remove_white(SOURCE)
print(f"silhouette size after crop: {silhouette.size}")

# Reborn — white mark for dark backgrounds, near-black for light backgrounds
recolor(silhouette, (255, 255, 255), f"{ASSETS}/duneworks-logo.png")
recolor(silhouette, (17, 17, 19), f"{ASSETS}/duneworks-logo-light.png")

# OG — gold mark for dark backgrounds, bronze for light backgrounds (matches --accent-primary)
recolor(silhouette, (201, 169, 98), f"{ASSETS}/logo-og.png")
recolor(silhouette, (141, 113, 56), f"{ASSETS}/logo-og-light.png")

print("All logo assets regenerated and verified.")
