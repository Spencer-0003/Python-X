# I honestly hate Python, I did this because I was bored at 11:30pm waiting for Cyberpunk 2077 to release.

import secrets
from flask import Flask, request, json, send_from_directory
from PIL import Image
from waitress import serve

import os
from os import path
from os.path import splitext

api_key = "changeme"
file_size = 6000000 # Increase or decrease to your liking.

app = Flask(__name__)


@app.route("/upload", methods = ["POST"])
def upload():
    if (request.method != "POST"):
        return "Only POST requests can be sent to this URL.", 405
    else:
        if (request.form.to_dict(flat = False)["api_key"][0] == api_key):
            file = request.files["sharex"]
            file.flush()
            size = os.fstat(file.fileno()).st_size

            if (size > file_size):
                return "File size too large", 401

            image = Image.open(file)
            data = list(image.getdata())
            file_without_exif = Image.new(image.mode, image.size)
            file_without_exif.putdata(data)

            filename = secrets.token_urlsafe(5)
            file_without_exif.save(os.path.join("uploads", file.filename))
            return json.dumps({"file": file.filename}), 200
        else:
            return "Invalid key!", 403

@app.route("/uploads/<file>", methods = ["GET"])
def showFile(file):
    if (path.exists("uploads/" + file)):
        return send_from_directory("uploads/", filename = file), 200
    else:
        return "Invalid file", 404

# app.run(port = 80)

if (__name__ == "__main__"):
    print("Uploader running.")
    serve(app, host = "0.0.0.0", port = 3000)
