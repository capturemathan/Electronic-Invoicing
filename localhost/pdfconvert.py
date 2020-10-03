#
# Copyright (c) 2020 | Sathiyajith KS & Mathana Kumar S
#

"""pdfconvert.ipynb"""
from pdf2image import convert_from_path

def convert2pdf(pdfpath,imgpath):
  """
  The function to convert from pdf to image page by page 
  Parameters: 
            imgpath(String): The path of pdf to be converted.
  """
  pages = convert_from_path(pdfpath, 350)
  i = 1
  for page in pages:
    image_name = imgpath + str(i) + ".jpg"
    page.save(image_name, "JPEG")
    i = i+1
    
#convert2pdf("Sample_Invoice_1.pdf","output/dataset1/")