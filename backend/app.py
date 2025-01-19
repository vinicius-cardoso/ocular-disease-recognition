from flask import Flask, render_template, request, redirect
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit uploads to 16MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "image" not in request.files:
            return redirect(request.url)

        file = request.files["image"]

        if file.filename == "":
            return redirect(request.url)

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            with Image.open(filepath) as img:
                width, height = img.size

            return render_template(
                "index.html", uploaded_image=file.filename, width=width, height=height
            )

    return render_template("index.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)

