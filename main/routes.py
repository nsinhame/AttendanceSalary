# Routes to do backend work and connect webpages and data from each other

from main import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request
from main.models import WorkerPrimary, WorkerDetail, WorkerTodayMorningAttendance, WorkerTodayEveningAttendance, WorkerAttendance, WorkerSalary, LocationData, SiteData, ProjectData, SiteEngineerDetails, SupervisorDetails, Boss
from datetime import datetime, timedelta, date
import calendar
from flask_login import login_user, current_user, logout_user, login_required


########################################################## Home Page ################################################################

@app.route("/", methods=["GET", "POST"])                           # Route for the opening page
@app.route("/home", methods=["GET", "POST"])                       # Route when someone tries to navigate to first page
def home():                                                        # This is the first page by default
    return render_template("home.html", title="Home Page")         # Return home.html


######################################################### For Logging Out ###########################################################
@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return redirect(url_for("home"))

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
        
        '''Check the given id in all the tables
        '''
        try:
            boss_user = Boss.query.filter_by(boss_id=input_id).first()
            if input_password == boss_user.boss_password:
                flash("Login Successful", "success")
                return render_template("bosslogin.html", title = "Boss Login", login_name = boss_user.boss_name)
        except Exception as e:
            pass
        
        try:
            site_eng_user = SiteEngineerDetails.query.filter_by(site_eng_id=input_id).first()  
            if input_password == site_eng_user.site_eng_password:
                flash("Login Successful", "success")
                return render_template("siteengineerlogin.html", title = "Site Engineer Login", login_name = site_eng_user.site_eng_name)
        except Exception as e:
            
            pass
            
        
        try:    
            supervisor_user = SupervisorDetails.query.filter_by(supervisor_id=input_id).first()
            if input_password == supervisor_user.supervisor_password:
                flash("Login Successful", "success")
                return render_template("supervisorlogin.html", title = "Supervisor Login", login_name = supervisor_user.supervisor_name)
            
        except Exception as e:
            pass
            
        
            
        '''By default input credentials
        '''
        if input_id == "Boss01" and input_password == "123qwe":
            flash("Login Successful", "success")
            return render_template("bosslogin.html", title = "Boss Login", login_name = "Sample Boss")
        
        elif input_id == "Super01" and input_password == "123qwe":
            flash("Login Successful", "success")
            return render_template("supervisorlogin.html", title = "Supervisor Login", login_name = "Sample Supervisor")
        
        elif input_id == "Site01" and input_password == "123qwe":
            flash("Login Successful", "success")
            return render_template("siteengineerlogin.html", title = "Site Engineer Login", login_name = "Sample Site Engineer")
        
        else:
            print(input_id, input_password)
            flash("Login Unsuccessful. Please check email and password", "warning")
            return render_template("home.html", title="Home")
    flash("Wrong Input Credencials", "warning")
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
    # Get all the data from the form
    site_eng_id = request.form["site_eng_id"]
    site_eng_name = request.form["site_eng_name"]
    site_eng_phone = request.form["site_eng_phone"]
    location_id = request.form["location_id"]
    site_id = request.form["site_id"]
    project_id = request.form["project_id"]
    site_eng_email = request.form["site_eng_email"]
    site_eng_password = request.form["site_eng_password"]
    
    # Try to add data
    try:
        site_engineer_data = SiteEngineerDetails(site_eng_id=site_eng_id,
                                                 site_eng_name=site_eng_name,
                                                 site_eng_phone=site_eng_phone,
                                                 location_id=location_id,
                                                 site_id=site_id,
                                                 project_id=project_id,
                                                 site_eng_email=site_eng_email,
                                                 site_eng_password=site_eng_password)
        # Add the data into data base
        db.session.add(site_engineer_data)
        db.session.commit()
    
    except Exception as e:
        flash(f"Got an error: {e}", "warning")
        return render_template("add_site_engineer.html", title="Add Site Engineer")
        

    ## Add data into the table
    return render_template("add_site_engineer.html", title = "Add Site Engineer")




