import matplotlib.pyplot as plt
import numpy as np

def plot_sketch_histogram(sketch_img):
    import cv2
    gray = cv2.cvtColor(sketch_img, cv2.COLOR_BGR2GRAY)
    fig, ax = plt.subplots(figsize=(5,3))
    ax.hist(gray.ravel(), bins=256, range=(0,256), color='black')
    ax.set_title("Sketch Shades Histogram")
    ax.set_xlabel("Shade (0=Black, 255=White)")
    ax.set_ylabel("Pixels Count")
    plt.tight_layout()
    return fig

def plot_creation_progress(timestamps):
    fig, ax = plt.subplots(figsize=(5,3))
    if len(timestamps)<2:
        ax.plot([0,1], [0,1], 'r--')
        ax.set_title("Creation Progress (Sample)")
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Progress (%)")
        return fig

    times = np.array(timestamps) - timestamps[0]
    progress = np.linspace(0, 100, len(timestamps))
    ax.plot(times, progress, marker='o')
    ax.set_title("Creation Progress Over Time")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Progress (%)")
    ax.grid(True)
    plt.tight_layout()
    return fig

def plot_quality_vs_thickness(data):
    fig, ax = plt.subplots(figsize=(5,3))
    ax.scatter(data['Thickness'], data['Quality'], c='blue')
    ax.set_title("Quality vs. Line Thickness")
    ax.set_xlabel("Line Thickness")
    ax.set_ylabel("Quality Score")
    ax.grid(True)
    plt.tight_layout()
    return fig
