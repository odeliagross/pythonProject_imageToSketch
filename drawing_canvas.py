import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

class DrawingCanvas(tk.Canvas):
    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height, bg='white')
        self.bind("<B1-Motion>", self.draw)
        self.bind("<ButtonPress-1>", self.start_draw)
        self.old_x = self.old_y = None
        self.line_width = 3
        self.image = Image.new("RGB", (width, height), "white")
        self.draw_img = ImageDraw.Draw(self.image)

    def set_line_width(self, width):
        self.line_width = width

    def start_draw(self, event):
        self.old_x, self.old_y = event.x, event.y

    def draw(self, event):
        if self.old_x and self.old_y:
            self.create_line(self.old_x, self.old_y, event.x, event.y,
                             width=self.line_width, fill='black', capstyle=tk.ROUND)
            self.draw_img.line([self.old_x, self.old_y, event.x, event.y],
                               fill='black', width=self.line_width)
        self.old_x, self.old_y = event.x, event.y

    def clear(self):
        self.delete("all")
        self.image = Image.new("RGB", self.image.size, "white")
        self.draw_img = ImageDraw.Draw(self.image)

    def get_image(self):
        return self.image
