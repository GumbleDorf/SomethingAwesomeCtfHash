from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/level1")
def level1():
    return render_template("level1/level1.html")

@app.route("/level1/querydb")
def l1querydb():
    pass

@app.route("/level2")
def level2():
    return "not implemented"

@app.route("/level3")
def level3():
    return "not implemented"