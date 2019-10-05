import sys
import os
from importlib import reload
import re
from nltk.tokenize import word_tokenize
import csv
import json
from io import StringIO
reload(sys)
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from werkzeug.utils import secure_filename
import hashlib
from app import app

name = []
cpi = []
institution = []
batch = []

def extract_decimals(string):
    r = re.compile(r'\d+\.\d')
    return r.findall(string)


def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    # infile = file(fname, 'rb')
    with open(fname,'rb') as infile:
    	for page in PDFPage.get_pages(infile, pagenums):
        	interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

class ResumeParser:
	def parse(filename):
		resume_string = convert(filename)

		scores = extract_decimals(resume_string)
		print(resume_string)
		cpi.append(scores[0])

		tokens = word_tokenize(resume_string)
		name.append(tokens[0] + " " + tokens[1])

		resume_string = resume_string.replace(',',' ')
		resume_string = resume_string.lower()

		with open('college.csv','r') as f:
		    reader = csv.reader(f)
		    college_list = list(reader)


		for college in college_list:
		    if college[0].lower() in resume_string:
		        institution.append(college[0])

		if re.search(r'\b[21][09][8901][0-9]',resume_string.lower()):
			year = re.findall(r'\b[21][09][8901][0-9]',resume_string.lower())[0]

		data={}
		data["cpi"] = str(cpi[0])
		data["name"] = str(name[0])
		data["year"] = str(year)
		data["institution"] = str(institution[0])

		fileName = str(name[0]) + '.json'
		
		with open(os.path.join(app.config['RESUMEJSON_FOLDER'], fileName), 'w') as outfile:
			json.dump(data, outfile)
		
		return fileName

if __name__ == '__main__':
	resume = ResumeParser('resume1.pdf')