# This is a decorator to change the data of site engineer. Its function call is present in bosslogin.html. 
@app.route("/change_site_engineer", methods=["POST"])
def change_site_engineer():                                                                 # Return the webpage where we can change the data of site engineer
    
    return render_template("change_site_engineer.html", title="Change Site Engineer") 


# Route to the webpage where we can search the site engineer. It is available at change_site_engineer.html
@app.route("/search_site_engineer", methods = ["POST"])                                     
def search_site_engineer():                                                                
    option_site_engineer = request.form["option_site_engineer"]                            
    search_attribute_site_eng = request.form["search_attribute_site_eng"]
    
    if option_site_engineer == "site_eng_id":
        selected_site_engineer = SiteEngineerDetails.query.filter_by(site_eng_id = search_attribute_site_eng).first()       
        attribute_site_engineer = "ID"                    # This is used to tell which attribute is used to search the site engineer           
                                                                                           
    if option_site_engineer == "site_eng_name":
        selected_site_engineer = SiteEngineerDetails.query.filter_by(site_eng_name = search_attribute_site_eng).first()             
        attribute_site_engineer = "Name"                    # This is used to tell which attribute is used to search the site engineer     
    
    if option_site_engineer == "site_id":
        selected_site_engineer = SiteEngineerDetails.query.filter_by(site_id = search_attribute_site_eng).first()                  
        attribute_site_engineer = "Site ID"                    # This is used to tell which attribute is used to search the site engineer
    
    # Add searching query                                                               
    return render_template("update_site_engineer.html", title="Update Site Engineer", selected_site_engineer=selected_site_engineer, option_site_engineer=option_site_engineer,
                           attribute_site_engineer=attribute_site_engineer, search_attribute_site_eng=search_attribute_site_eng)          
    # return render_template("under_maintainance.html", title = "Under Maintainance")        


@app.route("/update_site_engineer", methods = ["POST"])
def update_site_engineer():
    return render_template("update_site_engineer.html", title = "Update Site Engineer")


# Need Working on this. IDs are accepted but name and site id gives error
@app.route("/submit_change_site_engineer/<string:id>", methods = ["GET","POST"])
def submit_change_site_engineer(id):
    try:
        site_engineer = SiteEngineerDetails.query.filter_by(site_eng_id=id).first()
    except:
        try:
            site_engineer = SiteEngineerDetails.query.filter_by(site_eng_name=id).first()
        except:
            site_engineer = SiteEngineerDetails.query.filter_by(site_id=id).first()
    
    
    '''Update the given site engineer with the new given data'''
    if request.form["site_eng_id"]:
        site_engineer.site_eng_id = request.form["site_eng_id"]
    if request.form["site_eng_name"]:
        site_engineer.site_eng_name = request.form["site_eng_name"]
    if request.form["site_eng_phone"]:
        site_engineer.site_eng_phone = request.form["site_eng_phone"]
    if request.form["location_id"]:
        site_engineer.location_id = request.form["location_id"]
    if request.form["site_id"]:
        site_engineer.site_id = request.form["site_id"]
    if request.form["project_id"]:
        site_engineer.project_id = request.form["project_id"]
    if request.form["site_eng_email"]:
        site_engineer.site_eng_email = request.form["site_eng_email"]
    if request.form["site_eng_password"]:
        site_engineer.site_eng_password = request.form["site_eng_password"]
    db.session.commit()
    
    return render_template("/change_site_engineer.html", title = "Change Site Engineer")
    


# ############################################  Adding/updating Worker ##########################################33

@app.route("/add_worker", methods=["POST"])
def add_worker():
    return render_template("add_worker.html", title="Add Worker")

