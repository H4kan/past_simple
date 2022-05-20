from crypt import methods
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entxt = request.form["entxt"]
        pltxt = entxt
        return render_template("index.html", pltxt=pltxt, entxt=entxt)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run()
