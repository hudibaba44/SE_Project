import pymongo
from flask import Flask, jsonify, abort, make_response, request, url_for, session
from flask import render_template, redirect
import json
import re
import os
import hashlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
db = myclient["database"]
users = db["users"]
frameworkdb = db["framework"]

def cleardb():
    db.users.drop()

@app.route("/", methods = ["GET"])
def test():
    cleardb()
    return jsonify({}),200

@app.route("/signup", methods = ["POST"])
def add_user():
    req = eval(request.data)
    name = req["name"]
    user_email = req["email"]
    pwd = req["password"]
    document = {"email_id" : user_email}
    if users.find_one(document) == None:
        document = {"email_id" : user_email ,"password": pwd, "name" : name}
        x = users.insert_one(document)
        status = 200
        print(x)
    else:
        x = users.find_one(document)
        print(x)
        status = 400
    return jsonify({}), status

@app.route("/login", methods = ["POST"])
def login():
    req = eval(request.data)
    user_email = req["email"]
    pwd = req["password"]
    document = {"email_id" : user_email, "password" : pwd}
    x = users.find_one(document)
    res = {}
    if x == None:
        status = 404
    elif x['password'] == pwd:
        status = 200
        res = {"email" : user_email, "fullName" : x['name']}
    else:
        status = 404
    return jsonify(res), status

@app.route("/logout", methods = ["GET"])
def logout():
    session.pop('username', None)
    return jsonify({}),200

@app.route("/framework_signup", methods = ["POST"])
def framework_signup():
    req = eval(request.data)
    email_id = req["email"]
    framework = req["framework"]
    path = "/" + email_id + framework
    folder_path = os.path.join(oath, framework)
    os.mkdir(folder_path,777)
    document = {id : email_id, framework_path : folder_path}
    x = frameworkdb.find_one(document)
    if x == None:
        frameworkdb.insert_one(x)
        # create git repo
        status = 200
    else:
        status = 400
    return jsonify({}), status


if __name__ == '__main__':
    app.secret_key = "secret_key"
    app.run(debug = True)
