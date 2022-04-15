import cv2
import numpy as np

from os.path import join, dirname, realpath

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import request
from flask import send_from_directory
from flask import url_for

from scipy import interpolate
from werkzeug.utils import secure_filename

bp = Blueprint("upload", __name__)

t = [0,0,0,0,1,1,1,1]
c = [[58.3863029989894,116.89745219181054],[105.31685340513181,38.956713078315055],[310.3370211379565,22.44508241175887],[369.9147409302334,111.62765304361334]]
c_int = np.array(c)
k = 3

def draw_spline(file_path):
    img = cv2.imread(file_path, 1)
    height, width, channels = img.shape

    x_range = np.arange(width)
    x_range_new = np.arange(width)
    y_range = interpolate.splev(x_range_new, (t, c, k), der=0)

    print(len(y_range))
    red = (0, 0, 255)

    draw_points = (np.asarray([c_int[:,0], c_int[:,1]]).T).astype(np.int32)
    cv2.polylines(img, [draw_points], False, (0,0,0))  # args: image, points, closed, color

    for n in range(len(y_range)):
        draw_points = (np.asarray([x_range, y_range[n]]).T).astype(np.int32)   # needs to be int32 and transposed
        cv2.polylines(img, [draw_points], False, (0,0,0))  # args: image, points, closed, color

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
      <input type=text value=Param>
    </form>
    '''

@bp.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(join(dirname(realpath(__file__)), current_app.config["UPLOAD_FOLDER"]), name)