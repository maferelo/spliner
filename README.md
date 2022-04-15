# Challenge 1: Spline Visualizing Service

Takes an image and
t, c and k parameters as inputs and draws the spline on the image

### Setup:

> pip install -r requirements.txt

### Run

> flask run

Go to http://127.0.0.1:5000/

#

this is the minimun viable product, for a bit of background in my knowledge in
design patterns and S.O.L.I.D. principles checkout this other challenge I took.

https://github.com/maferelo/prueba-python

On the steps I took:

Read the problem -> image drawing -> I used OpenCV before so decided to use it

Flask as I have 2+ years experience with it

Read some forums about how to make splines, ended up using scipy and numpy for that purpose


Started with a basic template project using the Flask official documentation

Then added the functionality for uploading images which was one of the main features.

After that, I added OpenCV and a basic functionality to draw a line and store the uploaded
image.

Finished calculating the spline points and drawing them on the image.
