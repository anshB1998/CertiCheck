import os
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import csv

UNIVERSITY_ALLOWED_EXTENSIONS = set(['csv'])
VERIFIER_ALLOWED_EXTENSIONS = set(['pdf', 'json'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in UNIVERSITY_ALLOWED_EXTENSIONS

def allowed_verification_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in VERIFIER_ALLOWED_EXTENSIONS

def login():
	if request.method == 'POST':
		username = request.form['username']
	return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	universities = ['VJTI', 'IITB', 'KJSCE']
	login()
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file selected')
			return render_template('home.html', universities=universities)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected')
			return render_template('home.html', universities=universities)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['CSV_FOLDER'], filename))
			with open(os.path.join(app.config['CSV_FOLDER'], filename)) as File:  
				reader = csv.reader(File)
				for row in reader:
					print(row)
	return render_template('home.html', universities=universities)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
	if request.method == 'POST':
		if 'json' not in request.files or 'pdf' not in request.files:
			flash('All files not selected')
			return render_template('verify.html')
		json = request.files['json']
		pdf = request.files['pdf']
		if json.filename == '' or pdf.filename == '':
			flash('All files not selected')
			return render_template('verify.html')
		if json and allowed_verification_file(json.filename) and pdf and allowed_verification_file(pdf.filename):
			json_name = secure_filename(json.filename)
			json.save(os.path.join(app.config['JSON_FOLDER'], json_name))
			pdf_name = secure_filename(pdf.filename)
			pdf.save(os.path.join(app.config['RESUME_FOLDER'], pdf_name))

	return render_template('verify.html')

if __name__ == "__main__":
	app.run(debug = True)
