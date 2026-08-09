"""Remove black background from the new Duneworks logo and create a light variant."""
from PIL import Image

SRC = r"C:\Users\Odil\.cursor\projects\c-Duneworks-Studios-Duneworks-Production-website-Duneworks-Productions\assets\c__Users_Odil_AppData_Roaming_Cursor_User_workspaceStorage_766a3dbfaedbfa87275168c8623eb090_images_Duneworksprbanner-Photoroom-489a4987-3bea-44ca-964b-cd8b0a6a23c6.png"

src = Image.open(SRC).convert("RGBA")
px = src.load()
w, h = src.size

dark = Image.new("RGBA", (w, h), (0, 0, 0, 0))
light = Image.new("RGBA", (w, h), (0, 0, 0, 0))
dpx = dark.load()
lpx = light.load()

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
    dark = dark.crop(bbox)
    light = light.crop(bbox)

dark.save("assets/duneworks-logo.png")
light.save("assets/duneworks-logo-light.png")
print("saved", dark.size)
