#
# Copyright (c) 2020 | Sathiyajith KS & Mathana Kumar S
#

"""text_extraction"""

import pytesseract
from PIL import Image,ImageDraw,ImageFont
from textblob import TextBlob
import pandas as pd
import nltk
nltk.download('words')
from nltk.corpus import words
# Replace Tesseract Path with your Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def extractText(imgpath):
  """
  The function to extract raw text from image using tesseract 
  Parameters: 
            imgpath(String): The path of image in which text to be extracted. 
          
        Returns: 
            String: the raw text extracted from image. 
  """
  extractedInformation = pytesseract.image_to_string(Image.open(imgpath))
  return extractedInformation

def writeExcel(string,destpath):
  """
  The function to write text to file 
  Parameters: 
            imgpath(String): The path of image in which text to be extracted. 
            destpath : The path where text to be written  
  """
  dataframe = pd.DataFrame({'header':string})
  df_excel = pd.read_excel(destpath)
  result = pd.concat([dataframe,df_excel], ignore_index=True)
  result.to_excel(destpath, index=True)

def writeImage(string,desttext):
  img = Image.new('RGB', (1000, 500), color = (73, 109, 137)) 
  d = ImageDraw.Draw(img)
  d.text((10,10), string, fill=(255,255,0))
  img.show()  
  img.save(desttext)

def checkWords(string):
  return string in words.words() or len(string)>5

def formatText(imgpath,desttext,destpath):
  """
  The function to remove unwanted text
  Parameters: 
            imgpath(String): The path of image in which text to be cleaned. 
            destpath: The destination path where the text to be written.
        Returns: 
            String: the raw text extracted from image. 
  """
  text = extractText(imgpath)
  s= text.split("\n")
  string = ''
  l = len(s)
  i = 0
  string = ''
  while i<len(s):
    if len(s[i])<=1  or s[i].isspace():
      s.pop(i)
    else:
      if checkWords(s[i]):
        string+=s[i].encode('latin-1', 'ignore').decode()+'\n'
        i+=1
      else:
        s.pop(i)

  writeExcel(s,destpath)
  writeImage(string,desttext)
  return s

formatted = formatText("output/dataset1/cropped1.jpg","output/dataset1/desttext1.png","output/dataset1/excel1.xlsx")

"""**RAW EXTRACTED DATA**"""