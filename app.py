from flask import Flask, request, render_template
from threading import Lock
from start import generateFlag
from encoding import caesar, randomNum
import secrets
import sqlite3
import json
import string
import os
import random
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/level1")
def level1():
    return render_template("level1/level1.html")

@app.route("/level1/verify", methods=['GET'])
def l1verify():
    try:
        alphabets = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
        code = request.args.get('code')
        conn = sqlite3.connect('./templates/level1/data.db').cursor()
        encodedcode = caesar(code, len(code), alphabets)
        statement = "SELECT * FROM users WHERE secret='{}'".format(encodedcode)
        conn.execute(statement)
        results = conn.fetchall()
        conn.close()
        #THIS IS PURPOSELY REALLY BAD CODE
        match = False
        for (a, b) in results:
            if (a == "User554" and b == encodedcode):
                match = True
        return {
            "match": match,
            "debugData": statement + "|"+ str(results)
        }
    except Exception as e:
        return {
            "match": False,
            "debugData": statement + "|"+str(e)
        }


def evalString(message):
    if message == None:
        return message
    else:
        newMessage = ""
        subMessage = ""
        evalOn = False
        for i in message:
            if i == '{' and not evalOn:
                evalOn = True
            elif i != '}' and evalOn:
                subMessage += i
            elif i == '}' and evalOn:
                evalOn = False
                print(eval(subMessage))
                try:
                    tmpMes = eval(subMessage)
                    
                    newMessage += str(tmpMes)
                except:
                    newMessage += subMessage
                subMessage = ""
            else:
                newMessage += i
    return newMessage



@app.route("/level2/makepost", methods=['GET'])
def l2post():
    post = evalString(request.args.get('post'))
    conn = sqlite3.connect('./templates/level2/data.db')
    c = conn.cursor()
    c.execute('INSERT INTO posts VALUES (?,?)', [request.args.get('user'), post])
    conn.commit()
    conn.close()
    return {
        "success": True,
        "post": post
    }

@app.route("/level2/verify", methods=['GET'])
def l2verify():
    conn = sqlite3.connect('./templates/level2/data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    res = c.fetchall()
    conn.close()
    for (user, password) in res:
        if(request.args.get('user') == user):
            if (request.args.get('pass') == password):
                return {
                    "match": True,
                    "passwordMatch": True
                }
            else:
                return {
                    "match": True,
                    "passwordMatch": False
                }
    return {
        "match": False,
        "passwordMatch": False
    }

@app.route("/level2")
def level2():
    return render_template("level2/level2.html")

@app.route("/level2/posts")
def level2posts():
    conn = sqlite3.connect('./templates/level2/data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM posts WHERE user=?', [request.args.get('user')])
    res = c.fetchall()
    conn.close()
    return {
        "posts": [b for (a,b) in res]
    }


seed=random.randint(0,127)
def nextNum():
    global seed
    seed=(seed + 1)%128
    return seed
def encrypt(message):
    stringNums = string.ascii_letters + string.digits
    encryptedMessage = ""
    for i in message:
        nextNum()
        encryptedMessage += stringNums[(ord(i) + randomNum(seed))%len(stringNums)]
    return encryptedMessage


@app.route("/level3/encrypt", methods=['GET'])
def level3encrypt():
    username=request.args.get('user')
    password=request.args.get('pass')
    message=request.args.get('message')
    conn = sqlite3.connect('./templates/level3/data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username='"+username+"' AND password='"+password+"'")
    res = c.fetchall()
    conn.close()
    if(len(res) != 1):
        return {
            "auth": False,
            "encryptedMessage": ""
        }
    else:
        return {
            "auth": True,
            "encryptedMessage": encrypt(message)
        }

@app.route("/level3")
def level3():
    return render_template("level3/level3.html", encrypted=encrypt(generateFlag(int(os.environ["l3Seed"]))))

@app.route("/codecheck", methods=['GET'])
def codecheck():
    level = request.args.get('level')
    code = request.args.get('code')
    match = False
    if(level == 'level1' and code == generateFlag(int(os.environ["l1Seed"])) or 
    level == 'level2' and code == generateFlag(int(os.environ["l2Seed"]))  or
    level == 'level3' and code == generateFlag(int(os.environ["l3Seed"]))):
        match = True
    return {
        'match': match
    }

