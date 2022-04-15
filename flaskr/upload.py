import cv2

from os.path import join, dirname, realpath

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import request
from flask import send_from_directory
from flask import url_for

from werkzeug.utils import secure_filename

bp = Blueprint("upload", __name__)

def draw_spline(file_path):
    img = cv2.imread(file_path, 1)
    height, width, channels = img.shape
    red = (0, 0, 255)
    cv2.line(img, (height, 0), (0, width), red, 3)
    cv2.imwrite(file_path, img)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = join(dirname(realpath(__file__)), current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            draw_spline(file_path)
            return redirect(url_for('upload.download_file', name=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@bp.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(join(dirname(realpath(__file__)), current_app.config["UPLOAD_FOLDER"]), name)