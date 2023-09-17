from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder="template")
app.static_folder = "static"
# รายชื่อผู้ใช้งาน (ตัวอย่าง)
users = {"user1": "password1", "user2": "password2"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/do")
def do():
    return render_template("do.html")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
    # app.run(debug=True)
