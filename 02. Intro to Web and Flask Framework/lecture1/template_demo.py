from flask import Flask
from flask import (
    render_template,
)

app = Flask(__name__)
#   NOTE: all *_folder arguments are relative to the path of the application module. So having
#   FLASK_APP="lecture1.main" already sets these folders to "lecture1/*_folder"


@app.route("/")
def index():
    name = "Rado"
    return render_template("index.html", name = name)

if __name__ == "__main__":
    app.run()

