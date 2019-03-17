from flask import Flask, render_template,request,redirect,url_for
from bson import ObjectId
from pymongo import MongoClient
import os
from werkzeug import secure_filename
from MatchSkills import *
from AzureAPI import *
import cgi


app = Flask(__name__)
title = "TODO with Flask"
heading = "ToDo Reminder"
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

client = MongoClient("mongodb://localhost:27017") #host uri
db = client.job_desc_db  #Select the database

job_desc_list = db.list_collection_names() #Select the collection

@app.route("/")
def home():
    job_list = job_desc_list
    return render_template("homePage.html", jobs = job_list)



@app.route('/uploader', methods = ['POST', 'GET'])
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if request.method == 'POST':
        jobid = request.form['jobid']
    print(jobid)
    keywords = getKeywords(file)
    flag, applied_job, score, results = skill_match(keywords, jobid, job_desc_list)

    return render_template("details.html", flag=flag, applied_job=applied_job, score=score, results=results)



if __name__ == "__main__":
    app.run(debug=True)

