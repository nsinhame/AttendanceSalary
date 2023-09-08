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
                return render_template("bosslogin.html", title = "Boss Login", login_name = boss_user.boss_name, login_site_id = None)
        except Exception as e:
            pass
        
        try:
            site_eng_user = SiteEngineerDetails.query.filter_by(site_eng_id=input_id).first()  
            if input_password == site_eng_user.site_eng_password:
                flash("Login Successful", "success")
                return render_template("siteengineerlogin.html", title = "Site Engineer Login", login_name = site_eng_user.site_eng_name, login_site_id = site_eng_user.project_id)
        except Exception as e:
            
            pass
            
        
        try:    
            supervisor_user = SupervisorDetails.query.filter_by(supervisor_id=input_id).first()
            if input_password == supervisor_user.supervisor_password:
                flash("Login Successful", "success")
                return render_template("supervisorlogin.html", title = "Supervisor Login", login_name = supervisor_user.supervisor_name, login_site_id =supervisor_user.project_id)
            
        except Exception as e:
            pass
            
        
            
        '''By default input credentials
        '''
        if input_id == "Boss01" and input_password == "123qwe":
            flash("Login Successful", "success")
            return render_template("bosslogin.html", title = "Boss Login", login_name = "Sample Boss", login_site_id = None)
        
        elif input_id == "Super01" and input_password == "123qwe":
            flash("Login Successful", "success")
            return render_template("supervisorlogin.html", title = "Supervisor Login", login_name = "Sample Supervisor", login_site_id = None)
        
        elif input_id == "Site01" and input_password == "123qwe":
            flash("Login Successful", "success")
            return render_template("siteengineerlogin.html", title = "Site Engineer Login", login_name = "Sample Site Engineer", login_site_id = None)
        
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
    # option_site_engineer = request.form["option_site_engineer"]
    option_site_engineer = "site_eng_id"                            
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
    except Exception as e:
        flash(f"Gon an error: {e}", "warning")
    
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
    project_id = request.form["project_id"]
    still_working = request.form["still_working"]
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(request.form['worker_join_date'], type(request.form['worker_join_date']))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    try:
        worker_data = WorkerDetail(worker_id=worker_id, worker_name=worker_name,
                                   worker_phone_number=worker_phone_number,
                                   worker_address=worker_address, worker_gender=worker_gender,
                                   worker_aadhar_number=worker_aadhar_number, 
                                   worker_account_number=worker_account_number, 
                                   worker_ifsc_code=worker_ifsc_code, worker_bank_name=worker_bank_name,
                                   worker_bank_branch_name=worker_bank_branch_name, worker_join_date=worker_join_date,
                                   worker_salary=worker_salary, supervisor_id=supervisor_id,
                                   project_id=project_id, still_working=still_working)
        
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
    # option_worker = request.form["option_worker"]
    option_worker = "worker_id"                            
    search_attribute_worker = request.form["search_attribute_worker"]
    
    if option_worker == "worker_id":
        selected_worker = WorkerDetail.query.filter_by(worker_id = search_attribute_worker).first()       
        attribute_worker = "ID"                    # This is used to tell which attribute is used to search the worker
                                                                                           
    if option_worker == "worker_name":
        selected_worker = WorkerDetail.query.filter_by(worker_name = search_attribute_worker).first()             
        attribute_worker = "Name"                    # This is used to tell which attribute is used to search the worker
    
    if option_worker == "project_id":
        selected_worker = WorkerDetail.query.filter_by(project_id = search_attribute_worker).first()                  
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
    if request.form["project_id"]:
        worker.project_id = request.form["project_id"]
    if request.form["still_working"]:
        worker.still_working = request.form["still_working"]
    
    db.session.commit()
    
    return render_template("/change_worker.html", title = "Change Worker")
    


# ############################################  Adding/updating Supervisor ##########################################33



# This is a decorator to add a new supervisor. Its function call is present in bosslogin.html. 
@app.route("/add_supervisor", methods=["POST"])
def add_supervisor():                                                                       # Return the webpage where we can add a new supervisor
    return render_template("add_supervisor.html", title="Add Supervisor") 


