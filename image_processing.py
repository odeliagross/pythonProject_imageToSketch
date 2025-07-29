import cv2
import numpy as np
from PIL import Image, ImageTk

def convert_to_sketch(img_cv, line_thickness=1):
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256.0)

    if line_thickness > 1:
        kernel = np.ones((line_thickness, line_thickness), np.uint8)
        sketch = cv2.erode(sketch, kernel, iterations=1)

    return sketch

def show_image_on_canvas(img_cv, canvas):
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil.thumbnail((400, 400))
    tk_img = ImageTk.PhotoImage(img_pil)
    canvas.image = tk_img
    canvas.create_image(0, 0, anchor='nw', image=tk_img)
