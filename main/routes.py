from main import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from main.models import WorkerPrimary, WorkerTodayAttendance, WorkerAttendance, WorkerSalary, LocationData, SiteData, ProjectData, SiteEngineerDetails, SupervisorDetails, Boss
from datetime import datetime, timedelta
import calendar
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods=["GET", "POST"])                             # Route for the opening page
@app.route("/homepage", methods=["GET", "POST"])                   # Route when someone tries to navigate to first page
def front_page():
    return render_template("home.html", title="Home Page")

@app.route("/submit_login_credit", methods=["GET", "POST"])
def LoginForm():
    if current_user.is_authenticated:
        return redirect(url_for("bosslogin"))
    if request.method == "POST":
        input_id = request.form["input_id"]
        input_password = request.form["input_password"]
        if input_id == "Boss01@1" and input_password == "123qwe":
            flash("Login Successful", "success")
            return render_template("bosslogin.html", title = "Boss Login")
        else:
            flash("Login Unsuccessful. Please check email and password", "warning")
            return render_template("home.html", title="Home")
    return render_template("bosslogin.html", title = "Boss Login")
