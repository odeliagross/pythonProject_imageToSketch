from flask import Flask, request, render_template, redirect, url_for
import os
import cv2
from utils import process_image  # פונקציית עיבוד התמונה שלך
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
SKETCH_FOLDER = 'static'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SKETCH_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SKETCH_FOLDER'] = SKETCH_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "לא נבחר קובץ", 400
        file = request.files['file']
        if file.filename == '':
            return "לא נבחר קובץ", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            img = cv2.imread(filepath)
            if img is None:
                return "טעינת התמונה נכשלה", 400

            sketch = process_image(img)

            sketch_path = os.path.join(app.config['SKETCH_FOLDER'], 'sketch_' + filename)
            cv2.imwrite(sketch_path, sketch)

            return redirect(url_for('show_sketch', filename='sketch_' + filename))
    return render_template('upload.html')

@app.route('/sketch/<filename>')
def show_sketch(filename):
    return render_template('show_sketch.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