@app.route("/submit_new_supervisor", methods=["POST"])
def submit_new_supervisor():
    supervisor_id = request.form["supervisor_id"]
    supervisor_name = request.form["supervisor_name"]
    supervisor_phone = request.form["supervisor_phone"]
    location_id = request.form["location_id"]
    site_id = request.form["site_id"]
    project_id = request.form["project_id"]
    supervisor_email = request.form["supervisor_email"]
    supervisor_password = request.form["supervisor_password"]
    site_eng_id = request.form["site_eng_id"]
    
    try:
        supervisor_data = SupervisorDetails(supervisor_id=supervisor_id,
                                            supervisor_name=supervisor_name,
                                            supervisor_phone=supervisor_phone,
                                            location_id=location_id,
                                            site_id=site_id,project_id=project_id,
                                            supervisor_email=supervisor_email,
                                            supervisor_password=supervisor_password,
                                            site_eng_id=site_eng_id)
        
        db.session.add(supervisor_data)
        db.session.commit()
        
    except Exception as e:
        flash(f"Got an error: {e}", "warning")
        return render_template("add_supervisor.html", title="Add Supervisor")
    
    return render_template("add_supervisor.html", title="Add Supervisor")


# This is a decorator to change the data of supervisor. Its function call is present in bosslogin.html. 
@app.route("/change_supervisor", methods=["POST"])
def change_supervisor():                                                                   # Return the webpage where we can change the data of supervisor
    return render_template("change_supervisor.html", title="Change Supervisor") 


@app.route("/search_supervisor", methods = ["POST"])                                     
def search_supervisor():                                                                
    # option_supervisor = request.form["option_supervisor"]
    option_supervisor = "supervisor_id"                            
    search_attribute_supervisor = request.form["search_attribute_supervisor"]
    
    if option_supervisor == "supervisor_id":
        selected_supervisor = SupervisorDetails.query.filter_by(supervisor_id = search_attribute_supervisor).first()       
        attribute_supervisor = "ID"                    # This is used to tell which attribute is used to search the supervisor           
                                                                                           
    if option_supervisor == "supervisor_name":
        selected_supervisor = SupervisorDetails.query.filter_by(supervisor_name = search_attribute_supervisor).first()             
        attribute_supervisor = "Name"                    # This is used to tell which attribute is used to search the supervisor     
    
    if option_supervisor == "site_id":
        selected_supervisor = SupervisorDetails.query.filter_by(site_id = search_attribute_supervisor).first()                  
        attribute_supervisor = "Site ID"                    # This is used to tell which attribute is used to search the supervisor
    
    # Add searching query                                                               
    return render_template("update_supervisor.html", title="Update Supervisor", selected_supervisor=selected_supervisor, option_supervisor=option_supervisor,
                           attribute_supervisor=attribute_supervisor, search_attribute_supervisor=search_attribute_supervisor)          
    # return render_template("under_maintainance.html", title = "Under Maintainance")        


@app.route("/update_supervisor", methods = ["POST"])
def update_supervisor():
    return render_template("update_supervisor.html", title = "Update Supervisor")

@app.route("/submit_change_supervisor/<string:id>", methods = ["GET","POST"])
def submit_change_supervisor(id):
    try:
        supervisor = SupervisorDetails.query.filter_by(supervisor_id=id).first()
    except:
        try:
            supervisor = SupervisorDetails.query.filter_by(supervisor_name=id).first()
        except:
            supervisor = SupervisorDetails.query.filter_by(site_id=id).first()
    
    
    '''Update the given site engineer with the new given data'''
    if request.form["supervisor_id"]:
        supervisor.supervisor_id = request.form["supervisor_id"]
    if request.form["supervisor_name"]:
        supervisor.supervisor_name = request.form["supervisor_name"]
    if request.form["supervisor_phone"]:
        supervisor.supervisor_phone = request.form["supervisor_phone"]
    if request.form["location_id"]:
        supervisor.location_id = request.form["location_id"]
    if request.form["site_id"]:
        supervisor.site_id = request.form["site_id"]
    if request.form["project_id"]:
        supervisor.project_id = request.form["project_id"]
    if request.form["supervisor_email"]:
        supervisor.supervisor_email = request.form["supervisor_email"]
    if request.form["supervisor_password"]:
        supervisor.supervisor_password = request.form["supervisor_password"]
    if request.form["site_eng_id"]:
        supervisor.site_eng_id = request.form["site_eng_id"]
    db.session.commit()
    
    return render_template("/change_supervisor.html", title = "Change Supervisor")
    


###################################### Add/Update Boss ##########################################################


# This is a decorator to add a new boss. Its function call is present in bosslogin.html. 
@app.route("/add_boss", methods=["POST"])
def add_boss():                                                           # Return the webpage where we can add a new location 
    return render_template("add_boss.html", title="Add Boss") 


