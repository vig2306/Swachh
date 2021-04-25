from flask import render_template, request, redirect, url_for, session, escape, Flask, jsonify
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bson import ObjectId
from random import randint
import json
import pathlib
import hashlib
import requests
import random
import os
from datetime import datetime
from flask_pymongo import PyMongo
import re
import math,random
import smtplib
from werkzeug.utils import secure_filename
from fastai.vision import *
# import cv2
import numpy as np
import base64
from PIL import Image
from io import BytesIO
from math import radians, cos, sin, asin, sqrt
import herepy
import ast
from os.path import join, dirname, realpath
from flask_paginate import Pagination, get_page_args
from email.message import EmailMessage
import smtplib

port = 5000

host = "192.168.1.2"

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://vignesh23:8oqq9WUNHGw2eSYo@jobcluster1.sal4m.mongodb.net/Swachh?retryWrites=true&w=majority"

mongo = PyMongo(app)

app.config['uploads'] = join(dirname(realpath(__file__)), "uploads")
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = '5234124584324'

headers = {'Authorization': 'Basic cm9vdDo2NjIyNDQ2Ng==',
           'Content-Type': 'application/json'}


UPLOAD_FOLDER = "../static/uploads/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route('/api/register', methods=['POST'])
def api_register():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        user_email = data["user_email"]
        check_if_exist = mongo.db.grievance_users.find_one(
            {"user_email": user_email})
        if check_if_exist:
            return jsonify({"status": 'failed', "message": "User already exist!"})
        else:
            result = mongo.db.grievance_users.insert_one(data)
            return jsonify({"status": 'success', "message": "registered successfully!"})
em = ''
o = ''
@app.route('/api/reset', methods=['POST'])
def api_reset():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)
        user_email = em
        user_password = data["user_password"]
        otp = data["otp"]
        vr_user_password = data["vr_password"]
        print(otp)
        print(o)
        if (otp == o and vr_user_password == user_password):
            update_password = mongo.db.grievance_users.find_one_and_update(
                {'user_email': user_email}, {'$set': {"user_password": user_password}},{'new':True})
            print(update_password)
            print("MAtched OTP")
            return jsonify({"status": 'success', "message": "registered successfully!"})
        else:
            return jsonify({"status": 'failed', "message": "Enter valid OTP"})

@app.route('/api/login', methods=['POST'])
def api_login():
    if request.method == 'POST':
        if 'logged_in' in session:
            return jsonify({"status": 'user is already logged.'})
        else:
            data = request.get_data()
            data = json.loads(data)
            user_name = data['user_email']
            user_password = data['user_password']
            loginuser = mongo.db.grievance_users.find_one({"$and": [{"$or": [{"user_email": user_name}, {
                "user_phone": user_name}]}, {"user_password": user_password}]})
            print(loginuser,user_name,user_password)
            print("!1")
            if loginuser['user_type'] == 'general':
                del loginuser["user_password"]
                del loginuser["_id"]
                session['username'] = loginuser["user_email"]
                session['logged_in'] = True
                return jsonify({"data": loginuser, "status": "user logged in succesffully"})
            elif loginuser['user_type'] == 'admin':
                return jsonify({"status": 'failed', "message": "Restricted login"})
            else:
                return jsonify({"status": 'failed', "message": "invalid Credential!"})

@app.route('/api/forget', methods=['POST'])
def api_forget():
    data = request.get_data()
    data = json.loads(data)
    user_name = data['user_email']
    
    loginuser = mongo.db.grievance_users.find_one({"$and": [{"$or": [{"user_email": user_name}, {
        "user_phone": user_name}]}]})
    print(loginuser,user_name)
    print("!1")
    if loginuser['user_type'] == 'general':
        del loginuser["_id"]
        digits = "0123456789"
        OTP = ""
        for i in range(4) :
            OTP += digits[math.floor(random.random() * 10)]
        global o
        global em
        o = str(OTP)
        em = str(user_name)
        EMAIL_ADDRESS = 'vs062300@gmail.com'
        EMAIL_PASSWORD = 'qikpAx-keqgo3-guhmyr'
        msg = EmailMessage()
        msg['Subject'] = 'OTP is ' + str(OTP)
        msg['To'] = user_name
        msg['From'] = EMAIL_ADDRESS
        msg.set_content('OTP is' + str(OTP))
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return jsonify({"data": loginuser, "status": "user exists"})
    else:
        return jsonify({"status": 'failed', "message": "invalid Credential!"})

