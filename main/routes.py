from main import app, db
from flask import render_template, redirect, url_for, flash, request
from main.models import WorkerPrimary, WorkerTodayAttendance, WorkerAttendance, WorkerSalary, LocationData, SiteData, ProjectData, SiteEngineerDetails, SupervisorDetails, Boss
from datetime import datetime, timedelta
import calendar


@app.route("/", methods=["GET", "POST"])
@app.route("/layout", methods=["GET", "POST"])
def home():
    first_name_ = request.form.get("f_name")
    return redirect(url_for("layout"))