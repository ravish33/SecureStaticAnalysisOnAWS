# import memcache
import mysql.connector
from flask import Flask, render_template, request, redirect, Markup, sessions, session
from flask import flash, request, session, abort, url_for
#from flask.ext.hashing import Hashing
import re
import hashlib
from pymongo import MongoClient
from random import SystemRandom
import os
import subprocess
# mc = memcache.Client(['db-cache.ielwjl.cfg.use1.cache.amazonaws.com:11211'], debug = 1)

application = Flask(__name__)
cryptogen = SystemRandom()
application.secret_key = str(cryptogen.random())
app = application
#hashing = Hashing(application)
## Connection details for SQL Connections
# cnx = mysql.connector.connect(user='ravish33', password='ravish293',
#                               host='ravish.cg5bqgnmovqh.us-west-2.rds.amazonaws.com',
#                               database='Ravish_secure')

# cursor = cnx.cursor(buffered=True)

client = MongoClient('ds115918.mlab.com:15918')
print("DB Connected Successfully")
db = client['ravish']
db.authenticate('ravish33','ravish293')

collection = db.secure

@app.route('/')
def index():
    return render_template('login.html')


@app.route("/select", methods=['GET', 'POST'])
def hello():
    if request.method == "GET":
        if 'user' in session:
            return render_template("welcome.html", user= session['user'])
        else:
            return render_template("login.html")


    if request.method == "POST":

        userName = request.form["uname"]
        password = request.form["pwd"]

        hash_object = hashlib.sha512(password.encode())
        hex_dig = hash_object.hexdigest()

        query = collection.find({"userName": userName, 'password':hex_dig})


        for post in query:

            if (post['password'] == hex_dig):
                return render_template("welcome.html", user=userName)

        return render_template("login.html", Error="Invalid Username or Password")









@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET' or request.method == 'POST':
        return render_template('register.html')


@app.route("/registerUser", methods=['GET', 'POST'])

def register_User():
    if request.method == 'GET':
        return render_template('register.html')

    userName = request.form["uname"]
    password = request.form["pwd"]
    patternUserName = '(?=^.{3,20}$)^[a-zA-Z][a-zA-Z0-9]*[._-]?[a-zA-Z0-9]$'
    pattern = '[A-Za-z0-9@#$%^&+=]{8,}'
    pw = re.match(pattern, password)
    un = re.match(patternUserName,userName)


    query = collection.find({"userName":userName})
    for post in query:

        if(post['userName']==userName):
            return render_template("register.html", Error = "User Already Registered.")





    if (re.match(pattern, password) and re.match(patternUserName,userName) and len(userName)>4 and len(userName)<21):

        hash_object = hashlib.sha512(password.encode())
        hex_dig = hash_object.hexdigest()


        print("match")
        user = {
            "userName":userName,
            "password":hex_dig
        }
        print("user")
        collection.insert(user)
        print("after insert")
        return render_template("login.html")
    else:
        print("else part")
        return render_template("register.html", Error = "Invalid Username or Password")




@app.route("/uploadFile", methods=['GET', 'POST'])
def uploadFile():

    if request.method == "GET":
        return render_template("welcome.html",user = session['user'])
    print("upload")
    file = request.files["File"].filename

    userName = request.form["user"]



    if (file.endswith(".py") | file.endswith(".c") | file.endswith(".CPP") | file.endswith(".java") | file.endswith(".PHP") | file.endswith(".PL") ):
        content = request.files['File'].read()

        path = "/home/ec2-user/Files/"
        with open(path+file, "w") as file_test:
            file_test.write(content)

        #Rats output
        command = "rats --quiet --html -w 3 " + path + file
        print(command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # Launch the shell command:
        ratsOutput, error = process.communicate()
        print
        ratsOutput



        #flowfinder output
        flawfinderOutput = "File must be .c or .CPP"
        if (file.endswith(".c") | file.endswith(".CPP")):
            command = "flawfinder " + path
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            flawfinderOutput, error = process.communicate()


        data = {
            'fileName': file,
            'content': content,
            'userName': userName,
            'ratsOutPut':ratsOutput,
            'flowfinderOutPut':flawfinderOutput
        }
        db.data.insert(data)

        print("-----flawfinder----")
        print(flawfinderOutput)

        #remove file from Directory
        command = "rm -r " + path + file
        print(command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # Launch the shell command:
        removeOutPut, error = process.communicate()
        print("-------remove-----")
        print(removeOutPut)




        return render_template("welcome.html", ratsOutPut = Markup(ratsOutput), flawfinderOutPut = flawfinderOutput, user = userName)


    else:
        return render_template("welcome.html", Message = "Invalid file type", user = userName)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if not 'user' in session:
        return render_template("login.html")
    else:
        userName = request.form["user"]
        session.pop('user', userName)
        return render_template("login.html", Error = "Logged out")

if __name__ == '__main__':
    #app.run(debug=True)
    app.run('ec2-35-164-188-52.us-west-2.compute.amazonaws.com')


