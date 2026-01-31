from flask import Blueprint, render_template, request, current_app
import uuid
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}


main = Blueprint(
    "main",
    __name__,
    template_folder="templates"
)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/create", methods=["GET", "POST"])
def create():
    my_id = str(uuid.uuid1())
    if request.method == "POST":
        rec_id = request.form.get("uuid")
        text = request.form.get("text")
        print(request.files.keys())
        for key, value in request.files.items():
            print(key, value)
            # upload file
            file = request.files[key]
            if file:
                filename = secure_filename(file.filename)
                os.mkdir(os.path.join(current_app.config['UPLOAD_FOLDER'], rec_id))
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], rec_id, filename))

    return render_template("create.html", my_id=my_id)

@main.route("/gallery")
def gallery():
    return render_template("gallery.html")
