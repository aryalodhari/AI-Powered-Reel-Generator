from flask import Blueprint, render_template, request, current_app
import uuid
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

main = Blueprint("main", __name__, template_folder="templates")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/create", methods=["GET", "POST"])
def create():
    my_id = str(uuid.uuid4())

    if request.method == "POST":
        rec_id = request.form.get("uuid")
        text = request.form.get("text")

        upload_root = current_app.config['UPLOAD_FOLDER']
        save_dir = os.path.join(upload_root, rec_id)

        os.makedirs(save_dir, exist_ok=True)

        # save text
        with open(os.path.join(save_dir, "text.txt"), "w", encoding="utf-8") as f:
            f.write(text or "")

        input_files = []

        for file in request.files.values():
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(save_dir, filename))
                input_files.append(filename)

        # 🔥 FIXED input.txt
        with open(os.path.join(save_dir, "input.txt"), "w") as f:
            for fname in input_files:
                f.write(f"file '{fname}'\n")
                f.write("duration 1\n")

    return render_template("create.html", my_id=my_id)



@main.route("/gallery")
def gallery():
    return render_template("gallery.html")