@app.route('/api/logout', methods=['GET'])
def api_logout():
    del session['logged_in']
    del session['username']
    return jsonify({"status": "user logged out in succesffully"})

@app.route("/", methods=['GET'])
@app.route("/login", methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            loginuser = mongo.db.grievance_users.find_one({"$and": [{"$or": [{"user_email": username}, {
                "user_phone": username}]}, {"user_password": password}]})
            print("1")
            print(loginuser)
            if loginuser['user_type'] == 'admin':
                print('\n\ntrue:')
                session['admin_area'] = loginuser['user_email']
                print(session['admin_area'])
                session['admin_login'] = True
                grievance_all = list(mongo.db.grievance.find(
                    {'assigned_authority': loginuser['user_email']}))
                return redirect('/index')
            else:
                CONTEXT_msg = 'Entered Username and password do not match. Please Retry!'
                return render_template("loginpage.html", CONTEXT_msg=CONTEXT_msg)
        except Exception as e:
            print(e)
            return render_template('loginpage.html')
        grievance_all = list(mongo.db.grievance.find(
            {'assigned_authority': session['admin_area']}))
        return render_template('problems.html', all=[grievance_all, session['admin_area']])
    else:
        CONTEXT_msg = ''
        return render_template("loginpage.html", CONTEXT_msg=CONTEXT_msg)


@app.route('/logout')
def logout():

    del session['admin_login']
    del session['admin_area']
    return redirect('/login')


@app.route('/upload')
def upload():
    return render_template('add.html')


@app.route('/hello/<send_mail>', methods=['GET', 'POST'])
def predict(send_mail="yes"):
    send_mail_to = None
    grievance_all = list(mongo.db.grievance.find({"grievance_type": "unpredicted"}))

    for i in grievance_all:
        if 'grievance_type' not in i or i['grievance_type'] == "unpredicted":
            filename = str(i['grievance_id'][:5])

            pathh = i['image_link']
            
            path = Path('./')
            
            classes = ['Garbage', 'Pothole', 'Sewage']
            
            data = ImageDataBunch.single_from_classes(path, classes, ds_tfms=get_transforms(), size=240).normalize(imagenet_stats)
            
            learn = cnn_learner(data, models.resnet101, metrics=error_rate)
            
            learn.load('phase1')
            
            img = open_image(pathh)
            pred_class, pred_idx, outputs = learn.predict(img)
            print(str(pred_class))
            
            if(str(pred_class) == "Sewage"):
                send_mail_to = "tirth.hs@somaiya.edu"
            if(str(pred_class) == "Garbage"):
                send_mail_to = "sarvesh.bangad@somaiya.edu"
            if(str(pred_class) == "Pothole"):
                send_mail_to = "v.sunderraman@somaiya.edu"
            all1 = mongo.db.grievance.find_one_and_update({'grievance_id': i["grievance_id"]}, {
                '$set': {"grievance_type": str(pred_class)}})

            if send_mail == "yes":

                sendMail(send_mail_to, "New Grievance Received",
                         "Your department has received a grievance. Please check your portel for details.")
            return "smd"


def distance(lat1, lat2, lon1, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))

    r = 6371

    return(c * r)

@app.route('/api/history/<email>', methods=['GET'])
def history(email):
    grievance_all = list(mongo.db.grievance.find({"user_id": email}))
    grievance_all = grievance_all[::-1]
    for i in grievance_all:
        if 'area' not in i or i['area'] == "unpredicted":
            longitude = float(i['longitude'])
            latitude = float(i['latitude'])
            res = getLocationDetails(latitude, longitude)
            update_location = mongo.db.grievance.find_one_and_update(
                {'grievance_id': i["grievance_id"]}, {'$set': {"area": res}})
        del i["_id"]
        i["id"] = i["grievance_id"]

        i["image_link"] = "http://"+ host+":5000" +i["image_link"][1:]
    
    print(grievance_all)
    
    return jsonify({"status": 'success', "data": grievance_all})


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        data = request.get_data()
        data = json.loads(data)

        im = Image.open(BytesIO(base64.b64decode(data['image_link'])))
        image_link='./static/uploads/'+str(datetime.now())+str(data['grievance_id'])+'.jpeg'
        im.save(image_link, 'JPEG')
        
        data["image_link"] = image_link

        data["assigned_authority"] = "null"
        data["assigned_date"] = str(datetime.now())
        data["status"] = "unsolved"
        data["timestamp"] = str(datetime.now())
        data["area"] = "unpredicted"

        mongo.db.grievance.insert_one(data)

        predict()

        return jsonify({"status": 'success', "message": "registered successfully!"})