@app.route("/submit_new_boss", methods = ["POST"])
def submit_new_boss():
    boss_id = request.form["boss_id"]
    boss_name = request.form["boss_name"]
    boss_email = request.form["boss_email"]
    boss_password = request.form["boss_password"]
    
    try:
        boss_data = Boss(boss_id=boss_id,boss_name=boss_name,
                         boss_email=boss_email,boss_password=boss_password)
        
        db.session.add(boss_data)
        db.session.commit()
        
    except Exception as e:
        flash(f"Got an error: {e}", "warning")
        return render_template("add_boss.html", title="Add Boss")
    
    return render_template("add_boss.html", title="Add Boss")

# This is a decorator to change the data of boss. Its function call is present in bosslogin.html. 
@app.route("/change_boss", methods=["POST"])
def change_boss():                                                        # Return the webpage where we can change the data of boss
    return render_template("change_boss.html", title="Change Boss") 


@app.route("/search_boss", methods=["POST"])
def search_boss():
    option_boss = "boss_id"
    search_attribute_boss = request.form["search_attribute_boss"]
    
    selected_boss = Boss.query.filter_by(boss_id = search_attribute_boss).first()
    
    return render_template("update_boss.html", title = "Update Boss", option_boss=option_boss,search_attribute_boss=search_attribute_boss,
                           selected_boss=selected_boss)
    
@app.route("/update_boss", methods=["POST"])
def update_boss():
    return render_template("update_boss.html", title="Update Boss")


@app.route("/submit_change_boss/<string:id>", methods=["GET", "POST"])
def submit_change_boss(id):
    boss = Boss.query.filter_by(boss_id=id).first()
    
    if request.form["boss_id"]:
        boss.boss_id = request.form['boss_id']
    if request.form["boss_name"]:
        boss.boss_name = request.form['boss_name']
    if request.form["boss_email"]:
        boss.boss_email = request.form['boss_email']
    if request.form["boss_password"]:
        boss.boss_password = request.form['boss_password']
    db.session.commit()
    
    return render_template("/change_boss.html", title="Change Boss")





###################################### Add/Update Location ##########################################################


# This is a decorator to add a new location. Its function call is present in bosslogin.html. 
@app.route("/add_location", methods=["POST"])
def add_location():                                                           # Return the webpage where we can add a new location 
    return render_template("add_location.html", title="Add Location") 


@app.route("/submit_new_location", methods = ["POST"])
def submit_new_location():
    location_id = request.form["location_id"]
    location_name = request.form["location_name"]
    location_state = request.form["location_state"]
    location_project_number = request.form["location_project_number"]
    
    try:
        location_data = LocationData(location_id=location_id,location_name=location_name,
                                     location_state=location_state,
                                     location_project_number=location_project_number)
        
        db.session.add(location_data)
        db.session.commit()
        
    except Exception as e:
        flash(f"Got an error: {e}", "warning")
        return render_template("add_location.html", title="Add Location")
    
    return render_template("add_location.html", title="Add Location")

# This is a decorator to change the data of location. Its function call is present in bosslogin.html. 
@app.route("/change_location", methods=["POST"])
def change_location():                                                        # Return the webpage where we can change the data of location 
    return render_template("change_location.html", title="Change Location") 


@app.route("/search_location", methods=["POST"])
def search_location():
    option_location = "location_id"
    search_attribute_location = request.form["search_attribute_location"]
    
    selected_location = LocationData.query.filter_by(location_id = search_attribute_location).first()
    
    return render_template("update_location.html", title = "Update Location", option_location=option_location,search_attribute_location=search_attribute_location,
                           selected_location=selected_location)
    
@app.route("/update_location", methods=["POST"])
def update_location():
    return render_template("update_location.html", title="Update Location")


@app.route("/submit_change_location/<string:id>", methods=["GET", "POST"])
def submit_change_location(id):
    location = LocationData.query.filter_by(location_id=id).first()
    
    if request.form["location_id"]:
        location.location_id = request.form['location_id']
    if request.form["location_name"]:
        location.location_name = request.form['location_name']
    if request.form["location_state"]:
        location.location_state = request.form['location_state']
    if request.form["location_project_number"]:
        location.location_project_number = request.form['location_project_number']
    db.session.commit()
    
    return render_template("/change_location.html", title="Change Location")



############################################## Add/Update Project #########################################


# This is a decorator to add a new project. Its function call is present in bosslogin.html. 
@app.route("/add_project", methods=["POST"])
def add_project():                                                           # Return the webpage where we can add a new location 
    return render_template("add_project.html", title="Add Project") 


