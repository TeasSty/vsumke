from PIL import Image, ImageDraw
import os

out = r"C:\Users\popoo\Desktop\в сумке\assets"
os.makedirs(out, exist_ok=True)

vk1 = Image.open(
    r"C:\Users\popoo\.cursor\projects\c-Users-popoo-Desktop\assets\c__Users_popoo_AppData_Roaming_Cursor_User_workspaceStorage_7d4c3781885e4e0a9deb83cc09f89bc9_images_image-806ffb0b-0826-45a3-8adc-98d547c49459.png"
).convert("RGB")
vk2 = Image.open(
    r"C:\Users\popoo\.cursor\projects\c-Users-popoo-Desktop\assets\c__Users_popoo_AppData_Roaming_Cursor_User_workspaceStorage_7d4c3781885e4e0a9deb83cc09f89bc9_images_image-22eb1a1e-820b-4c04-9a08-48cd33ba9452.png"
).convert("RGB")


def save(im, name):
    path = os.path.join(out, name)
    if name.endswith(".png"):
        im.save(path)
    else:
        im.save(path, quality=94, optimize=True)
    print(name, im.size)


def upscale(im, factor=3):
    return im.resize((im.size[0] * factor, im.size[1] * factor), Image.Resampling.LANCZOS)


# Banner
save(upscale(vk1.crop((0, 0, 660, 195)), 2), "banner.jpg")

# Logo circle
logo = vk1.crop((20, 165, 106, 251))
mask = Image.new("L", logo.size, 0)
ImageDraw.Draw(mask).ellipse((0, 0, logo.size[0] - 1, logo.size[1] - 1), fill=255)
logo_rgba = logo.convert("RGBA")
logo_rgba.putalpha(mask)
save(upscale(logo_rgba, 2), "logo.png")

# Lifestyle photos (photo area only)
floral = vk1.crop((298, 518, 562, 778))
grey = vk1.crop((22, 518, 288, 778))
save(upscale(floral, 3), "hero.jpg")
save(upscale(grey, 3), "visit-model.jpg")
save(upscale(floral, 3), "model-floral-bag.jpg")
save(upscale(grey, 3), "model-grey-bag.jpg")

# 3x3 product grid
grid = vk2.crop((16, 168, 454, 606))
save(grid, "catalog-grid.jpg")

gw, gh = grid.size
cell_w = gw // 3
cell_h = gh // 3
gap = 3

names = [
    "p1-fringe-dark",
    "p2-shoulder-brown",
    "p3-olive-logo",
    "p4-fringe-tan",
    "p5-hobo-brown",
    "p6-black-logo",
    "p7-fringe-bucket",
    "p8-cylinder",
    "p9-brown-logo",
]

for i, name in enumerate(names):
    row, col = divmod(i, 3)
    x0 = col * cell_w + gap
    y0 = row * cell_h + gap
    x1 = (col + 1) * cell_w - gap
    y1 = (row + 1) * cell_h - gap
    cell = upscale(grid.crop((x0, y0, x1, y1)), 3)
    save(cell, f"{name}.jpg")

# Cleanup temp/debug files
for junk in [
    "_grid_mockup.png",
    "_grid_vk1.png",
    "_grid_vk2.png",
    "_grid_area.jpg",
    "_grid_area2.jpg",
    "hero-from-mock.jpg",
    "product-1.jpg",
    "product-2.jpg",
    "product-3.jpg",
    "product-4.jpg",
    "visit-left.jpg",
    "visit-store.jpg",
    "logo-raw.jpg",
    "mock-hero.jpg",
    "mock-prod-1.jpg",
    "mock-prod-2.jpg",
    "mock-prod-3.jpg",
    "mock-prod-4.jpg",
    "mock-store-left.jpg",
    "mock-store-right.jpg",
]:
    p = os.path.join(out, junk)
    if os.path.exists(p):
        os.remove(p)
        print("removed", junk)

print("done")