# Add new data for the worker
@app.route("/submit_new_worker", methods = ["POST"])
def submit_new_worker():
    worker_id = request.form["worker_id"]
    worker_name = request.form["worker_name"]
    worker_phone_number = request.form["worker_phone_number"]
    worker_address = request.form["worker_address"]
    worker_gender = request.form["worker_gender"]
    worker_aadhar_number = request.form["worker_aadhar_number"]
    # Bank Details
    worker_account_number = request.form["worker_account_number"]
    worker_ifsc_code = request.form["worker_ifsc_code"]
    worker_bank_name = request.form["worker_bank_name"]
    worker_bank_branch_name = request.form["worker_bank_branch_name"]
    # Bank Details End
    worker_join_date = datetime.strptime(request.form['worker_join_date'], '%Y-%m-%d')
    worker_salary = request.form["worker_salary"]
    supervisor_id = request.form["supervisor_id"]
    site_id = request.form["site_id"]
    still_working = request.form["still_working"]
    
    try:
        worker_data = WorkerDetail(worker_id=worker_id, worker_name=worker_name,
                                   worker_phone_number=worker_phone_number,
                                   worker_address=worker_address, worker_gender=worker_gender,
                                   worker_aadhar_number=worker_aadhar_number, 
                                   worker_account_number=worker_account_number, 
                                   worker_ifsc_code=worker_ifsc_code, worker_bank_name=worker_bank_name,
                                   worker_bank_branch_name=worker_bank_branch_name, worker_join_date=worker_join_date,
                                   worker_salary=worker_salary, supervisor_id=supervisor_id,
                                   site_id=site_id, still_working=still_working)
        
        db.session.add(worker_data)
        db.session.commit()
        return render_template("add_worker.html", title="Add Worker")
    
    except Exception as e:
        flash(f"Got an error: {e}", "warning")
        return render_template("add_worker.html", title="Add Worker")
    
# This decorator is to change the data of the worker
@app.route("/change_worker", methods=["POST"])
def change_worker():                                                                 # Return the webpage where we can change the data of worker
    return render_template("change_worker.html", title="Change Worker") 

# Route to the webpage where we can search the worker. It is available at change_worker.html
@app.route("/search_worker", methods = ["POST"])                                     
def search_worker():                                                                
    option_worker = request.form["option_worker"]                            
    search_attribute_worker = request.form["search_attribute_worker"]
    
    if option_worker == "worker_id":
        selected_worker = WorkerDetail.query.filter_by(worker_id = search_attribute_worker).first()       
        attribute_worker = "ID"                    # This is used to tell which attribute is used to search the worker
                                                                                           
    if option_worker == "worker_name":
        selected_worker = WorkerDetail.query.filter_by(worker_name = search_attribute_worker).first()             
        attribute_worker = "Name"                    # This is used to tell which attribute is used to search the worker
    
    if option_worker == "site_id":
        selected_worker = SiteEngineerDetails.query.filter_by(site_id = search_attribute_worker).first()                  
        attribute_worker = "Site ID"                    # This is used to tell which attribute is used to search the worker
    
    # Add searching query                                                               
    return render_template("update_worker.html", title="Update Worker", selected_worker=selected_worker, option_worker=option_worker,
                           attribute_worker=attribute_worker, search_attribute_worker=search_attribute_worker)          
    
@app.route("/update_worker", methods = ["POST"])
def update_worker():
    return render_template("update_worker.html", title = "Update Worker")


