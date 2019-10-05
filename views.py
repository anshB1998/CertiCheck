import os
from app import app
from flask import Flask, flash, request, redirect, render_template, session, jsonify
from werkzeug.utils import secure_filename
import csv

# Mugdha imports for Merkle Tree
import hashlib
from math import sqrt
from merkletools import MerkleTools
import json
import ast

# Prachiti Resume Parser
from resumeParser import ResumeParser

UNIVERSITY_ALLOWED_EXTENSIONS = set(['csv'])
VERIFIER_ALLOWED_EXTENSIONS = set(['pdf', 'json'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in UNIVERSITY_ALLOWED_EXTENSIONS

def allowed_verification_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in VERIFIER_ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
	universities = ['VJTI', 'IITB', 'KJSCE']
	if request.method == 'POST':
		username = request.form['username']
		session['logged_in'] = True
		session['username'] = username
		return render_template('upload.html', universities=universities)
	return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	
	universities = ['VJTI', 'IITB', 'KJSCE']
	if request.method == 'POST':
		if 'file' not in request.files:
			flash("No file selected", "danger")
			error = "No file selected"
			return render_template('upload.html', universities=universities, error = error)
		file = request.files['file']
		if file.filename == '':
			flash("No file selected", "error")
			return render_template('upload.html', universities=universities)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['CSV_FOLDER'], filename))
			
			#Merkle Tree init
			mt = MerkleTools(hash_type='sha3_256')
			count = 0

			with open(os.path.join(app.config['CSV_FOLDER'], filename)) as File:  
				reader = csv.reader(File)
				for row in reader:
					
					#studentID CPI Name batch college
					data = str(row[0]) + str(row[2]) + str(row[1]) + str(row[3]) + session['username']
					mt.add_leaf(data, do_hash= True)
					count += 1

			mt.make_tree()
			# if mt.get_leaf_count() != count:
				# print("not equal")
				# print(count, mt.get_leaf_count())
			if mt.get_tree_ready_state:
				merkleRoot = mt.get_merkle_root()
			print(merkleRoot)

			itr = 0

			with open(os.path.join(app.config['CSV_FOLDER'], filename)) as File:  
				reader = csv.reader(File)
				for row in reader:
					data={}
					data["cpi"] = str(row[2])
					data["name"] = str(row[1])
					data["year"] = str(row[3])
					data["studentId"] = str(row[0])
					data["institution"] = session['username']
					data["merklePath"] = mt.get_proof(itr)
					itr += 1

					filename = str(row[1]) + '.json'

					with open(os.path.join(app.config['RECEIPT_FOLDER'], filename), 'w') as json_file:
						json_file.write(json.dumps(data))
					
				flash("Successfully uploaded!", "success")
					
	return render_template('upload.html', universities=universities)

@app.route('/verify', methods=['GET', 'POST'])
def verify():
	if request.method == 'POST':
		if 'json' not in request.files or 'pdf' not in request.files:
			flash("All files not selected", "danger")
			return render_template('verify.html')
		jsonFile = request.files['json']
		pdf = request.files['pdf']
		if jsonFile.filename == '' or pdf.filename == '':
			flash("All files not selected", "danger")
			return render_template('verify.html')
		if jsonFile and allowed_verification_file(jsonFile.filename) and pdf and allowed_verification_file(pdf.filename):
			json_name = secure_filename(jsonFile.filename)
			jsonFile.save(os.path.join(app.config['JSON_FOLDER'], json_name))
			pdf_name = secure_filename(pdf.filename)
			pdf.save(os.path.join(app.config['RESUME_FOLDER'], pdf_name))
			resumeJsonData = ResumeParser.parse(os.path.join(app.config['RESUME_FOLDER'], pdf_name))

			with open(os.path.join(app.config['JSON_FOLDER'], json_name)) as receiptJson:
				receiptJsonData = json.loads(receiptJson.read())

			if resumeJsonData["cpi"] != receiptJsonData["cpi"] or resumeJsonData["name"] != receiptJsonData["name"] or resumeJsonData["year"] != receiptJsonData["year"]:
				flash("Details don't match", "danger")
			else:
				flash("Details match", "success")

	return render_template('verify.html')