# @app.route('/records')
# def records():
#     all = list(mongo.db.grievance.find())
#     return render_template('table.html', all=all)


@app.route('/reports')
def reports():
    grievance_all = list(mongo.db.grievance.find())

    pothole = [0] * 12
    sewage = [0] * 12  # Total grievance reported
    garbage = [0] * 12

    totalpothole = totalsewage = totalgarbage = 0   # Grievances reported

    solved = [0] * 12   # Solved vs Pending
    unsolved = [0] * 12

    for i in grievance_all:
        if(i["grievance_type"] == "Sewage"):
            # pothole.append(i["grievance_type"])
            date, time = i["assigned_date"].split(" ")
            year, month, day = date.split("-")
            sewage[int(month)-1] += 1
            totalsewage += 1

            if(i["status"] == "unsolved"):
                unsolved[int(month)-1] += 1
            else:
                solved[int(month)-1] += 1

        if(i["grievance_type"] == "Pothole"):
            # pothole.append(i["grievance_type"])
            date, time = i["assigned_date"].split(" ")
            year, month, day = date.split("-")
            pothole[int(month)-1] += 1
            totalpothole += 1

            if(i["status"] == "unsolved"):
                unsolved[int(month)-1] += 1
            else:
                solved[int(month)-1] += 1
        if(i["grievance_type"] == "Garbage"):
            # pothole.append(i["grievance_type"])
            date, time = i["assigned_date"].split(" ")
            year, month, day = date.split("-")
            garbage[int(month)-1] += 1
            totalgarbage += 1

            if(i["status"] == "unsolved"):
                unsolved[int(month)-1] += 1
            else:
                solved[int(month)-1] += 1

    return render_template('admin.html', garbage=garbage, seewage=sewage, pothole=pothole, solved=solved, unsolved=unsolved, totalsewage=totalsewage, totalgarbage=totalgarbage, totalpothole=totalpothole)


def getLocationDetails(latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)

    gp = herepy.GeocoderReverseApi(
        'oT6JdnfeU8cnrcaqqRHSGzICgG6noykgly9Tz8PnXHE')
    response = gp.retrieve_addresses([latitude, longitude])
    response = str(response)
    response = json.loads(response)
    response = response["items"][0]["address"]["label"]
    return response


@app.route("/index")
def index():
    try:
        if(session['admin_login']):
            last_id=None
            grievance_all = list(mongo.db.grievance.find())
            grievance_all = grievance_all[::-1]
            page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
            total = len(grievance_all)
            pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
            pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
            for i in grievance_all:
                print(i["area"])
                if i['area'] == "unpredicted":    
                    longitude = float(i['longitude'])
                    latitude = float(i['latitude'])
                    res = getLocationDetails(latitude, longitude)
                    update_location = mongo.db.grievance.find_one_and_update(
                        {'grievance_id': i["grievance_id"]}, {'$set': {"area": res}})
            return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="info",b="light",c="light",first="index",second="solved",third="unsolved")
    except Exception as e: 
        CONTEXT_msg = ''
        return render_template("loginpage.html", CONTEXT_msg=CONTEXT_msg)

def get_users(users,offset=0, per_page=6):
    return users[offset: offset + per_page]

