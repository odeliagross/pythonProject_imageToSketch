import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np


# פונקציה להמרת תמונה לסקיצה עם שליטה בעובי
def convert_to_sketch(img_cv, line_thickness=1):
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256.0)

    # הדגשת קווים עם עיבוי לפי הגדרת המשתמש
    if line_thickness > 1:
        kernel = np.ones((line_thickness, line_thickness), np.uint8)
        sketch = cv2.erode(sketch, kernel, iterations=1)

    return sketch


# הצגת תמונה על קנבס
def show_image_on_canvas(img_cv, canvas):
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_pil.thumbnail((300, 300))  # שינוי גודל
    tk_img = ImageTk.PhotoImage(img_pil)
    canvas.image = tk_img
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)


# פתיחת תמונה
def open_image():
    global original_img_cv, sketch_img_cv
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not file_path:
        return

    original_img_cv = cv2.imread(file_path)
    if original_img_cv is None:
        messagebox.showerror("שגיאה", "לא ניתן לפתוח את הקובץ")
        return

    show_image_on_canvas(original_img_cv, original_canvas)
    generate_sketch()


# יצירת סקיצה לפי עובי
def generate_sketch():
    global sketch_img_cv
    if original_img_cv is None:
        return
    thickness = thickness_slider.get()
    sketch = convert_to_sketch(original_img_cv, thickness)
    sketch_img_cv = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    show_image_on_canvas(sketch_img_cv, sketch_canvas)


# שמירה
def save_sketch():
    if sketch_img_cv is None:
        messagebox.showwarning("אין סקיצה", "אין מה לשמור עדיין")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*.*")])
    if save_path:
        cv2.imwrite(save_path, sketch_img_cv)
        messagebox.showinfo("הצלחה", f"הסקיצה נשמרה ב־{save_path}")


# GUI
root = tk.Tk()
root.title("ציור לסקיצה")

# כותרות
tk.Label(root, text="תמונה מקורית").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="תמונה כסקיצה").grid(row=0, column=1, padx=10, pady=5)

# קנבסים
original_canvas = tk.Canvas(root, width=300, height=300, bg="white")
original_canvas.grid(row=1, column=0, padx=10, pady=5)

sketch_canvas = tk.Canvas(root, width=300, height=300, bg="white")
sketch_canvas.grid(row=1, column=1, padx=10, pady=5)

# מחוון לעובי קו
tk.Label(root, text="עובי קו:").grid(row=2, column=0)
thickness_slider = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, command=lambda e: generate_sketch())
thickness_slider.set(1)
thickness_slider.grid(row=2, column=1)

# כפתורים
tk.Button(root, text="בחר תמונה", command=open_image).grid(row=3, column=0, pady=10)
tk.Button(root, text="שמור סקיצה", command=save_sketch).grid(row=3, column=1, pady=10)

# משתנים גלובליים
original_img_cv = None
sketch_img_cv = None

root.mainloop()
