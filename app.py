from flask import Flask
import os

cwd = os.getcwd()
# Change the path
RECEIPT_FOLDER = os.path.join(cwd, 'static/receipt')
CSV_FOLDER = os.path.join(cwd, 'static/certificate')
JSON_FOLDER = os.path.join(cwd, 'static/json')
RESUME_FOLDER = os.path.join(cwd, 'static/resume')

app = Flask(__name__)
app.secret_key = "secret key"
app.config['RECEIPT_FOLDER'] = RECEIPT_FOLDER
app.config['CSV_FOLDER'] = CSV_FOLDER
app.config['JSON_FOLDER'] = JSON_FOLDER
app.config['RESUME_FOLDER'] = RESUME_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from views import *

if __name__ == "__main__":
	app.run(debug = True)