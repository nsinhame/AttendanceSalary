from main import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from main.models import WorkerPrimary, WorkerTodayAttendance, WorkerAttendance, WorkerSalary, LocationData, SiteData, ProjectData, SiteEngineerDetails, SupervisorDetails, Boss
from datetime import datetime, timedelta
import calendar
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods=["GET", "POST"])                             # Route for the opening page
@app.route("/homepage", methods=["GET", "POST"])                   # Route when someone tries to navigate to first page
def front_page():
    return render_template("homepage.html", title="Home Page")

@app.route("/login", methods=["GET", "POST"])
def LoginForm():
    if current_user.is_authenticated:
        return redirect(url_for("explore"))
    if request.method == "POST":
        _email = request.form.get("inputEmail")
        _password = request.form.get("inputPassword")
        # _user = User.query.filter_by(email=_email).first()
        # if _user and bcrypt.check_password_hash(_user.password, _password):
        #     login_user(_user, remember=_remember)
        #     flash("Login Successful", "success")
            # return redirect(url_for("profile"))
        # Sample:
        if _email == "Boss01@1" and _password == "123qwe":
            flash("Login Successful", "info")
            return render_template("bosslogin.html", title = "Boss Login")
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
            return render_template("homepage.html", title="Home")
    return redirect(url_for("homepage"))
