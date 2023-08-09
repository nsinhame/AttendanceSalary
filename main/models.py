from datetime import datetime
from main import db, app
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

class WorkerPrimary(db.Model):
    worker_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False)
    worker_name = db.Column(db.String(35), unique = False, primary_key = False, nullable = False)

class WorkerDetail(db.Model):
    worker_id = db.Column(db.String(6), db.ForeignKey("WorkerPrimary.worker_id"), primary_key = True, nullable = False)
    worker_name = db.Column(db.String(35), db.ForeignKey("WorkerPrimary.worker_name"), nullable = False)
    worker_phone_number = db.Column(db.Integer, nullable = False, unique = True)
    worker_address = db.Column(db.String(50), nullable = False, unique = False)
    worker_aadhar_number = db.Column(db.Integer, nullable = False, unique = True)
    worker_account_number = db.Column(db.Integer, nullable = False, unique = False)
    worker_ifsc_code = db.Column(db.String(12), nullable = False, unique = False)
    worker_bank_name = db.Column(db.String(35), nullable = False, unique = True)
    worker_bank_branch_name = db.Column(db.String(40), nullable = False, unique = True)
    woker_join_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow, unique = False)
    worker_salary = db.Column(db.Integer, nullable = False, unique = False) #per day
    supervisor_id = db.Column(db.String(35), db.ForeignKey("SupervisorDetail.supervisor_id"), nullable = False, unique = False)
    site_id = db.Column(db.String(6), db.ForeignKey("SiteData.site_id"), nullable = False, unique = False)
    # Still working can be Y (yes), N (no), L (on leave)
    still_working = db.Column(db.String(1), nullable = False, unique = False)

class WorkerTodayAttendance(db.Model):
    worker_id = db.Column(db.String(6), db.ForeignKey("WorkerPrimary.worker_id"), primary_key = True, nullable = False)
    ## Attendance status can be Present, Absent, HalfTime
    attendance_status = db.Column(db.String(1), nullable = False, unique = False)
    attendance_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow, unique = False)
    did_overtime = db.Column(db.String(1), nullable = False, unique = False)
    overtime_today = db.Column(db.Integer, nullable = True, unique = False)


class WorkerAttendance(db.Model):
    row_id = db.Column(db.String(6), primary_key = True, nullable = False)
    worker_id = db.Column(db.String(6), db.ForeignKey("WorkerPrimary.worker_id"), nullable = False)
    attendance_date = db.Column(db.Integer, nullable = False, unique = False)
    attendance_month = db.Column(db.Integer, nullable = False, unique = False)
    attendance_year = db.Column(db.Integer, nullable = False, unique = False)
    overtime_hours = db.Column(db.Integer, nullable = False, unique = False)
    attendance_status = db.Column(db.String(1), db.ForeignKey("WorkerTodayAttendance.attendance_status"), nullable = False, unique = False)

class WorkerSalary(db.Model):
    worker_id = db.Column(db.String(6), db.ForeignKey("WorkerPrimary.worker_id"), primary_key = True, nullable = False)
    monthly_salary = db.Column(db.Integer, nullable = False, unique = False)
    overtime_salary = db.Column(db.Integer, nullable = False, unique = False)
    total_salary = db.Column(db.Integer, nullable = False, unique = False)
    advance_salary = db.Column(db.Integer, nullable = True, unique = False)
    

class LocationData(db.Models):
    location_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False)
    location_name = db.Column(db.String(30), nullable = False, unique = False)
    location_state = db.Column(db.String(30), nullable = False, unique = False)
    location_project_number = db.Colunm(db.Integer, nullable = False, unique = False)

class SiteData(db.Models):
    site_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False)
    site_name = db.Column(db.String(30), nullable = False, unique = True)
    location_id = db.Column(db.String(6), db.ForeignKey("LocationData.location_id"), nullable = False, unique = True)
    site_pincode = db.Column(db.Integer, nullable = False, unique = False)
    site_project_number = db.Column(db.Integer, nullable = False, unique = False)

class ProjectData(db.Model):
    project_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False)
    project_name = db.Column(db.String(30), nullable = False, unique = False)
    site_id = db.Column(db.String(6), db.ForeignKey("SiteData.site_id"), nullable = False, unique = True)
    location_id = db.Column(db.String(6), db.ForeignKey("LocationData.location_id"), nullable = False, unique = True)
    site_eng_id = db.Column(db.String(6), db.ForeignKey("SiteEngineerDetail.site_eng_id"), nullable = False, unique = True)
    supervisor_id = db.Column(db.String(6), db.ForeignKey("SupervisorDetail.supervisor_id"), nullable = False, unique = True)
    total_workers = db.Column(db.Integer, nullable = False, unique = False)

class SiteEngineerDetails(db.Model):
    site_eng_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False)
    site_eng_name = db.Column(db.String(30), nullable = False, unique = False)
    site_eng_phone = db.Column(db.Integer, nullable = False, unique = True)
    location_id = db.Column(db.String(6), db.ForeignKey("LocationData.location_id"), nullable = False, unique = True)
    site_id = db.Column(db.String(6), db.ForeignKey("SiteData.site_id"), nullable = False, unique = True)
    project_id = db.Column(db.String(6), db.ForeignKey("ProjectData.project_id"), nullable = False, unique = True)
    site_eng_email = db.Column(db.String(40), nullable = False, unique = True)
    site_eng_password = db.Column(db.String(20), nullable = False, unique = False)

class SupervisorData(db.Model):
    supervisor_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False)
    supervisor_name = db.Column(db.String(30), nullable = False, unique = False)
    supervisor_phone = db.Column(db.Integer, nullable = False, unique = True)
    location_id = db.Column(db.String(6), db.ForeignKey("LocationData.location_id"), nullable = False, unique = True)
    site_id = db.Column(db.String(6), db.ForeignKey("SiteData.site_id"), nullable = False, unique = True)
    project_id = db.Column(db.String(6), db.ForeignKey("ProjectData.project_id"), nullable = False, unique = True)
    supervisor_email = db.Column(db.String(40), nullable = False, unique = True)
    supervisor_password = db.Column(db.String(20), nullable = False, unique = False)
    site_eng_id = db.Column(db.String(6), db.ForeignKey("SiteEngineerData.site_eng_id"), nullable = False, unique = True)

class Boss(db.Model):
    boss_id = db.Column(db.String(6), unique = True, primary_key = True, nullable = False)
    boss_name = db.Column(db.String(30), nullable = False, unique = False)
    boss_email = db.Column(db.String(40), nullable = False, unique = True)
    boss_password = db.Column(db.String(20), nullable = False, unique = False)
