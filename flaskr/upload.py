import cv2
import numpy as np

from os.path import join, dirname, realpath

from flask import Blueprint
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import url_for

from scipy import interpolate
from werkzeug.utils import secure_filename

bp = Blueprint("upload", __name__)


red = (0, 0, 255)
t = [0,0,0,0,1,1,1,1]
c = np.array([[54.740454740454695,49.511797511797425],[164.71214071214064,153.00900900900905],[340.7498927498925,145.13770913770907],[441.2835692835691,34.392106392106385]])
k = 3

def spline(t, c, k):
    shape = c.shape[0]
    u  = np.linspace(0, shape - k, 100)
    points = np.array(interpolate.splev(u, (t, c.T, k))).T.astype(np.int32)
    x_range = points[:,0]
    y_range = points[:,1] 
    return (np.asarray([x_range, y_range]).T) 

def draw_spline(file_path, points):
    img = cv2.imread(file_path, 1)
    cv2.polylines(img, [points], False, (0,0,0))
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
        t_form = request.form["t"]

        try:
            t_form = np.array(t_form.split(",")).astype(np.int32)
        except ValueError:
            flash('Not a valid t')
            return redirect(request.url)

        c_form = request.form["c"]
        try:
            pairs = np.array(c_form.split(",")).astype(np.float)
            pairs = pairs.reshape(-1,2)
            c_form = pairs
        except Exception:
            flash('Not a valid c')
            return redirect(request.url)

        k_form = request.form["k"]
        try:
            k_form = int(k_form)
        except ValueError:
            flash('Not a valid k')
            return redirect(request.url)

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = join(dirname(realpath(__file__)), current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            points = spline(t_form, c_form, k_form)
            draw_spline(file_path, points)
            return redirect(url_for('upload.download_file', name=filename))
    return render_template("uploads/uploads.html")

@bp.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(join(dirname(realpath(__file__)), current_app.config["UPLOAD_FOLDER"]), name)