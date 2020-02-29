import os
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_session import Session
import ingredientsOCR as i
import factsOCR as f
import json
import ast

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQLAlchemy(app)

values = {}
values["calories"] = 0
values["total fat"] = 0
values["cholesterol"] = 0
values["sodium"] = 0
values["total carbohydrate"] = 0
values["sugars"] = 0
values["protein"] = 0

loggedIn = False

factsCount = 1
ingredientsCount = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)


	def __repr__(self):
		return '<User %r>' % self.email


@app.route("/")
@app.route("/home")
def home():
	if "userEmail" in session:
		with open("data.txt", "r") as a:
			r = a.readline()
		res = ast.literal_eval(r)

		if res["calories"] == -1:
			values["calories"] = 0
		else:
			values["calories"] = res["calories"]

		if res["total fat"] == -1:
			values["total fat"] = 0
		else:
			values["total fat"] = res["total fat"]

		if res["cholesterol"] == -1:
			values["cholesterol"] = 0
		else:
			values["cholesterol"] = res["cholesterol"]

		if res["sodium"] == -1:
			values["sodium"] = 0
		else:
			values["sodium"] = res["sodium"]

		if res["total carbohydrate"] == -1:
			values["total carbohydrate"] = 0
		else:
			values["total carbohydrate"] = res["total carbohydrate"]

		if res["sugars"] == -1:
			values["sugars"] = 0
		else:
			values["sugars"] = res["sugars"]

		if res["protein"] == -1:
			values["protein"] = 0
		else:
			values["protein"] = res["protein"]

		

		return render_template("index.html", logged=True, nutrients=values)
	else:
		return render_template("index.html", logged=False, nutrients=values)

@app.route("/view")
def view():
	return render_template("view.html", data=User.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		
		session.permanent = True

		userEmail = request.form["em"]
		userPass = request.form["pw"]

		session["userEmail"] = userEmail
		session["userPass"] = userPass

		found_user = User.query.filter_by(email=userEmail).first()

		if found_user:
			if found_user.password == userPass:
				#flash("Login Successful!", "info")
				return redirect(url_for("home"))
			else:
				#flash("Incorrect Password!", "error")
				return render_template("login.html")
		else:
			#flash("This email does not correspond to an account!", "error")
			return render_template("login.html")

	else:
		if "user" in session:
			#flash("Already Logged In!", "info")
			return redirect(url_for("home"))
		return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():

	if request.method == "POST":
		session.permanent = True
		
		userEmail = request.form["em"]
		userPass = request.form["pw"]
		
		session["userEmail"] = userEmail
		session["userPass"] = userPass

		db.create_all()

		found_user = User.query.filter_by(email=userEmail).first()
		
		if found_user != None:
			#flash("This email is already in use!", "error")
			return render_template("register.html")
		else:
			usr = User(email=userEmail, password=userPass)
			db.session.add(usr)
			db.session.commit()
			loggedIn = True
			#flash("Registration Successful!", "info")
			return render_template("index.html", logged=True, nutrients=values)
	else:
		if "userEmail" in session:
			#flash("Already Logged In!", "info")
			return redirect(url_for("home"))
		else:
			return render_template("register.html")

@app.route("/facts", methods=["POST", "GET"])
def facts():
	global factsCount
	
	if "userEmail" in session:
		if request.method == "GET":
			return render_template("upload_facts.html")
		else:
			target = os.path.join(APP_ROOT, "c:/Users/prana/Hackathons/A-Z Hacks/AZHacks-master/images")
			print(target)

			if not os.path.isdir(target):
				os.mkdir(target)

			for file in request.files.getlist("file"):
				print(file)
				filename = "ocrlabel.jpg"
				destination = "/".join([target, filename])
				print(destination)
				file.save(destination)
				factsCount += 1

			return redirect(url_for("facts_info"))
	else:
		return redirect(url_for("login"))



@app.route("/facts_info")
def facts_info():
	if "userEmail" in session:
		output = f.returnFacts("c:/Users/prana/Hackathons/A-Z Hacks/AZHacks-master/images/ocrlabel.jpg")
		for k in output.keys():
			values[k] += output[k]

		# write output to file
		with open("data.txt", "w") as a:
			a.write(str(values))

	return render_template("facts_info.html", data=output)

@app.route("/ingredients", methods=["POST", "GET"])
def ingredients():
	global ingredientsCount
	
	if "userEmail" in session:
		if request.method == "GET":
			return render_template("upload_ingredients.html")
		else:
			target = os.path.join(APP_ROOT, "c:/Users/prana/Hackathons/A-Z Hacks/AZHacks-master/images")
			print(target)

			if not os.path.isdir(target):
				os.mkdir(target)

			for file in request.files.getlist("file"):
				print(file)
				filename = "ocrimage.jpg"
				destination = "/".join([target, filename])
				print(destination)
				file.save(destination)
				ingredientsCount += 1

			ingredientsList = request.form["allergens"]
			session["bads"] = ingredientsList.split(",")

			return redirect(url_for("ingredients_info"))
	else:
		return redirect(url_for("login"))

@app.route("/ingredients_info")
def ingredients_info():
	if "userEmail" in session:
		output = i.returnText("c:/Users/prana/Hackathons/A-Z Hacks/AZHacks-master/images/ocrimage.jpg", session["bads"])
	return render_template("ingredients_info.html", data=output)

@app.route("/logout")
def logout():
	if "userEmail" in session:
		userEmail = session["userEmail"]
		userPass = session["userPass"]

		session.pop("userEmail", None)
		session.pop("userPass", None)

		loggedIn = False
		#flash("You have been logged out!", "info")
	#else:
		#flash("You are not logged in!", "error")
	
	return redirect(url_for("home"))

@app.route("/reset")
def reset():
	User.query.delete()
	db.session.commit()

	session.pop("userName", None)
	session.pop("userEmail", None)
	session.pop("userPass", None)

	values = {}

	loggedIn = False

	factsCount = 1
	ingredientsCount = 1

	return redirect(url_for("home"))

if __name__ == "__main__":
	db.create_all()
	app.run(debug=True);