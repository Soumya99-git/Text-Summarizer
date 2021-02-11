from flask import Flask,redirect,session,render_template,request,flash,send_file
from pymongo import MongoClient
import os
import videotoaudio
import text_summariztion
import feedback_analysis
        
client  = MongoClient("mongodb://localhost:27017/")
db = client["blogpost"]

coll = db["feedback"]
coll1 = db["login"]

app = Flask(__name__)
app.config["UPLOAD_FOLDER"]=r"C:\Users\Soumya Chatterjee\Desktop\INFRAMIND\PROJECT\uploads"

app.secret_key = 'super secret key'


@app.route("/",methods=["GET"])
def home():
    if "uname" in session:
        if session["uname"]=="admin":
            return render_template("home_adm.html")
        return render_template("home.html")
    else:
        return render_template("home!sign.html")

@app.route("/signin",methods=["GET","POST"])
def signin():
    if request.method=="POST":
        uname = request.form["uname"]
        password = request.form["password"]
                        
        l = list(coll1.find({"uname":uname}))
        if (len(l)==0):
            flash("User does not exist")
            return render_template("signin.html")
        else:
            a=l[0]
            if password!=a["password"]:
                flash("Wrong password")
                return render_template("signin.html")
            else:
                session["uname"] = uname
                if uname=="admin":
                    return render_template("home_adm.html")
                else:
                    return render_template("home.html",uname=session["uname"])
    else:
        return render_template("signin.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        uname = request.form["uname"]
        password = request.form["password"]
        re_pass = request.form["password2"]
        email = request.form["email"]
        
        l = list(coll1.find({"uname":uname}))
        if(len(l)>0):
            flash("User already exists")
            return render_template("signup.html")
        else:
            if password!=re_pass:
                flash("Retype password correctly")
                return render_template("signup.html")
            else:
                new_user={
                    "uname": uname,
                    "email": email,
                    "password": password
                }
                coll1.insert_one(new_user)
                session["uname"] = uname
                return render_template("home.html",uname=session["uname"])
    else:
        return render_template("signup.html")


@app.route("/feed",methods=["GET","POST"])
def feed():
    if "uname" in session:
        
        if session["uname"]=="admin":
            feed = list(coll.find())
            return render_template("feedback_adm.html",feeds=feed)
        
        if request.method=="POST":
            uname = session["uname"]
            feed = request.form["feed"]
            polarity = feedback_analysis.feedback(feed)
            new_feed = {

                "uname": uname,

                "feedback": feed,

                "polarity": polarity

            }
            print(new_feed)
            coll.insert_one(new_feed)
            flash("Thank you for Posting a feedback")
            return render_template("home.html",uname=session["uname"])
        else:
            return render_template("feedback.html",uname=session["uname"])
    else:
        flash("Please Sign in")
        return render_template("signin.html")

@app.route("/vid_aud",methods=["GET","POST"])
def vid_aud():
    if "uname" in session:
        if request.method=="POST":
            if not request.files['f']:
                flash("Give some input file")
                return render_template("home.html")
            upload_file = request.files["f"]
            if upload_file.filename[-3:0]=="mp3": 
                file_name = upload_file.filename.replace(" ","")
                upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))
                print(file_name)
                new_path = videotoaudio.spliter_audio_text(file_name,1)
                return send_file(new_path,as_attachment=True)
            else:
                flash("mp3 or wav or mp4 files allowed")
                return render_template("home.html")
        else:
            return render_template("home.html",uname=session["uname"])
    else:
        flash("Please Sign in")
        return render_template("signin.html")

@app.route("/vid_aud_feed",methods=["GET","POST"])
def vid_aud_feed():
    if "uname" in session:
        if session["uname"]=="admin":
            if request.method=="POST":
                if not request.files['f']:
                    flash("Give some input file")
                    return render_template("home_adm.html")
                upload_file = request.files["f"]
                file_name = upload_file.filename.replace(" ","")
                upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))
                print(file_name)
                feed_value,feed_back = videotoaudio.spliter_audio_text(file_name,0)
                new_feed = {
                    "uname" : "Admin",
                    "feedback" : feed_back,
                    "polarity" : feed_value
                }

                print(new_feed)
                coll.insert_one(new_feed)
                feed_all  = list(coll.find())
                return render_template("feedback_adm.html",feeds=feed_all)
            else:
                return render_template("home_adm.html")
        else:
            flash("Sign in as Admin to Use this Feature")
            return render_template("signin.html")
    else:
        flash("Please Sign in")
        return render_template("signin.html")

@app.route("/text",methods=["GET","POST"])
def text():
    if "uname" in session:
        if request.method=="POST":
            if not request.files['f']:
                flash("Give some input file")
                return render_template("home.html",uname=session["uname"])
            upload_file = request.files["f"]
            if upload_file.filename[-3:] == "txt":
                file_name = upload_file.filename.replace(" ","_")
                upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'],file_name))
                path = text_summariztion.summarization(file_name)
                n_path = os.path.join(app.config['UPLOAD_FOLDER'],path)
                return send_file(n_path,as_attachment=True)
            else:
                flash("Only text file for Text Summarizer")
                return render_template("home.html")
        else:
            return render_template("home.html",uname=session["uname"])
    else:
        flash("Please Sign in")
        return render_template("signin.html")


@app.route("/logout",methods=["GET"])
def logout():
    session.pop("uname",None)
    return render_template("home!sign.html")

@app.route("/charts")
def charts():
    d={}
    d["total"] = len(list(coll.find()))
    d["positive"] = len(list(coll.find({"polarity":"positive"})))
    d["negative"] = len(list(coll.find({"polarity":"negative"})))
    return render_template("chart.html",d = d)

if __name__ == "__main__":
    app.run(debug=True)