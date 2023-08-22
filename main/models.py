# Defining database schemas here

# Import libraries
from datetime import datetime
from main import db, app, login_manager
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return Boss.query.get(int(user_id))



''' Worker Primary is a kind of reference table that hold worker_id and worker_name. The variables
    present in this class is used as foreign key in most of the table.'''
class WorkerPrimary(db.Model):
    __tablename__ = "WorkerPrimary"                                                                 # Name of the table
    worker_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False)        # Worker ID is autogenerated 6 digit string
    worker_name = db.Column(db.String(35), unique = False, primary_key = False, nullable = False)   # Name of the worker




''' Worker Detail contains all the details of the worker. This table uses multiple foreign keys from multiple tables.'''
class WorkerDetail(db.Model):
    __tablename__ = "WorkerDetail"                                                                 # Name of the table
    worker_id = db.Column(db.String(6), db.ForeignKey("WorkerPrimary.worker_id"), primary_key = True, nullable = False)  # Worker ID is a foreign key from Worker Primary table
    worker_name = db.Column(db.String(35), db.ForeignKey("WorkerPrimary.worker_name"), nullable = False)      # Worker name is a foreign key from Worker Primary table
    worker_phone_number = db.Column(db.Integer, nullable = False, unique = True)              # Worker's phone number
    worker_address = db.Column(db.String(50), nullable = False, unique = False)               # Worker's address
    worker_gender = db.Column(db.String(1), nullable = False, unique = False)                 # Worker's gender, can be F (female), M (male) or O (other)
    worker_aadhar_number = db.Column(db.Integer, nullable = False, unique = True)             # Worker's aadhar card number
    # Bank Details for the worker for making a payment                                        
    worker_account_number = db.Column(db.Integer, nullable = False, unique = True)           # Worker's account number
    worker_ifsc_code = db.Column(db.String(12), nullable = False, unique = False)             # Worker's IFSC code
    worker_bank_name = db.Column(db.String(35), nullable = False, unique = False)              # Worker's Bank Name
    worker_bank_branch_name = db.Column(db.String(40), nullable = False, unique = False)       # Worker's Bank Branch Name
    # Bank Details ended
    worker_join_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow, unique = False) # Date of joining
    worker_salary = db.Column(db.Integer, nullable = False, unique = False)                   # Per day salary of the worker
    supervisor_id = db.Column(db.String(35), db.ForeignKey("SupervisorDetails.supervisor_id"), nullable = False, unique = False) # ID of the supervisor they work under
    site_id = db.Column(db.String(6), db.ForeignKey("SiteData.site_id"), nullable = False, unique = False) # Site ID where the worker is working
    still_working = db.Column(db.String(1), nullable = False, unique = False)                 # Still working can be Y (yes), N (no) or L (on leave)



''' Worker Today Attendance contains attendance of only today. It gets reset at after 3 AM everyday. It's data is transfered into 
    Worker Attendance table after every 24 hours.'''
class WorkerTodayAttendance(db.Model):
    __tablename__ = "WorkerTodayAttendance"                                                   # Name of the table
    worker_id = db.Column(db.String(6), db.ForeignKey("WorkerPrimary.worker_id"), primary_key = True, nullable = False)  # Worker ID is a foreign key from Worker Primary table
    attendance_status = db.Column(db.String(1), nullable = False, unique = False)  # Attendance status can be P (Present), A (Absent), or H (Half time)
    attendance_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow, unique = False)  # Date of the attendance
    did_overtime = db.Column(db.String(1), nullable = False, unique = False)                  # Did Overtime can be Y (Yes) or N (No)
    overtime_today = db.Column(db.Integer, nullable = True, unique = False)                   # Overtime Today store an integer value which is the number of hours a worker has worked. It can be roundoff to ciel value.



''' Worker Attendance contains overall attendance of the workers from each and every site.'''
class WorkerAttendance(db.Model):
    __tablename__ = "WorkerAttendance"                                                        # Name of the table
    row_id = db.Column(db.String(6), primary_key = True, nullable = False)                    # Row ID works as a primary key as Worker ID is repeated after every day and hence can be used as a primary key.
    worker_id = db.Column(db.String(6), db.ForeignKey("WorkerPrimary.worker_id"), nullable = False) # Worker ID is a foreign key from Worker Primary table
    attendance_date = db.Column(db.Integer, nullable = False, unique = False)                 # Date of the attendance
    attendance_month = db.Column(db.Integer, nullable = False, unique = False)                # Month of the attendance
    attendance_year = db.Column(db.Integer, nullable = False, unique = False)                 # Year of the attendance
    overtime_hours = db.Column(db.Integer, nullable = False, default = int("0"), unique = False)   # Overtime hours of the worker. If no overtime hours set it as zero.
    attendance_status = db.Column(db.String(1), nullable = False, unique = False)             # Attendance status can be P (Present), A (Absent), or H (Half time)



''' Worker Salary contains the monthly calculated salary of the workers. '''
class WorkerSalary(db.Model):
    __tablename__ = "WorkerSalary"                                                            # Name of the table
    row_id = db.Column(db.String(6), primary_key = True, nullable = True, unique = True)      # Row ID works as a primary key as Worker ID is repeated after every day and hence can be used as a primary key.
    worker_id = db.Column(db.String(6), db.ForeignKey("WorkerPrimary.worker_id"), nullable = False) # Worker ID is a foreign key from Worker Primary table
    month_year = db.Column(db.String(7), nullable = False, unique = False)                    # Month Year contains the combination of month and year so that we can see the month and year of each worker
    monthly_salary = db.Column(db.Integer, nullable = False, unique = False)                  # Monthly salary of the worker
    overtime_salary = db.Column(db.Integer, nullable = False, unique = False)                 # Overtime salary of the worker
    total_salary = db.Column(db.Integer, nullable = False, unique = False)                    # Monthly salary + Overtime salary - Advance Salary
    advance_salary = db.Column(db.Integer, nullable = True, unique = False)                   # Advance taken by the worker
    


