from flask import Blueprint, render_template, request
import uuid

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
    my_id = uuid
    if request.method == "POST":
        print(request.files.keys())
        for key, value in request.files.items():
            print(key, value)
    return render_template("create.html", my_id=my_id)

@main.route("/gallery")
def gallery():
    return render_template("gallery.html")
