from flask import Flask, render_template
from app import app


@app.route("/")
def home():
    return "hello world"


@app.route("/login")
def login():
    return render_template("login.html")


def runserver():
    app.run(debug=True, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    runserver()