@app.route('/solve/<id1>')
def solve(id1):
    mongo.db.grievance.find_one_and_update(
        {'grievance_id': id1}, {'$set': {'status': 'solved'}})
    grievance_all = list(mongo.db.grievance.find({'grievance_id': id1}))
    for i in grievance_all:
        to = i["user_id"]
    print("Hello kfnkfnf",to)
    gmail_user = 'vs062300@gmail.com'
    gmail_password = 'qikpAx-keqgo3-guhmyr'

    sent_from = gmail_user
    #to = "singroleketan@gmail.com"
    subject = "Grievance Solved"
    body = "Your reported grievance has been solved,Thank you for your support."

    email_text = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (sent_from, to, subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print('Email sent!')
    except Exception as e:
        print('Something went wrong...'+str(e))
    return redirect('/index')

@app.route("/userspecific/<id>")
def userspecific(id):
    grievance_all = list(mongo.db.grievance.find({"user_id": id}))
    grievance_all = grievance_all[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    for i in grievance_all:
        if 'area' not in i or i['area'] == "unpredicted":
            longitude = float(i['longitude'])
            latitude = float(i['latitude'])
            res = getLocationDetails(latitude, longitude)
            update_location = mongo.db.grievance.find_one_and_update(
                {'grievance_id': i["grievance_id"]}, {'$set': {"area": res}})
   
    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination)

@app.route("/sewage")
def sewage():
    grievance_all = list(mongo.db.grievance.find({"grievance_type": "Sewage"}))
    grievance_all = grievance_all[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="info",b="light",c="light",first="sewage",second="solvedsewage",third="unsolvedsewage")


@app.route("/garbage")
def garbage():
    grievance_all = list(mongo.db.grievance.find(
        {"grievance_type": "Garbage"}))
    grievance_all = grievance_all[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')

    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="info",b="light",c="light",first="garbage",second="solvedgarbage",third="unsolvedgarbage")


@app.route("/potholes")
def potholes():
    grievance_all = list(mongo.db.grievance.find(
        {"grievance_type": "Pothole"}))
    grievance_all = grievance_all[::-1]
    print("Hello",grievance_all)
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    print("How",pagination_users)

    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="info",b="light",c="light",first="potholes",second="solvedpothole",third="unsolvedpothole")


@app.route("/solved")
def solved():
    grievance_all = list(mongo.db.grievance.find(
        {"status": "solved"}))
    grievance_all = grievance_all[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="light",b="info",c="light",first="index",second="solved",third="unsolved")

@app.route("/unsolved")
def unsolved():
    grievance_all = list(mongo.db.grievance.find(
        {"status": "unsolved"}))
    grievance_all = grievance_all[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="light",b="light",c="info",first="index",second="solved",third="unsolved")

@app.route("/solvedgarbage")
def solvedgarbage():
    grievance_all = list(mongo.db.grievance.find({"$and":[{"status": "solved"},{"grievance_type": "Garbage"}]}))
    grievance_all = grievance_all[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="light",b="info",c="light",first="garbage",second="solvedgarbage",third="unsolvedgarbage")

@app.route("/unsolvedgarbage")
def unsolvedgarbage():
    grievance_all = list(mongo.db.grievance.find({"$and":[{"status": "unsolved"},{"grievance_type": "Garbage"}]}))
    grievance_all = grievance_all[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="light",b="light",c="info",first="garbage",second="solvedgarbage",third="unsolvedgarbage")

@app.route("/solvedpothole")
def solvedpothole():
    grievance_all = list(mongo.db.grievance.find({"$and":[{"status": "solved"},{"grievance_type": "Pothole"}]}))
    grievance_all = grievance_all[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="light",b="info",c="light",first="potholes",second="solvedpothole",third="unsolvedpothole")   

@app.route("/unsolvedpothole")
def unsolvedpothole():
    grievance_all = list(mongo.db.grievance.find({"$and":[{"status": "unsolved"},{"grievance_type": "Pothole"}]}))
    grievance_all = grievance_all[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="light",b="light",c="info",first="potholes",second="solvedpothole",third="unsolvedpothole")   

@app.route("/solvedsewage")
def solvedsewage():
    grievance_all = list(mongo.db.grievance.find({"$and":[{"status": "solved"},{"grievance_type": "Sewage"}]}))
    grievance_all = grievance_all[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="light",b="info",c="light",first="sewage",second="solvedsewage",third="unsolvedsewage")

@app.route("/unsolvedsewage")
def unsolvedsewage():
    grievance_all = list(mongo.db.grievance.find({"$and":[{"status": "unsolved"},{"grievance_type": "Sewage"}]}))
    grievance_all = grievance_all[::-1]
    page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    total = len(grievance_all)
    pagination_users = get_users(grievance_all,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,css_framework='bootstrap4')
    return render_template('problems.html', all=pagination_users,page=page,per_page=per_page,pagination=pagination,a="light",b="light",c="info",first="sewage",second="solvedsewage",third="unsolvedsewage")

def sendMail(to, subject, body):
    gmail_user = 'vs062300@gmail.com'
    gmail_password = 'qikpAx-keqgo3-guhmyr'

    sent_from = gmail_user
    #to = "singroleketan@gmail.com"
    subject = subject
    body = body

    email_text = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (sent_from, to, subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
        return 'Email sent!'
    except Exception as e:
        print('Something went wrong...'+str(e))
        return 'Email not sent!'


if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