# Change the workers details
@app.route("/submit_change_worker/<string:id>", methods = ["GET","POST"])
def submit_change_worker(id):
    try:
        worker = WorkerDetail.query.filter_by(worker_id=id).first()
        print(worker.worker_id)
    except:
        try:
            worker = WorkerDetail.query.filter_by(worker_name=id).first()
        except:
            worker = WorkerDetail.query.filter_by(site_id=id).first()
    
    '''Update the given worker with the new given data'''
    if request.form["worker_id"]:
        worker.worker_id = request.form["worker_id"]
    if request.form["worker_name"]:
        worker.worker_name = request.form["worker_name"]
    if request.form["worker_phone_number"]:
        worker.worker_phone_number = request.form["worker_phone_number"]
    if request.form["worker_address"]:
        worker.worker_address = request.form["worker_address"]
    if request.form["worker_gender"]:
        worker.worker_gender = request.form["worker_gender"]
    if request.form["worker_aadhar_number"]:
        worker.worker_aadhar_number = request.form["worker_aadhar_number"]
    if request.form["worker_account_number"]:
        worker.worker_account_number = request.form["worker_account_number"]
    if request.form["worker_ifsc_code"]:
        worker.worker_ifsc_code = request.form["worker_ifsc_code"]
    if request.form["worker_bank_name"]:
        worker.worker_bank_name = request.form["worker_bank_name"]
    if request.form["worker_bank_branch_name"]:
        worker.worker_bank_branch_name = request.form["worker_bank_branch_name"]
    if request.form["worker_join_date"]:
        worker.worker_join_date = datetime.strptime(request.form['worker_join_date'], '%Y-%m-%d')
    if request.form["worker_salary"]:
        worker.worker_salary = request.form["worker_salary"]
    if request.form["supervisor_id"]:
        worker.supervisor_id = request.form["supervisor_id"]
    if request.form["site_id"]:
        worker.site_id = request.form["site_id"]
    if request.form["still_working"]:
        worker.still_working = request.form["still_working"]
    
    db.session.commit()
    
    return render_template("/change_worker.html", title = "Change Worker")
    





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




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Attendance system @@@@@@@@@@@@@@@@@@@@@@@@@@@
@app.route("/take_morning_attendance", methods = ["POST"])
def take_morning_attendance():
    worker_attendance = WorkerDetail.query.all()
    site_name = SiteData.query.filter_by(site_id = worker_attendance[0].site_id).first()
    site_name = site_name.site_name
    date_time = datetime.now()
    attendance_date = date_time.strftime("%d/%m/%Y")
    return render_template("take_morning_attendance.html", title ="Take Attendance", worker_attendance=worker_attendance, site_name = site_name, attendance_date = attendance_date)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~` Sample`
@app.route("/submit_morning_attendance", methods = ["POST"])
def submit_morning_attendace():
     # If time is between 10 PM to 4 AM, delete the database
    current_time = datetime.now().hour
    # if current_time in [22, 23, 0, 1, 2, 3, 4]:
    db.session.query(WorkerTodayMorningAttendance).delete()
    db.session.commit()
    
    present_workers = request.form.getlist("present")
    all_workers = WorkerPrimary.query.all()
    absent_workers = [x.worker_id for x in all_workers if x.worker_id not in present_workers]
    
    # MArk present
    for worker in present_workers:
        attendance = WorkerTodayMorningAttendance(worker_id = worker,
                                           morning_attendance_status = "P",
                                           attendance_date = date.today())
    
        db.session.add(attendance)
        db.session.commit()
    
    # Mark absent
    for worker in absent_workers:
        attendance = WorkerTodayMorningAttendance(worker_id = worker,
                                           morning_attendance_status = "A",
                                           attendance_date = date.today())
        
        
        db.session.add(attendance)
        db.session.commit()
    
    
    return render_template("siteengineerlogin.html", title = "Site Engineer Login")


# For evening attendance
@app.route("/take_evening_attendance", methods = ["POST"])
def take_evening_attendance():
    worker_attendance = WorkerDetail.query.all()
    site_name = SiteData.query.filter_by(site_id = worker_attendance[0].site_id).first()
    site_name = site_name.site_name
    date_time = datetime.now()
    attendance_date = date_time.strftime("%d/%m/%Y")
    return render_template("take_evening_attendance.html", title ="Take Attendance", worker_attendance=worker_attendance, site_name = site_name, attendance_date = attendance_date)