''' Location Data contains the data and information of each Location '''
class LocationData(db.Model):
    __tablename__ = "LocationData"                                                            # Name of the table
    location_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False) # ID of the location
    location_name = db.Column(db.String(30), nullable = False, unique = False)                # Name of location
    location_state = db.Column(db.String(30), nullable = False, unique = False)               # State of loction
    location_project_number = db.Column(db.Integer, nullable = False, unique = False)         # Number of projects running on that location



''' Site is like the name of the place where the projects are going on. Site data contains the data and the information of each site '''
class SiteData(db.Model):
    __tablename__ = "SiteData"                                                                # Name of the table
    site_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False)    # ID of the site
    site_name = db.Column(db.String(30), nullable = False, unique = True)                     # Name of the site
    location_id = db.Column(db.String(6), db.ForeignKey("LocationData.location_id"), nullable = False, unique = True) # Location ID being used as a foreign key
    site_pincode = db.Column(db.Integer, nullable = False, unique = False)                    # Pincode of the site
    site_project_number = db.Column(db.Integer, nullable = False, unique = False)             # Number of projects running on that site


''' Project data contains the data and information about the projects '''
class ProjectData(db.Model):
    __tablename__ = "ProjectData"                                                            # Name of the table
    project_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False) # ID of the project
    project_name = db.Column(db.String(30), nullable = False, unique = False)                # Name ot the project
    site_id = db.Column(db.String(6), db.ForeignKey("SiteData.site_id"), nullable = False, unique = True) # ID of the site is used as foreign key
    location_id = db.Column(db.String(6), db.ForeignKey("LocationData.location_id"), nullable = False, unique = True) # ID of the location being used as foreign key
    site_eng_id = db.Column(db.String(6), db.ForeignKey("SiteEngineerDetails.site_eng_id"), nullable = False, unique = True) # Site Engineer ID being used as a foreign key
    supervisor_id = db.Column(db.String(6), db.ForeignKey("SupervisorDetails.supervisor_id"), nullable = False, unique = True) # Suprvisor ID being used as a foreign key
    total_workers = db.Column(db.Integer, nullable = False, unique = False)                  # Total number of workers working on that project



''' Site Engineer Details contain the data of the Site Engineer working at a particular site. Site Engineer is the head of the project. Site
    Engineer have some rights like changing attendance status. Seeing previous attendance, etc. '''
class SiteEngineerDetails(db.Model):
    __tablename__ = "SiteEngineerDetails"                                                   # Name of the table
    site_eng_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False) # ID of the Site Engineer
    site_eng_name = db.Column(db.String(30), nullable = False, unique = False)              # Site Engineer name
    site_eng_phone = db.Column(db.Integer, nullable = False, unique = True)                 # Site Engineer phone number
    location_id = db.Column(db.String(6), db.ForeignKey("LocationData.location_id"), nullable = False, unique = True) # ID of the location where the Site Engineer is working used as a foreign key
    site_id = db.Column(db.String(6), db.ForeignKey("SiteData.site_id"), nullable = False, unique = True) # ID of the site being used as a foreign key
    project_id = db.Column(db.String(6), db.ForeignKey("ProjectData.project_id"), nullable = False, unique = True) # ID of the Project being used as a foreign key
    site_eng_email = db.Column(db.String(40), nullable = False, unique = True)              # Email of the site engineer
    site_eng_password = db.Column(db.String(20), nullable = False, unique = False)          # Password of the site engineer



''' Supervisor Details contain the data of the Supervisor. Supervisor comes under Site Engineer and can only take attendance. '''
class SupervisorDetails(db.Model):
    __tablename__ = "SupervisorDetails"                                                     # Name of the table
    supervisor_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False) # ID of the supervisor
    supervisor_name = db.Column(db.String(30), nullable = False, unique = False)            # Supervisor name
    supervisor_phone = db.Column(db.Integer, nullable = False, unique = True)               # Supervisor Phone number
    location_id = db.Column(db.String(6), db.ForeignKey("LocationData.location_id"), nullable = False, unique = True) # ID of the location where the Site Engineer is working used as a foreign key
    site_id = db.Column(db.String(6), db.ForeignKey("SiteData.site_id"), nullable = False, unique = True) # ID of the site being used as a foreign key
    project_id = db.Column(db.String(6), db.ForeignKey("ProjectData.project_id"), nullable = False, unique = True) # ID of the Project being used as a foreign key
    supervisor_email = db.Column(db.String(40), nullable = False, unique = True)            # Email of the supervisor
    supervisor_password = db.Column(db.String(20), nullable = False, unique = False)        # Password of the supervisor
    site_eng_id = db.Column(db.String(6), db.ForeignKey("SiteEngineerDetails.site_eng_id"), nullable = False, unique = True) # ID of the supervisor being used as foreign key



''' Boss table contains the details of Boss and some subordinates who can control all the data '''
class Boss(db.Model):
    __tablename__ = "Boss"                                                                 # Name of the table
    boss_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False) # ID of the boss
    boss_name = db.Column(db.String(30), nullable = False, unique = False)                 # Name of the boss
    boss_email = db.Column(db.String(40), nullable = False, unique = True)                 # Email of the boss
    boss_password = db.Column(db.String(20), nullable = False, unique = False)             # Password of the boss
