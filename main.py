from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename

import pst_reader
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config["UPLOAD_FOLDER"] = "static/files"
app.config["UPLOAD_EXTENSIONS"] = ['.pst']



class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload a file")


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])

def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file_ext = os.path.splitext(file.filename)[1]

        if not file:
            return "You need to select a file"
        elif file_ext not in app.config["UPLOAD_EXTENSIONS"]:
            return "Extension " + file_ext + " is not allowed"
        else:
            # Upload file and return the proto content
            file.save(os.path.join(
                os.path.abspath(os.path.dirname(__file__)), 
                app.config['UPLOAD_FOLDER'], 
                secure_filename(file.filename)))
            
            rel_path = app.config["UPLOAD_FOLDER"] + "/" + file.filename

            return "<pre><code>" + str(pst_reader.main( rel_path )) + "</code></pre>"
        
    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)