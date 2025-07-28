import cv2
import numpy as np

def process_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=10)
    sketch = 255 * np.ones_like(img)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(sketch, (x1, y1), (x2, y2), (0, 0, 0), 2)

    return sketch

def analyze_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"בהירות ממוצעת: {np.mean(gray):.2f}")
    print(f"סטיית תקן: {np.std(gray):.2f}")
