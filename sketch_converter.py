import cv2
import numpy as np
from pathlib import Path


def preprocess_image(image_path: str):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"תמונה לא נמצאה: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 50, 150)
    return img, edged


def vectorize_edges(edged):
    # מוצא קונטורים (קווים/צורות) לפי הגבולות
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def draw_vectorized(image, contours):
    output = np.ones_like(image) * 255  # רקע לבן
    cv2.drawContours(output, contours, -1, (0, 0, 0), 1)  # קווים שחורים
    return output


def main(image_path: str, output_path: str = "output.png"):
    original, edged = preprocess_image(image_path)
    contours = vectorize_edges(edged)
    sketch = draw_vectorized(original, contours)
    cv2.imwrite(output_path, sketch)
    print(f"שירטוט נשמר כ־{output_path}")


if __name__ == "__main__":
    input_file = "my_drawing.jpg"  # שימי כאן את שם הקובץ שלך
    output_file = "clean_sketch.png"
    main(input_file, output_file)
