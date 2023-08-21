# Routes to do backend work and connect webpages and data from each other

from main import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from main.models import WorkerPrimary, WorkerTodayAttendance, WorkerAttendance, WorkerSalary, LocationData, SiteData, ProjectData, SiteEngineerDetails, SupervisorDetails, Boss
from datetime import datetime, timedelta
import calendar
from flask_login import login_user, current_user, logout_user, login_required


########################################################## Home Page ################################################################

@app.route("/", methods=["GET", "POST"])                           # Route for the opening page
@app.route("/home", methods=["GET", "POST"])                       # Route when someone tries to navigate to first page
def home():                                                        # This is the first page by default
    return render_template("home.html", title="Home Page")         # Return home.html


########################################################## Login form submission ####################################################

# Decorator when someone click on submit login credential button present at home.html
@app.route("/submit_login_credit", methods=["GET", "POST"])
def submit_login_credit():
    ''' Have to think a logic so that authenticated 
        users can go to their designated place '''
    if current_user.is_authenticated:                             # If the current user is authenticated send him to boss login page
        return render_template("bosslogin.html", title = "Boss Login")
    
    if request.method == "POST":                                  # If the request method is POST get the input credentials
        input_id = request.form["input_id"]                       # Get input ID
        input_password = request.form["input_password"]           # Get input password
        
        #~~~~~~~~~~~~~~~~~~~~~ Add a drop down so that person can select that he is a boss/site engineer/supervisor ~~~~~~~~~~~~~~~~~~~~~~~~~ 
        
        ''' Have to work on authenticating 
            the user '''
        if input_id == "Boss01" and input_password == "123qwe":
            flash("Login Successful", "success")
            return render_template("bosslogin.html", title = "Boss Login")
        
        elif input_id == "Super01" and input_password == "123qwe":
            flash("Login Successful", "success")
            return render_template("supervisorlogin.html", title = "Supervisor Login")
        
        elif input_id == "Site01" and input_password == "123qwe":
            flash("Login Successful", "success")
            return render_template("siteengineerlogin.html", title = "Site Engineer Login")
        
        else:
            flash("Login Unsuccessful. Please check email and password", "warning")
            return render_template("home.html", title="Home")
    return render_template("bosslogin.html", title = "Boss Login")



# Route for the boss login
@app.route("/bosslogin", methods=["POST"])
def bosslogin():
    return render_template("bosslogin.html", title = "Boss Login")

##################################################### Function calls present at bosslogin.html ################################################################


# This is a decorator to add a new site engineer. Its function call is present in bosslogin.html. 
@app.route("/add_site_engineer", methods=["POST"])
def add_site_engineer():
    return render_template("add_site_engineer.html", title = "Add Site Engineer")           # Return the webpage where we can add a new site engineer


# Add new data for the site engineer
@app.route("/submit_new_site_engineer", methods = ["POST"])
def submit_new_site_engineer():
    site_eng_id = request.form["site_eng_id"]
    site_eng_name = request.form["site_eng_name"]
    site_eng_phone = request.form["site_eng_phone"]
    location_id = request.form["location_id"]
    site_id = request.form["site_id"]
    project_id = request.form["project_id"]
    site_eng_email = request.form["site_eng_email"]
    site_eng_password = request.form["site_eng_password"]
    
    ## Add data into the table
    print(site_eng_id, site_eng_name, site_eng_phone, 
          location_id, site_id, project_id, site_eng_email, site_eng_password)
    return render_template("add_site_engineer.html", title = "Add Site Engineer")


# Route to the webpage where we can search the site engineer
app.route("/search_site_engineer", methods = ["POST"])
def search_site_engineer():
    option_site_engineer = request.form["option_site_engineer"]
    search_attribute_site_eng = request.form["search_attribute_site_eng"]
    
    # Add searching query
    print(option_site_engineer ,search_attribute_site_eng)
    # return render_template("update_site_engineer.html", "Update Site Engineer")
    return render_template("under_maintainance.html", title = "Under Maintainance")


# This is a decorator to change the data of site engineer. Its function call is present in bosslogin.html. 
@app.route("/change_site_engineer", methods=["POST"])
def change_site_engineer():                                                                 # Return the webpage where we can change the data of site engineer
    return render_template("change_site_engineer.html", title="Change Site Engineer") 


# This is a decorator to add a new supervisor. Its function call is present in bosslogin.html. 
@app.route("/add_supervisor", methods=["POST"])
def add_supervisor():                                                                       # Return the webpage where we can add a new supervisor
    return render_template("add_supervisor.html", title="Add Supervisor") 


# This is a decorator to change the data of supervisor. Its function call is present in bosslogin.html. 
@app.route("/change_supervisor", methods=["POST"])
def change_supervisor():                                                                   # Return the webpage where we can change the data of supervisor
    return render_template("change_supervisor.html", title="Change Supervisor") 


# This is a decorator to add a new location or project or site. Its function call is present in bosslogin.html. 
@app.route("/add_location_project_site", methods=["POST"])
def add_location_project_site():                                                           # Return the webpage where we can add a new location or project or site
    return render_template("add_location_project_site.html", title="Add Location/Project/Site") 


# This is a decorator to change the data of location or project or site. Its function call is present in bosslogin.html. 
@app.route("/change_location_project_site", methods=["POST"])
def change_location_project_site():                                                        # Return the webpage where we can change the data of location or project or site
    return render_template("change_location_project_site.html", title="Change Location/Project/Site") 


# This is a decorator to check the attendance. Its function call is present in bosslogin.html. 
@app.route("/check_attendance", methods=["POST"])
def check_attendance():                                                                    # Return the webpage where we can check the attndance
    return render_template("check_attendance.html", title="Check Attendance") 


# This is a decorator to check the salary. Its function call is present in bosslogin.html. 
@app.route("/check_salary", methods=["POST"])
def check_salary():                                                                        # Return the webpage where we can check the salary
    return render_template("check_salary.html", title="Check Salary") 


################################################## Funtions on siteengineerlogin.html and supervisorlogin.html ##############################

@app.route("/siteengineerlogin", methods = ["POST"])
def siteengineerlogin():
    return render_template("siteengineerlogin.html", title = "Site Engineer Login")


#``````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````#
@app.route("/supervisorlogin", methods = ["POST"])
def supervisorlogin():
    return render_template("supervisorlogin.html", title = "Supervisor Login")

#````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````#


@app.route("/take_attendance", method = ["POST"])
def take_attendance():
    return render_template("take_attendance", title ="Take Attendance")


@app.route("/view_attendance", method = ["POST"])
def take_attendance():
    return render_template("view_attendance", title ="View Attendance")

@app.route("/edit_attendance", method = ["POST"])
def take_attendance():
    return render_template("edit_attendance", title ="Edit Attendance")