################## Work on this
@app.route("/submit_evening_attendance", methods = ["POST"])
def submit_evening_attendace():
    
    # If time is between 10 PM to 4 AM, delete the database
    current_time = datetime.now().hour
    # if current_time in [22, 23, 0, 1, 2, 3, 4]:
    db.session.query(WorkerTodayEveningAttendance).delete()
    db.session.commit()
    
    present_workers = request.form.getlist("present")
    overtime_hour_work = request.form.getlist("overtime_hour")
    all_workers = WorkerPrimary.query.all()
    absent_workers = [x.worker_id for x in all_workers if x.worker_id not in present_workers]
    all_workers_id = [x.worker_id for x in all_workers]
    worker_dict = dict(zip(all_workers_id, overtime_hour_work))
    
    
    
    for worker in present_workers:
        attendance = WorkerTodayEveningAttendance(worker_id = worker,
                                           evening_attendance_status = "P",
                                           attendance_date = date.today(),
                                           overtime_today = worker_dict[worker])
    
        db.session.add(attendance)
        db.session.commit()
    
    # Mark absent
    for worker in absent_workers:
        attendance = WorkerTodayEveningAttendance(worker_id = worker,
                                           evening_attendance_status = "A",
                                           attendance_date = date.today(),
                                           overtime_today = 0)
        
        
        db.session.add(attendance)
        db.session.commit()
    
    return render_template("siteengineerlogin.html", title = "Site Engineer Login")


# Check Absent Present Half Day for the day
def finalize_attendance(id):
    morning_attendance = WorkerTodayMorningAttendance.query.filter_by(worker_id = id).first()
    evening_attendance = WorkerTodayEveningAttendance.query.filter_by(worker_id = id).first()
    
    
    if morning_attendance.morning_attendance_status == "P" and evening_attendance.evening_attendance_status == "P":
        return "P"
    elif morning_attendance.morning_attendance_status == "A" and evening_attendance.evening_attendance_status == "A":
        return "A"
    else:
        return "H"
    

# Submit the whole day attendance
@app.route("/add_full_day_attendance", methods = ["POST"])
def add_full_day_attendance():
    morning_attendance = WorkerTodayMorningAttendance.query.order_by(WorkerTodayMorningAttendance.worker_id).all()
    evening_attendance = WorkerTodayEveningAttendance.query.order_by(WorkerTodayEveningAttendance.worker_id).all()
    
    for i in evening_attendance:
        attendance = WorkerAttendance(row_id = random.randint(1, 1000),
                                      worker_id = i.worker_id,
                                      attendance_date = i.attendance_date,
                                      attendance_month = "August",
                                      attendance_year = "2023",
                                      overtime_hours = i.overtime_today,
                                      attendance_status = finalize_attendance(i.worker_id))
        
        db.session.add(attendance)
        db.session.commit()
    return render_template("siteengineerlogin.html", title = "Site Engineer Login") 











@app.route("/view_attendance", methods = ["POST"])
def view_attendance():
    worker_today_morning_attendance = WorkerTodayMorningAttendance.query.all()
    worker_today_evening_attendance = WorkerTodayEveningAttendance.query.all()
    worker_attendance = WorkerAttendance.query.all()
    return render_template("view_attendance.html", title ="View Attendance", worker_today_morning_attendance=worker_today_morning_attendance,
                           worker_today_evening_attendance=worker_today_evening_attendance,
                           worker_attendance=worker_attendance)

@app.route("/edit_attendance", methods = ["POST"])
def edit_attendance():
    return render_template("edit_attendance.html", title ="Edit Attendance")






#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! This is for testing !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
import string
import random
n = 6

@app.route("/add_data", methods = ["POST"])
def add_data():
    return render_template("add_data.html", title = "Add sample data")