@app.route("/submit_new_project", methods = ["POST"])
def submit_new_project():
    project_id = request.form["project_id"]
    project_name = request.form["project_name"]
    site_id = request.form["site_id"]
    location_id = request.form["location_id"]
    site_eng_id = request.form["site_eng_id"]
    supervisor_id = request.form["supervisor_id"]
    total_workers = request.form["total_workers"]
    
    try:
        project_data = ProjectData(project_id=project_id,project_name=project_name,
                                   site_id=site_id,location_id=location_id,
                                     site_eng_id=site_eng_id,
                                     supervisor_id=supervisor_id,total_workers=total_workers)
        
        db.session.add(project_data)
        db.session.commit()
        
    except Exception as e:
        flash(f"Got an error: {e}", "warning")
        return render_template("add_project.html", title="Add Project")
    
    return render_template("add_project.html", title="Add Project")

# This is a decorator to change the data of project. Its function call is present in bosslogin.html. 
@app.route("/change_project", methods=["POST"])
def change_project():                                                        # Return the webpage where we can change the data of location 
    return render_template("change_project.html", title="Change Project") 


@app.route("/search_project", methods=["POST"])
def search_project():
    option_project = "project_id"
    search_attribute_project = request.form["search_attribute_project"]
    
    selected_project = ProjectData.query.filter_by(project_id = search_attribute_project).first()
    
    return render_template("update_project.html", title = "Update Project", option_project=option_project,search_attribute_project=search_attribute_project,
                           selected_project=selected_project)
    
@app.route("/update_project", methods=["POST"])
def update_project():
    return render_template("update_project.html", title="Update Project")


@app.route("/submit_change_project/<string:id>", methods=["GET", "POST"])
def submit_change_project(id):
    project = ProjectData.query.filter_by(project_id=id).first()
    
    if request.form["project_id"]:
        project.project_id = request.form['project_id']
    if request.form["project_name"]:
        project.project_name = request.form['project_name']
    if request.form["site_id"]:
        project.site_id = request.form['project_id']
    if request.form["location_id"]:
        project.location_id = request.form['location_id']
    if request.form["site_eng_id"]:
        project.site_eng_id = request.form['site_eng_id']
    if request.form["supervisor_id"]:
        project.supervisor_id = request.form['supervisor_id']
    if request.form["total_workers"]:
        project.total_workers = request.form['total_workers']
    db.session.commit()
    
    return render_template("/change_project.html", title="Change Project")


############################################## Add/Update Site #########################################


# This is a decorator to add a new site. Its function call is present in bosslogin.html. 
@app.route("/add_site", methods=["POST"])
def add_site():                                                           # Return the webpage where we can add a new location 
    return render_template("add_site.html", title="Add Site") 


@app.route("/submit_new_site", methods = ["POST"])
def submit_new_site():
    site_id = request.form["site_id"]
    site_name = request.form["site_name"]
    location_id = request.form["location_id"]
    site_pincode = request.form["site_pincode"]
    site_project_number = request.form["site_project_number"]
    
    try:
        site_data = SiteData(site_id=site_id,site_name=site_name,location_id=location_id,
                             site_pincode=site_pincode,site_project_number=site_project_number)
        
        db.session.add(site_data)
        db.session.commit()
        
    except Exception as e:
        flash(f"Got an error: {e}", "warning")
        return render_template("add_site.html", title="Add Site")
    
    return render_template("add_site.html", title="Add Site")

# This is a decorator to change the data of site. Its function call is present in bosslogin.html. 
@app.route("/change_site", methods=["POST"])
def change_site():                                                        # Return the webpage where we can change the data of location 
    return render_template("change_site.html", title="Change Site") 


@app.route("/search_site", methods=["POST"])
def search_site():
    option_site = "site_id"
    search_attribute_site = request.form["search_attribute_site"]
    
    selected_site = SiteData.query.filter_by(site_id = search_attribute_site).first()
    
    return render_template("update_site.html", title = "Update Site", option_site=option_site,search_attribute_site=search_attribute_site,
                           selected_site=selected_site)
    
@app.route("/update_site", methods=["POST"])
def update_site():
    return render_template("update_site.html", title="Update Site")


@app.route("/submit_change_site/<string:id>", methods=["GET", "POST"])
def submit_change_site(id):
    site = SiteData.query.filter_by(site_id=id).first()
    
    if request.form["site_id"]:
        site.site_id = request.form['site_id']
    if request.form["site_name"]:
        site.site_name = request.form['site_name']
    if request.form["location_id"]:
        site.location_id = request.form['location_id']
    if request.form["site_pincode"]:
        site.site_project = request.form['site_pincode']
    if request.form["site_project_number"]:
        site.site_project_number = request.form['site_project_number']
    db.session.commit()
    
    return render_template("/change_site.html", title="Change Site")



################################################### Salary System #########################

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



