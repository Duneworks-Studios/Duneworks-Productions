"""Process partner logos (flood-fill black bg removal) + regenerate OG logo."""
from collections import deque
from PIL import Image, ImageFilter

BASE = r"C:\Users\Odil\.cursor\projects\c-Duneworks-Studios-Duneworks-Production-website-Duneworks-Productions\assets"

def flood_remove(src_path, out_path, thresh=30):
    im = Image.open(src_path).convert("RGBA")
    w, h = im.size
    px = im.load()
    bg = bytearray(w * h)  # 1 = background

    def is_black(x, y):
        r, g, b, a = px[x, y]
        return r < thresh and g < thresh and b < thresh

    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_black(x, y) and not bg[y * w + x]:
                bg[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_black(x, y) and not bg[y * w + x]:
                bg[y * w + x] = 1
                q.append((x, y))

    while q:
        x, y = q.popleft()
        for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0 <= nx < w and 0 <= ny < h and not bg[ny * w + nx] and is_black(nx, ny):
                bg[ny * w + nx] = 1
                q.append((nx, ny))

    mask = Image.new("L", (w, h), 255)
    mpx = mask.load()
    for y in range(h):
        for x in range(w):
            if bg[y * w + x]:
                mpx[x, y] = 0
    mask = mask.filter(ImageFilter.GaussianBlur(1.2))

    im.putalpha(mask)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    im.save(out_path)
    print("saved", out_path, im.size)


def luma_remove(src_path, out_dark, out_light):
    src = Image.open(src_path).convert("RGBA")
    px = src.load()
    w, h = src.size
    dark = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    light = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dpx, lpx = dark.load(), light.load()
    LOW, HIGH = 12, 64
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            luma = (r * 299 + g * 587 + b * 114) // 1000
            if luma <= LOW:
                alpha = 0
            elif luma >= HIGH:
                alpha = 255
            else:
                alpha = int(255 * (luma - LOW) / (HIGH - LOW))
            alpha = alpha * a // 255
            dpx[x, y] = (r, g, b, alpha)
            if r > 150 and g > 150 and b > 150:
                shade = max(0, min(60, 255 - luma))
                lpx[x, y] = (shade, shade, shade + 2, alpha)
            else:
                lpx[x, y] = (r, g, b, alpha)
    bbox = dark.getbbox()
    if bbox:
        dark, light = dark.crop(bbox), light.crop(bbox)
    dark.save(out_dark)
    light.save(out_light)
    print("saved", out_dark, dark.size)


flood_remove(BASE + r"\c__Users_Odil_AppData_Roaming_Cursor_User_workspaceStorage_766a3dbfaedbfa87275168c8623eb090_images_aaxyeypxd-Photoroom__1_-c6e4ff77-8c8b-4992-bffd-95cd40690893.png",
             "assets/partner-overcut.png")
flood_remove(BASE + r"\c__Users_Odil_AppData_Roaming_Cursor_User_workspaceStorage_766a3dbfaedbfa87275168c8623eb090_images_ChatGPT_Image_Aug_10__2026__01_21_31_AM-f74bb30c-b3df-48c7-bdea-34dc38262b6d.png",
             "assets/partner-montana.png")
luma_remove(BASE + r"\c__Users_Odil_AppData_Roaming_Cursor_User_workspaceStorage_766a3dbfaedbfa87275168c8623eb090_images_Duneworksprbanner-cffa9255-7002-4e38-8b78-9cbe63e7cdc2.png",
            "assets/logo-og.png", "assets/logo-og-light.png")
