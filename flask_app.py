__author__ = "Joshua Akangah"

from flask import Flask, render_template, url_for, redirect, request
import datetime
from config import *
from models import *
import os
import logging
from logging.handlers import RotatingFileHandler
import datetime

app = Flask(__name__)
app.config['IMAGE_UPLOADS'] = 'static/img/uploads'
handler = RotatingFileHandler('clinic.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

session = "TEST"

db = Database()

@app.route('/', methods=['GET', 'POST'])
def index():
	data = {
		"session":session
	}
	if request.method == 'POST':
		iD = request.form.get('id')
		name = request.form.get('name')
		age = request.form.get('age')
		gender = request.form.get('sex')
		email = request.form.get('email')
		contact = request.form.get('contact')
		address = request.form.get('address')
		pwd = gen_pass()
		image = request.files['img']
		if db.add_patient(iD, name, age, gender, email, contact, address):
			if db.add_auth(iD, pwd):
				app.logger.info(f"Student {iD} registered for clinical exam at {datetime.datetime.today()} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")
				image.save(os.path.join(app.config['IMAGE_UPLOADS'], f'{iD}.png'))
				# image.save(f'/home/jakangah/clinical/static/img/uploads/{iD}.png')
				data['msg'] = 'success'
				data['pwd'] = pwd
				return render_template('msg.html', **data)
		data['msg'] = 'error'
		return render_template('msg.html', **data)
	return render_template('index.html', **data)

@app.route('/home/<session>/<staff>', methods=['GET','POST'])
def home(session, staff):
	data = {
		"session":session,
		"patients":db.retrieve_patients(),
		"count":db.count_patient(),
		"med":db.count_med(),
		"app":db.count_appointment(),
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}

	app.logger.info(f"Staff {data['inf']} logged in at {datetime.datetime.today()} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")

	return render_template('admin.html', **data)

@app.route('/weight_height/<session>/<staff>', methods=['GET','POST'])
def weight(session, staff):
	data = {
		"session":session,
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	if request.method == 'POST':
		iD = request.form.get('id')		
		weight = request.form.get('weight')		
		height = request.form.get('height')		

		if db.validate_patient(iD):
			if db.add_patient_wh(iD, weight, height):
				data['msg'] = 'success'
				app.logger.info(f"Staff {data['inf']} added data for patient {iD} at {datetime.datetime.today()} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")

				return render_template('weight_height.html', **data)
			data['msg'] = 'error'
			return render_template('weight_height.html', **data)
		data['msg'] = 'none'
		return render_template('weight_height.html', **data)
		
	return render_template('weight_height.html', **data)

@app.route('/blood_pressure/<session>/<staff>', methods=['GET','POST'])
def blood_pressure(session, staff):
	data = {
		"session":session,
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	if request.method == 'POST':
		iD = request.form.get('id')		
		sys = request.form.get('systolic')
		dias = request.form.get('diastolic')
		if db.validate_patient(iD):
			if db.add_patient_bp(iD, sys, dias):
				data['msg'] = 'success'
				app.logger.info(f"Staff {data['inf']} added data for patient {iD} at {datetime.datetime.today()} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")

				return render_template('blood_pressure.html', **data)
			data['msg'] = 'error'
			return render_template('blood_pressure.html', **data)
		data['msg'] = 'none'
		return render_template('blood_pressure.html', **data)
		
	return render_template('blood_pressure.html', **data)

@app.route('/eye_reading/<session>/<staff>', methods=['GET','POST'])
def eye_reading(session, staff):
	data = {
		"session":session,
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	if request.method == 'POST':
		iD = request.form.get('id')		
		left = request.form.get('left')
		right = request.form.get('right')
		if db.validate_patient(iD):
			if db.add_patient_eye(iD, right, left):
				data['msg'] = 'success'
				app.logger.info(f"Staff {data['inf']} added data for patient {iD} at {datetime.datetime.today()} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")

				return render_template('eye_reading.html', **data)
			data['msg'] = 'error'
			return render_template('eye_reading.html', **data)
		data['msg'] = 'none'
		return render_template('eye_reading.html', **data)
	return render_template('eye_reading.html', **data)

@app.route('/blood_sample/<session>/<staff>', methods=["GET", 'POST'])
def blood_sample(session, staff):
	data = {
		"session":session,
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	if request.method == 'POST':
		iD = request.form.get('id')	
		rbc = request.form.get('rbc')
		wbc = request.form.get('wbc')
		sick = request.form.get('sick')
		bg = request.form.get('group')
		std = request.form.get('std')

		if db.validate_patient(iD):
			if db.add_patient_blood(iD, rbc, wbc, sick, bg, None, std):
				app.logger.info(f"Staff {data['inf']} added data for patient {iD} at {datetime.datetime.today()} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")

				data['msg'] = 'success'
				return render_template('blood_sample.html', **data)
			data['msg'] = 'error'
			return render_template('blood_sample.html', **data)
		data['msg'] = 'none'
		return render_template('blood_sample.html', **data)
	return render_template('blood_sample.html', **data)

@app.route('/urine_sample/<session>/<staff>', methods=['GET', 'POST'])
def urinalysis(session, staff):
	data = {
		"session":session,
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	if request.method == 'POST':
		iD = request.form.get('id')	
		ph = request.form.get('ph')
		gravity = request.form.get('gravity')
		if db.validate_patient(iD):
			if db.add_patient_urinalysis(iD, ph, gravity):
				data['msg'] = 'success'
				app.logger.info(f"Staff {data['inf']} added data for patient {iD} at {datetime.datetime.today()} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")

				return render_template('urinalysis.html', **data)
			data['msg'] = 'error'
			return render_template('urinalysis.html', **data)
		data['msg'] = 'none'
		return render_template('urinalysis.html', **data)
	return render_template('urinalysis.html', **data)

@app.route('/x_ray/<session>/<staff>', methods=['GET', 'POST'])
def x_ray(session, staff):
	data = {
		"session":session,
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	if request.method == 'POST':
		iD = request.form.get('id')
		remark = request.form.get('remark')
		image = request.files['img']
		if db.validate_patient(iD):
			if db.add_x_ray(iD, remark):
				#image.save(f'/home/jakangah/clinical/static/img/uploads/{iD}_x_ray.png')
				image.save(os.path.join(app.config['IMAGE_UPLOADS'], f'{iD}_x_ray.png'))
				data['msg'] = 'success'
				app.logger.info(f"Staff {data['inf']} added data for patient {iD} at {datetime.datetime.today()} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")

				return render_template('x_ray.html', **data)
			data['msg'] = 'error'
			return render_template('x_ray.html', **data)
		data['msg'] = 'none'
		return render_template('x_ray.html', **data)
	return render_template('x_ray.html', **data)

@app.route('/activity/<session>/<staff>', methods=['GET', 'POST'])
def activity(session, staff):
	items = []
	with open('clinic.log', 'r') as file:
		for line in file:
			items.append(line)
	data = {
		"session":session,
		"log":items,
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	return render_template('log.html', **data)

@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
	data = {
		"session":session
	}

	if request.method == 'POST':
		iD = request.form.get('id')
		passw = request.form.get('passw')
		if db.validate_login(iD, passw):
			app.logger.info(f"Student {iD} logged in at {datetime.datetime.today()} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")

			return redirect(f'/student_check/{iD}/{session}')
		data['msg'] = 'error'
		return render_template('login.html', **data)
	return render_template('login.html', **data)

@app.route('/login_staff', methods=['GET', 'POST'])
def login_staff():
	data = {
		"session":session,
		"inf":"NULL"
	}

	if request.method == 'POST':
		iD = request.form.get('id')
		passw = request.form.get('passw')
		if db.validate_login(iD, passw):
			app.logger.info(f"Staff {data['inf']} logged in at {datetime.datetime.today()} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")

			return redirect(f'/home/{session}/{iD}')
		data['msg'] = 'error'
		return render_template('staff.html', **data)
	return render_template('staff_login.html', **data)

@app.route('/login', methods=['GET', 'POST'])
def login():
	data = {
		"session":session,
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	return render_template('ask_login.html', **data)

@app.route('/student/<student>/<session>/<staff>', methods=['GET', 'POST'])
def student(student, session, staff):
	data = {
		"session":session,
		"patient":db.retrieve_student_data(student),
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	if request.method == 'POST':
		remark = request.form.get('remark')
		if db.add_remark(student, remark):
			data['msg'] = 'success'
			return render_template('student.html', **data)
		data['msg'] = 'error'
		return render_template('student.html', **data)
	return render_template('student.html', **data)

@app.route('/student_check/<student>/<session>/<staff>')
def students(student, session, staff):
	data = {
		"session":session,
		"patient":db.retrieve_student_data(student),
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	return render_template('students.html', **data)

@app.route('/staff_records/<session>/<staff>')
def staff(session, staff):
	data = {
		"session":session,
		"staff":db.retrieve_staff(),
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	return render_template('staff.html', **data)

@app.route('/add_staff/<session>/<staff>', methods=['GET', 'POST'])
def add_staff(session, staff):
	data = {
		"session":session,
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	if request.method == "POST":
		name = request.form.get('name')
		contact = request.form.get('contact')
		title = request.form.get('title')
		image = request.files['img']
		staff_id = gen_id(4)
		pwd = gen_pass()

		if db.add_staff(name, title, staff_id, contact):
			if db.add_auth(staff_id, pwd):
				data['pwd'] = pwd
				#image.save(f'/home/jakangah/clinical/static/img/uploads/{staff_id}.png')
				image.save(os.path.join(app.config['IMAGE_UPLOADS'], f'{staff_id}.png'))
				data['msg'] = 'success'
				return render_template('add_staff.html', **data)
		data['msg'] = 'error'
		return render_template('add_staff.html', **data)
	return render_template('add_staff.html', **data)

@app.route('/appointments/<session>/<staff>')
def appointment(session, staff):
	data = {
		"session":session,
		"appointments":db.retrieve_appointment(),
		"today": datetime.datetime.today().date(),
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	return render_template('appointments.html', **data)

@app.route('/add_appointment/<session>/<staff>', methods=['GET', 'POST'])
def add_appointment(session, staff):
	data = {
		"session":session,
		"staff":db.retrieve_staff(),
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}

	if request.method == 'POST':
		student = request.form.get('patient')
		date = request.form.get('date')
		time = request.form.get('time')
		officer = request.form.get('officer')

		if db.validate_staff(officer):
			if db.validate_patient(student):
				if db.add_appointment(student, officer, date, time):
					data['msg'] = 'success'
					app.logger.info(f"Staff {data['inf']} booked appointment for patient {iD} at {datetime.datetime.today()} on {date} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")

					return render_template('add_appointment.html', **data)
				data['msg'] = 'error'
				return render_template('add_appointment.html', **data)
			data['msg'] = 'nopat'
			return render_template('add_appointment.html', **data)
		data['msg'] = 'nostaff'
		return render_template('add_appointment.html', **data)
	return render_template('add_appointment.html', **data)

@app.route('/medication/<session>/<staff>')
def medication(session, staff):
	data = {
		"session":session,
		"meds":db.retrieve_med(),
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}
	return render_template('medication.html', **data)


@app.route('/add_medication/<session>/<staff>', methods=['GET', 'POST'])
def add_medication(session, staff):
	data = {
		"session":session,
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}

	if request.method == 'POST':
		bat = gen_id(3)
		if db.add_medication(request.form.get("category"), request.form.get('name'), request.form.get('expiry'), request.form.get('stock'), bat):
			data['msg'] = 'success'
			return render_template('add_medication.html', **data)
		data['msg'] = 'error'
		return render_template('add_medication.html', **data)
	return render_template('add_medication.html', **data)

@app.route('/add_prescription/<session>/<staff>', methods=['GET', 'POST'])
def add_prescription(session, staff):
	data = {
		"session":session,
		"staff":db.retrieve_staff(),
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}

	if request.method == 'POST':
		staff = request.form.get('staff')
		patient = request.form.get('patient')
		name = request.form.get('name')
		batch = request.form.get('batch')

		if db.validate_staff(request.form.get('staff')):
			if db.validate_patient(request.form.get('patient')):
				if db.validate_batch(request.form.get('batch')):
					if db.add_prescription(patient, staff, name):
						if db.update_stock(batch) != 'empty':
							data['msg'] = 'success'
							app.logger.info(f"Staff {data['inf']} added prescribed {name} for patient {iD} at {datetime.datetime.today()} from IP {request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}")
							return render_template('add_prescription.html', **data)
						data['msg'] = 'empty'
						return render_template('add_prescription.html', **data)
					data['msg'] = "error"
					return render_template('add_prescription.html', **data)
				data['msg'] = 'nobat'
				return render_template('add_prescription.html', **data)
			data['msg'] = 'nopat'
			return render_template('add_prescription.html', **data)
		data['msg'] = 'nostaff'
		return render_template('add_prescription.html', **data)
	return render_template('add_prescription.html', **data)

@app.route('/staff/<iD>/<session>/<staff>')
def staff_data(iD, session, staff):
	data = {
		"session":session,
		"staff":db.retrieve_staff_data(iD),
		"today": datetime.datetime.today().date(),
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}

	return render_template('staff_data.html', **data)

@app.route('/add_patient/<session>/<staff>', methods=['GET', 'POST'])
def add_patient(session, staff):
	data = {
		"session":session,
		"info":db.retrieve_staff_data(staff),
		"inf":db.retrieve_staff_data(staff)[0]
	}

	if request.method == "POST":
		image = request.files['img']
		patient_id = gen_id(1)
		name = request.form.get('name')
		address = request.form.get('address')
		gender = request.form.get('sex')
		age = int(request.form.get('age'))
		email = "None"
		contact = "None"
		if db.add_patient(patient_id, name, age, gender, email, contact, address):
			#image.save(f'/home/jakangah/clinical/static/img/uploads/{patient_id}.png')
			image.save(os.path.join(app.config['IMAGE_UPLOADS'], f'{patient_id}.png'))
			data['msg'] = "success"
			return render_template('add_patient.html', **data)
		data['msg'] = "error"
		render_template('add_patient.html', **data)
		return render_template('add_patient.html', **dept)

	return render_template('add_patient.html', **data)

app.run(debug=True)
