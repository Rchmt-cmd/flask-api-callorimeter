from pydoc import resolve
import pandas as pd
import numpy as np
import pickle
from PIL import Image
from base64 import encodebytes
import cv2
import os
from KaloriMeter import KaloriMeter
from segment import Segment
import argparse
import sys
from flask_cors import cross_origin, CORS
from keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app)

UPLOAD_FOLDER = 'static/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
@cross_origin()

def index():
    if request.method == "GET":
        response = jsonify(message="Simple server is running")

        # Enable Access-Control-Allow-Origin
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    elif request.method == "POST":
        if 'images[]' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
            
        images = request.files.getlist('images[]')
        errors = {}
        success = False
        
        image_file = {}
        for image in images:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                success = True
                image_file[image.filename] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            else:
                errors[image.filename] = 'File type is not allowed'

        # image processing

        


        if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
        if success:
            resp = jsonify({'message' : 'Files successfully uploaded'})
            resp.status_code = 201
            return resp
        else:
            resp = jsonify(errors)
            resp.status_code = 500
            return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")




# single image
        # image = request.files["image"]
        # filename = secure_filename(image.filename)
        # image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # image_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # # load image
        # image=cv2.imread(image_path)

        # # load segment class
        # seg = Segment()

        # # segment image
        # label,result= seg.kmeans(image)

        # # set response value
        # retval, buffer = cv2.imencode('.png', result)
        # response = make_response(buffer.tobytes())
        # response.headers['Content-Type'] = 'image/png'
        # return response





# multiple image
# images = request.files.getlist('images[]')
#         for image in images:
#             if image and allowed_file(image.filename):
#                 filename = secure_filename(image.filename)
#                 segmented_images.append(filename)
#                 image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#                 image_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
#                 image=cv2.imread(image_path)
#                 seg = Segment()
#                 # segment image
#                 label,result= seg.kmeans(image)

#                 segmented_images.append(image)

#                 set response value
#         for segmented_image in segmented_images:
#             retval, buffer = cv2.imencode('.png', segmented_image)
#             response = make_response(buffer.tobytes())
#             response.headers['Content-Type'] = 'image/png'
#         return jsonify(segmented_images)



# updated single image
# image = request.files["image"]
#         filename = secure_filename(image.filename)
#         image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         image_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)

#         # load image
#         image=cv2.imread(image_path)

#         # load segment class
#         seg = KaloriMeter()

#         # segment image
#         label,result= seg.segment(image_path)
        

#         # set response value
#         retval, buffer = cv2.imencode('.png', result)
#         response = make_response(buffer.tobytes())
#         response.headers['Content-Type'] = 'image/png'
#         return response