@app.route("/add_sample_data", methods = ["POST"])
def add_sample_data():
    for i in range(1, 5):
        res = "".join(random.choices(string.ascii_uppercase +
                             string.digits, k=n))
        data = WorkerPrimary(worker_id = f"{i}",
                            worker_name = str(res))                      
        print(data)
        db.session.add(data)                                                
        db.session.commit()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        data = WorkerDetail(worker_id = f"{i}", 
                            worker_name = str(res),
                            worker_phone_number = random.randint(60000000, 9999999999),
                            worker_address = "12, Asd Rty, Lkj",
                            worker_gender = "F",
                            worker_aadhar_number = random.randint(60000000, 9999999999),
                            worker_account_number = random.randint(60000000, 9999999999),
                            worker_ifsc_code = "eqw233",
                            worker_bank_name = "Bank of India",
                            worker_bank_branch_name = "Lksd",
                            worker_join_date = datetime.now(),
                            worker_salary = 300,
                            supervisor_id = "01",
                            site_id = "S01",
                            still_working = "Y")
        
        print(data)
        db.session.add(data)                                                
        db.session.commit()
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
    data = LocationData(location_id = "L01",
                        location_name = "Tkjh",
                        location_state = "Fihjlh",
                        location_project_number = 3)
    print(data)
    db.session.add(data)
    db.session.commit()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    data = SiteData(site_id="S01",
                    site_name ="Tkhj",
                    location_id = "L01",
                    site_pincode = 244421,
                    site_project_number = 2)
    print(data)
    db.session.add(data)
    db.session.commit()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    data = ProjectData(project_id = "P01",
                       project_name = "Perw",
                       site_id = "S01",
                       location_id = "L01",
                       site_eng_id = "SE01",
                       supervisor_id = "SP01",
                       total_workers = 15)
    print(data)
    db.session.add(data)
    db.session.commit()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    data = SiteEngineerDetails(site_eng_id = "SE01",
                               site_eng_name = "Hdsdf",
                               site_eng_phone = 9312456780,
                               location_id = "L01",
                               site_id= "S01",
                               project_id = "P01",
                               site_eng_email = "sqf@qe.com",
                               site_eng_password = "#2ffee")
    print(data)
    db.session.add(data)
    db.session.commit()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    data = SupervisorDetails(supervisor_id = "SP01",
                             supervisor_name = "Pofff",
                             supervisor_phone = 8907654321,
                             location_id = "L01",
                             site_id = "S01",
                             project_id = "P01",
                             supervisor_email = "rw2@ggg.in",
                             supervisor_password = "pwx5y",
                             site_eng_id = "SE01")
    
    db.session.add(data)
    db.session.commit()
    return render_template("add_data.html", title = "Added data")



@app.route("/view_all_data", methods = ["POST"])
def view_all_data():
    worker_primary = WorkerPrimary.query.all()
    worker_detail = WorkerDetail.query.all()
    location_data = LocationData.query.all()
    site_data = SiteData.query.all()
    project_data = ProjectData.query.all()
    site_eng_detail = SiteEngineerDetails.query.all()
    supervisor_detail = SupervisorDetails.query.all()
    worker_today_morning_attendance = WorkerTodayMorningAttendance.query.all()
    worker_today_evening_attendance = WorkerTodayEveningAttendance.query.all()
    worker_attendance = WorkerAttendance.query.all()
    
    
    return render_template("view_all_data.html", title = "View all data", 
                           worker_primary=worker_primary, worker_detail=worker_detail, 
                           location_data=location_data, site_data=site_data,
                           project_data=project_data, site_eng_detail=site_eng_detail,
                           supervisor_detail=supervisor_detail,
                           worker_today_morning_attendance=worker_today_morning_attendance,
                           worker_today_evening_attendance=worker_today_evening_attendance,
                           worker_attendance=worker_attendance)

@app.route("/view_site_engineer", methods = ["POST"])
def view_site_engineer():
    site_eng_detail = SiteEngineerDetails.query.all()
    
    return render_template("view_site_engineer.html", title = "View Site Engineer Data", 
                           site_eng_detail=site_eng_detail)

@app.route("/view_workers_details", methods = ["POST"])
def view_workers_details():
    worker_detail = WorkerDetail.query.all()
    return render_template("view_workers_details.html", title = "View Workers Details", 
                           worker_detail=worker_detail)

@app.route("/view_loc_site_proj", methods = ["POST"])
def view_loc_site_proj():
    location_data = LocationData.query.all()
    site_data = SiteData.query.all()
    project_data = ProjectData.query.all()

    return render_template("view_loc_site_proj.html", title = "View Loc Site & Project", 
                            location_data=location_data, site_data=site_data,
                           project_data=project_data)

@app.route("/view_supervisor", methods = ["POST"])
def view_supervisor():
    supervisor_detail = SupervisorDetails.query.all()
    
    return render_template("view_supervisor.html", title = "View Supervisor Details", 
                           supervisor_detail=supervisor_detail)
