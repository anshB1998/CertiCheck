import os
from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import csv
# Mugdha imports for Merkle Tree
import hashlib
from math import sqrt
from merkletools import MerkleTools
import json

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
			
			#Merkle Tree init
			mt = MerkleTools(hash_type='sha3_256')
			count = 0

			with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as File:  
				reader = csv.reader(File)
				for row in reader:
					
					data = str(row[0]) + str(row[2]) + str(row[1]) + str(row[3])
					print(data)

					mt.add_leaf(data, do_hash= True)
					count += 1

			mt.make_tree()
			if mt.get_leaf_count() != count:
				print("not equal")
				print(count, mt.get_leaf_count())
			if mt.get_tree_ready_state:
				merkleRoot = mt.get_merkle_root()
			print(merkleRoot)

			itr = 0

			with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as File:  
				reader = csv.reader(File)
				for row in reader:
					print(row)
					data={}
					data["cpi"] = str(row[2])
					data["name"] = str(row[1])
					data["year"] = str(row[3])
					data["studentId"] = str(row[0])
										
					data["merklePath"] = mt.get_proof(itr)
					itr += 1

					filename = str(row[1]) + '.json'

					with open(os.path.join(app.config['RECEIPT_FOLDER'], filename), 'w') as json_file:
						json.dump(data, json_file)

					print(data)
					
	return render_template('home.html', universities=universities)

if __name__ == "__main__":
	app.run(debug = True)
