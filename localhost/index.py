#
# Copyright (c) 2020 | Sathiyajith KS & Mathana Kumar S
#

"""flask.ipynb"""

from flask import *
import pdfconvert
import PyPDF2
import table_extraction1
import cv2
import shutil
import os
from flask_ngrok import run_with_ngrok

"""**PDF To Image**"""

"""
pdfconvert
  This module is for converting pdf to image page by page
  For more info, refer to pdfconvert.py
"""

def pdfsection(filepath):
  """
  This module is used to convet pd to image
  Parameters:  
            String : Path to the input pdf
"""
  pdfFileObj = open(filepath,"rb")
  pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
  numPages = pdfReader.numPages 
  imgpath = "output/dataset1/"
  pdfconvert.convert2pdf(filepath,imgpath)
  return numPages

"""**TABLE EXTRACTION**"""

"""
table_extraction1
  This module is for extracting table.
  For more info, refer to table_extraction1.py
"""

def tablesection(numPages):
  """
  This module is for extracting table from input image.
  Parameters:  
            int : The number of pages in invoice.
"""
  for i in range(1,numPages+1):
    srcpath = "output/dataset1/"+str(i)+'.jpg'#img from sourcepath to excel in excelpath
    excelpath = "output/dataset1/excel"+str(i)+".xlsx"
    croppath = "output/dataset1/cropped"+str(i)+".jpg"
    destpath = "output/dataset1/desttable"+str(i)+".png"  
    cropped,data = table_extraction1.textExtraction(srcpath,excelpath,destpath)
    cv2.imwrite(croppath,cropped)

"""**DIGITAL IMAGE PROCESSING**"""

import digital_processing
"""
digital_processing
  This module is for applying threshold and processing image.
  For more info, refer to digital_processing.py
"""

"""**TEXT EXTRACTION**"""

import text_extraction
"""
text_extraction
  This module is for extracting text from  cropped image.
  For more info, refer to text_extraction.py
"""

def textsection(numPages):
  """
  This module is for extracting text from  cropped image.
  Parameters:  
            int : The number of pages in invoice.
"""
  for i in range(1,numPages+1):
    imgpath = "output/dataset1/cropped"+str(i)+".jpg"
    digital_processing.threshAndConvert(imgpath)
    destpath = "output/dataset1/excel"+str(i)+".png"
    textimg = "output/dataset1/desttxt"+str(i)+".png"
    header = text_extraction.formatText(imgpath,textimg,destpath)

"""**DOWNLOAD INVOICE ASSETS**"""

def downloadAll(dirpath,output):
  shutil.make_archive(output, 'zip', dirpath)
  return output

#downloadAll("/content/drive/My Drive/hack_space/output/dataset1","/content/drive/My Drive/hack_space/output/dt1")

"""**START E-INVOICE WEB-SERVER**"""

app = Flask(__name__)
app.secret_key = os.urandom(24)
app._static_folder = "static"
run_with_ngrok(app)   #starts ngrok when the app is run
numPages = 0

@app.route('/', defaults={'convertbutton': "true",'downloadbutton': "false"})
@app.route("/<convertbutton>/<downloadbutton>")
def home(convertbutton,downloadbutton):
    return render_template("index.html",convertbutton=convertbutton,downloadbutton=downloadbutton)

@app.route("/upload", methods = ['POST'])  
def upload():
  if request.method == 'POST':
    if 'file' not in request.files:
      print("File Upload Error")
    else:
      file = request.files['file']
      filepath = "output/dataset1/invoice.pdf"
      file.save(filepath)
      print("File Saved at "+filepath)
      numPages = pdfsection(filepath)
      tablesection(numPages)
      print("Upload Ends")
    return redirect(url_for("home",convertbutton="false",downloadbutton="false"))  

@app.route('/download/<path:site>/<convertbutton>/<downloadbutton>')
def download(site,convertbutton,downloadbutton):
  url = '/'+site
  return render_template("index.html",site=url,convertbutton=convertbutton,downloadbutton=downloadbutton)


@app.route('/convert', methods = ['POST'])  
def convert():  
  if request.method == 'POST':
    textsection(numPages)
    site = downloadAll("output/dataset1","output/dt1")
    site = site[1:]
    print('Successfully Converted')
    return redirect(url_for("download",site=site,convertbutton="true",downloadbutton="true"))

app.run()

"""**RUN PYTHON**"""