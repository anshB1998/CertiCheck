from flask import Flask

# Change the path
UPLOAD_FOLDER = '/home/mugdha/Projects/KJSCE Hack 19/CertiCheck/static/certificate'
RECEIPT_FOLDER = '/home/mugdha/Projects/KJSCE Hack 19/CertiCheck/static/receipt'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RECEIPT_FOLDER'] = RECEIPT_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
