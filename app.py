from flask import Flask

# Change the path
# UPLOAD_FOLDER = '/home/mugdha/Projects/KJSCE Hack 19/CertiCheck/static/certificate'
RECEIPT_FOLDER = '/home/mugdha/Projects/KJSCE Hack 19/CertiCheck/static/receipt'
CSV_FOLDER = '/home/mugdha/Projects/KJSCE Hack 19/CertiCheck/static/certificate'
JSON_FOLDER = '/home/mugdha/Projects/KJSCE Hack 19/CertiCheck/static/json'
RESUME_FOLDER = '/home/mugdha/Projects/KJSCE Hack 19/CertiCheck/static/resume'

app = Flask(__name__)
app.secret_key = "secret key"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RECEIPT_FOLDER'] = RECEIPT_FOLDER
app.config['CSV_FOLDER'] = CSV_FOLDER
app.config['JSON_FOLDER'] = JSON_FOLDER
app.config['RESUME_FOLDER'] = RESUME_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
