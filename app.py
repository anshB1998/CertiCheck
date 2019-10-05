from flask import Flask

CSV_FOLDER = '/home/ansh/Desktop/EmployeeVerify/static/certificate'
JSON_FOLDER = '/home/ansh/Desktop/EmployeeVerify/static/json'
RESUME_FOLDER = '/home/ansh/Desktop/EmployeeVerify/static/resume'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['CSV_FOLDER'] = CSV_FOLDER
app.config['JSON_FOLDER'] = JSON_FOLDER
app.config['RESUME_FOLDER'] = RESUME_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
