from flask import Flask, request, render_template
from threading import Lock
import secrets
app = Flask(__name__)

class TokenCache():
    def __init__(self):
        self.cache = {}
        self.lock = Lock()
    def addToCache(self, key):
        self.lock.acquire()
        if (key not in self.cache):
            self.cache[key] = secrets.token_urlsafe()
            self.lock.release()
            return self.cache[key]
        else:
            self.lock.release()
            raise Exception
    def queryCache(self, key):
        return self.cache[key]
    def removeFromCache(self, key):
        self.lock.acquire()
        del self.cache[key]
        self.lock.release()

tokenCache2 = TokenCache()
tokenCache3 = TokenCache()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/level1")
def level1():
    return render_template("level1/level1.html")

@app.route("/level1/querydb", methods=['GET'])
def l1querydb():
    try:
        if (tokenCache1.queryCache(request.form['name']) != request.form['token']):
            raise Exception
    except:
        return "Unauthorised user"
    pass

@app.route("/level2")
def level2():
    return "not implemented"

@app.route("/level3")
def level3():
    return "not implemented"