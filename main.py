import os
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import csv

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	universities = ['VJTI', 'IITB', 'KJSCE']
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('Please upload your resume', 'danger')
			return render_template('home.html', universities=universities)
		file = request.files['file']
		if file.filename == '':
			flash('Please upload your resume', 'danger')
			return render_template('home.html', universities=universities)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as File:  
				reader = csv.reader(File)
				for row in reader:
					print(row)

	return render_template('home.html', universities=universities)

if __name__ == "__main__":
	app.run(debug = True)