#########################################                     Attendance System                      #################
# This is a decorator to check the attendance. Its function call is present in bosslogin.html. 
@app.route("/check_attendance", methods=["POST"])
def check_attendance():                                                                    # Return the webpage where we can check the attndance
    return render_template("check_attendance.html", title="Check Attendance") 



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Attendance system @@@@@@@@@@@@@@@@@@@@@@@@@@@
@app.route("/take_morning_attendance/<string:id>", methods = ["POST"])
def take_morning_attendance(id):
    
    if id != None:
        worker_attendance = WorkerDetail.query.filter_by(project_id=id).all()
        project_id = worker_attendance[0].project_id
    else:
        worker_attendance = WorkerDetail.query.all()
    
    try:
        site_name = ProjectData.query.filter_by(project_id = project_id).first()
        site_name = site_name.project_name
    except Exception as e:
        site_name = "All"
    
    
    date_time = datetime.now()
    attendance_date = date_time.strftime("%d/%m/%Y")
    return render_template("take_morning_attendance.html", title ="Take Attendance", worker_attendance=worker_attendance, site_name = site_name, attendance_date = attendance_date, login_site_id=id)


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~` Sample`
@app.route("/submit_morning_attendance/<string:id>", methods = ["POST"])
def submit_morning_attendace(id):
     # If time is between 10 PM to 4 AM, delete the database
    current_time = datetime.now().hour
    # if current_time in [22, 23, 0, 1, 2, 3, 4]:
    db.session.query(WorkerTodayMorningAttendance).delete()
    db.session.commit()
    
    present_workers = request.form.getlist("present")
    if id != None:
        all_workers = WorkerDetail.query.filter_by(project_id=id).all()
    else:
        all_workers = WorkerDetail.query.all()
    
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
@app.route("/take_evening_attendance/<string:id>", methods = ["POST"])
def take_evening_attendance(id):
    if id != None:
        worker_attendance = WorkerDetail.query.filter_by(project_id=id).all()
        project_id = worker_attendance[0].project_id
    else:
        worker_attendance = WorkerDetail.query.all()
    
    try:
        site_name = ProjectData.query.filter_by(project_id = project_id).first()
        site_name = site_name.project_name
    except:
        site_name = "All"
    date_time = datetime.now()
    attendance_date = date_time.strftime("%d/%m/%Y")
    return render_template("take_evening_attendance.html", title ="Take Attendance", worker_attendance=worker_attendance, site_name = site_name, attendance_date = attendance_date, login_site_id=id)


################## Work on this
@app.route("/submit_evening_attendance/<string:id>", methods = ["POST"])
def submit_evening_attendace(id):
    
    # If time is between 10 PM to 4 AM, delete the database
    current_time = datetime.now().hour
    # if current_time in [22, 23, 0, 1, 2, 3, 4]:
    db.session.query(WorkerTodayEveningAttendance).delete()
    db.session.commit()
    
    present_workers = request.form.getlist("present")
    overtime_hour_work = request.form.getlist("overtime_hour")
    
    
    if id != None:
        all_workers = WorkerDetail.query.filter_by(project_id=id).all()
    else:
        all_workers = WorkerDetail.query.all()
    
    
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
@app.route("/add_full_day_attendance/<string:id>", methods = ["POST"])
def add_full_day_attendance(id):
    if id != None:
        worker_attendance = WorkerDetail.query.filter_by(project_id=id).all()
        project_id = worker_attendance[0].project_id
        worker_ids = [i.worker_id for i in worker_attendance]
    else:
        worker_attendance = WorkerDetail.query.all()
        project_id = worker_attendance[0].project_id
        worker_ids = [i.worker_id for i in worker_attendance]
        
    
    morning_attendance = WorkerTodayMorningAttendance.query.filter(WorkerTodayMorningAttendance.worker_id.in_(worker_ids)).order_by(WorkerTodayMorningAttendance.worker_id).all()
    evening_attendance = WorkerTodayEveningAttendance.query.filter(WorkerTodayEveningAttendance.worker_id.in_(worker_ids)).order_by(WorkerTodayEveningAttendance.worker_id).all()
    
    for i in evening_attendance:
        attendance = WorkerAttendance(row_id = random.randint(1, 1000),
                                      worker_id = i.worker_id,
                                      attendance_date = i.attendance_date,
                                      attendance_month = str(calendar.month_name[date.today().month]),
                                      attendance_year = str(datetime.now().year),
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


@app.route("/view_boss", methods = ["POST"])
def view_boss():
    boss_detail = Boss.query.all()
    
    return render_template("view_boss.html", title = "View Boss Details", 
                           boss_detail=boss_detail)
