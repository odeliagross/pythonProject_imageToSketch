import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from image_processing import convert_to_sketch, show_image_on_canvas
from analysis import plot_sketch_histogram, plot_creation_progress, plot_quality_vs_thickness
from data import get_sample_data
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time


class SketchApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Drawing to Sketch & Analysis")
        self.state('zoomed')
        self.minsize(800, 600)

        self.main_canvas = tk.Canvas(self)
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.main_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.main_canvas.configure(yscrollcommand=scrollbar.set)
        self.main_canvas.bind('<Configure>', lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))

        self.container = tk.Frame(self.main_canvas)
        self.main_canvas.create_window((0, 0), window=self.container, anchor='nw')

        self.original_img_cv = None
        self.sketch_img_cv = None
        self.creation_times = []

        self.df_stats = get_sample_data()

        self.frames = {}
        for F in (DrawingFrame, GraphsFrame, TableFrame):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("DrawingFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class DrawingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Original Image").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self, text="Sketch Image").grid(row=0, column=1, padx=10, pady=5)

        self.original_canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.original_canvas.grid(row=1, column=0, padx=10, pady=5)
        self.sketch_canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.sketch_canvas.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="Line Thickness:").grid(row=2, column=0)
        self.thickness_slider = tk.Scale(self, from_=1, to=10, orient=tk.HORIZONTAL, command=self.generate_sketch)
        self.thickness_slider.set(1)
        self.thickness_slider.grid(row=2, column=1)

        btn_load = tk.Button(self, text="Load Image & Show Sketch", command=self.open_image)
        btn_load.grid(row=3, column=0, pady=10)
        btn_save = tk.Button(self, text="Save Sketch", command=self.save_sketch)
        btn_save.grid(row=3, column=1, pady=10)

        btn_to_graphs = tk.Button(self, text="Go to Graphs", command=lambda: controller.show_frame("GraphsFrame"))
        btn_to_graphs.grid(row=4, column=0, pady=10)
        btn_to_table = tk.Button(self, text="Go to Table", command=lambda: controller.show_frame("TableFrame"))
        btn_to_table.grid(row=4, column=1, pady=10)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return
        self.controller.original_img_cv = cv2.imread(file_path)
        if self.controller.original_img_cv is None:
            messagebox.showerror("Error", "Cannot open this file.")
            return

        start_time = time.time()

        show_image_on_canvas(self.controller.original_img_cv, self.original_canvas)
        self.generate_sketch()

        end_time = time.time()
        self.controller.creation_times.append(end_time - start_time)

    def generate_sketch(self, event=None):
        if self.controller.original_img_cv is None:
            return
        thickness = self.thickness_slider.get()
        sketch = convert_to_sketch(self.controller.original_img_cv, thickness)
        self.controller.sketch_img_cv = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
        show_image_on_canvas(self.controller.sketch_img_cv, self.sketch_canvas)

    def save_sketch(self):
        if self.controller.sketch_img_cv is None:
            messagebox.showwarning("Warning", "No sketch to save yet.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")])
        if save_path:
            # שמירת תמונה באמצעות OpenCV
            cv2.imwrite(save_path, self.controller.sketch_img_cv)
            messagebox.showinfo("Success", f"Sketch saved to {save_path}")


class GraphsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Graphs and Analysis", font=("Arial", 14)).pack(pady=5)

        btn_back = tk.Button(self, text="Back to Drawing", command=lambda: controller.show_frame("DrawingFrame"))
        btn_back.pack(pady=5)

        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack()

        btn_refresh = tk.Button(self, text="Refresh Graphs", command=self.update_graphs)
        btn_refresh.pack(pady=5)

        self.fig_hist = None
        self.canvas_hist = None

        self.fig_prog = None
        self.canvas_prog = None

        self.fig_quality = None
        self.canvas_quality = None

    def update_graphs(self):
        for canvas in (self.canvas_hist, self.canvas_prog, self.canvas_quality):
            if canvas:
                canvas.get_tk_widget().destroy()

        if self.controller.sketch_img_cv is not None:
            self.fig_hist = plot_sketch_histogram(self.controller.sketch_img_cv)
            self.canvas_hist = FigureCanvasTkAgg(self.fig_hist, master=self.graph_frame)
            self.canvas_hist.draw()
            self.canvas_hist.get_tk_widget().pack(side=tk.LEFT, padx=5)

        if self.controller.creation_times:
            self.fig_prog = plot_creation_progress(self.controller.creation_times)
            self.canvas_prog = FigureCanvasTkAgg(self.fig_prog, master=self.graph_frame)
            self.canvas_prog.draw()
            self.canvas_prog.get_tk_widget().pack(side=tk.LEFT, padx=5)

        self.fig_quality = plot_quality_vs_thickness(self.controller.df_stats)
        self.canvas_quality = FigureCanvasTkAgg(self.fig_quality, master=self.graph_frame)
        self.canvas_quality.draw()
        self.canvas_quality.get_tk_widget().pack(side=tk.LEFT, padx=5)


class TableFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Statistics Table", font=("Arial", 14)).pack(pady=5)

        btn_back = tk.Button(self, text="Back to Drawing", command=lambda: controller.show_frame("DrawingFrame"))
        btn_back.pack(pady=5)

        columns = ('Thickness', 'Quality', 'Upload Date', 'Creation Date')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        self.tree.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor='center')

        for _, row in self.controller.df_stats.iterrows():
            self.tree.insert('', tk.END, values=(row['Thickness'], row['Quality'],
                                                 row['Upload Date'].strftime('%Y-%m-%d'),
                                                 row['Creation Date'].strftime('%Y-%m-%d')))


if __name__ == "__main__":
    app = SketchApp()
    app.mainloop()
