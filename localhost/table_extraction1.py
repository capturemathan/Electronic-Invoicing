#
# Copyright (c) 2020 | Sathiyajith KS & Mathana Kumar S
#
# -*- coding: utf-8 -*-
"""table_extraction1.ipynb"""

import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import six
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import copy
# Replace Tesseract Path with your Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def threshAndConvert(imgpath):
  """
  The function to apply threshold to image.
  Parameters: 
            imgpath(String): The path of image to which threshold to be applied. 

        Returns: 
            array[int] :  input image 
            array[int] :  threshed image 
  """
  img = cv2.imread(imgpath,0)
  thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU) 
  thresh_img = 255-img_bin
  plotting = plt.imshow(thresh_img,cmap='gray')
  plt.show()
  return img,thresh_img

#img,threshed = threshAndConvert("/content/drive/My Drive/hack_space/output/dataset1/1.jpg")

def getLines(img):
  """
  The function to generate two kernels 
  Parameters: 
            array[int] : original image 

        Returns: 
            array[int] : kernel mask to apply masking 
            array[int] : vertical mask to apply masking
            array[int] : horizontal mask to apply masking
  """
  kernel_len = np.array(img).shape[1]//100
  ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
  hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
  return kernel,ver_kernel, hor_kernel

#kernel,vertical,horizontal = getLines(img)

def getVertical(img,vertical):
  """
  The function to apply erosion and dilation with vertical kernal
  Parameters: 
            array[int] : original image 
            array[int] : vertical mask to apply masking

        Returns: 
            array[int] : eroded image            
            array[int] : dilated image
  """
  image_1 = cv2.erode(img, vertical, iterations=3)
  lines = cv2.dilate(image_1, vertical, iterations=3)
  plotting = plt.imshow(image_1,cmap='gray')
  plt.show()
  return image_1,lines

#vert_img , vert_lines= getVertical(threshed,vertical)

def getHorizontal(img,horizontal):
  """
  The function to apply erosion and dilation with horizontal kernal
  Parameters: 
            array[int] : original image 
            array[int] : horizontal mask to apply masking

        Returns: 
            array[int] : eroded image            
            array[int] : dilated image
  """
  image_2 = cv2.erode(img, horizontal, iterations=3)
  lines = cv2.dilate(image_2, horizontal, iterations=3)
  plotting = plt.imshow(image_2,cmap='gray')
  plt.show()
  return image_2,lines

#hor_img, hor_lines = getHorizontal(threshed,horizontal)

def AddWeight(img,vert_lines,hor_lines,kernel):
  """
  The function to perform bit xor and not operations
  Parameters: 
            array[int] : original image 
            array[int] : vertical mask to apply masking
            array[int] : horizontal mask to apply masking
            array[int] : kernel mask to apply masking

        Returns: 
            array[int] : weighted image            
            array[int] : inverted image
  """
  img_vh = cv2.addWeighted(vert_lines, 0.5, hor_lines, 0.5, 0.0)
  img_vh = cv2.erode(~img_vh, kernel, iterations=2)
  thresh, img_vh = cv2.threshold(img_vh,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  bitxor = cv2.bitwise_xor(img,img_vh)
  bitnot = cv2.bitwise_not(bitxor)
  return img_vh, bitnot


#TableImg,bitnot = AddWeight(img,vert_lines,hor_lines,kernel)

def findContours(timg):
  """
  The function to find contours using cv2.findContours()
  Parameters: 
            array[int] : weighted image 

        Returns: 
            array[array[int]] : contours            
            array[array[array[int]]] : hierarchy
  """
  return cv2.findContours(timg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

def cropForText(contours,img):
  """
  The function to crop part of tabular image from original image
  Parameters: 
            array[array[int]] : contours
            array[int] : original image 

        Returns: 
            array[int] : cropped image 
  """
  crops = copy.copy(img)
  mask = np.ones(crops.shape[:2], dtype="uint8") * 255
  area = []
  for c in contours:
    a = cv2.contourArea(c)
    area.append(a)
  avg = 2*(sum(area)/len(area))
  for c in contours:
    a = cv2.contourArea(c)
    if a<avg:
      cv2.drawContours(mask, [c], 0, 0, -1)
  cropped = cv2.bitwise_and(crops, crops, mask=mask)
  plotting = plt.imshow(cropped,cmap='gray')
  plt.show()
  cropped2 = cv2.subtract(img,cropped, mask=mask)
  plotting = plt.imshow(cropped2,cmap='gray')
  plt.show()
  return cropped

#cropForText(contours,img)

def sort_contours(cnts, method="left-to-right"):
    """
  The function to sort all contours and generate box coordinates
  Parameters: 
            array[array[int]] : contours

        Returns: 
            array[array[int]] : sorted contours
            array[array[int]] : bounding boxes
  """
    reverse = False
    if method == "right-to-left" or method == "bottom-to-top":
      reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
      i = 1
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
    key=lambda b:b[1][i], reverse=reverse))
    return (cnts, boundingBoxes)

def createBoxes(img,contours,boundingBoxes):
  """
  The function to draw boxes in image and calculate mean of box heights
  Parameters: 
            array[int] : original image
            array[array[int]] : contours
            array[array[int]] : bounding boxes
        Returns: 
            array[array[int]] : box with x,y coordinates and width, height
            int:mean of hieghts of boxes
  """
  heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
  mean = np.mean(heights)  
  box = []
  for c in contours:
      x, y, w, h = cv2.boundingRect(c)
      if (w<1000 and h<500):
          image = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
          box.append([x,y,w,h])
  plotting = plt.imshow(image,cmap='gray')
  plt.show()
  return box,mean

def detectCells(box,mean):
  """
  The function to arrange every boxes based on rows and columns
  Parameters: 
            array[array[int]] : bounding boxes
        
        Returns: 
            array[array[int]] : Column-wise boxes
            array[array[int]] : row-wise boxes
  """
  row=[]
  column=[]
  j=0
  #Sorting the boxes to their respective row and column
  for i in range(len(box)):
    if(i==0):
      column.append(box[i])
      previous=box[i]
    else:
      if(box[i][1]<=previous[1]+mean/2):
        column.append(box[i])
        previous=box[i]
        if(i==len(box)-1):
          row.append(column)
      else:
        row.append(column)
        column=[]
        previous = box[i]
        column.append(box[i])
  return column,row    

#column,row = detectCells(box,mean)

def finaliseBoxes(row):
  """
  The function to place the box equidistant from the center.
  Parameters: 
            array[array[int]] : row-wise boxes
        
        Returns: 
            array[array[int]] : final boxes
            int : column count
  """
  countcol = 0
  for i in range(len(row)):
    countcol = len(row[i])
    if countcol > countcol:
      countcol = countcol
  center = [int(row[i][j][0]+row[i][j][2]/2) for j in range(len(row[i])) if row[0]]
  center=np.array(center)
  center.sort()
  finalboxes = []
  for i in range(len(row)):
    lis=[]
    for k in range(countcol):
      lis.append([])
    for j in range(len(row[i])):
      diff = abs(center-(row[i][j][0]+row[i][j][2]/4))
      minimum = min(diff)
      indexing = list(diff).index(minimum)
      lis[indexing].append(row[i][j])
    finalboxes.append(lis)
  return finalboxes,countcol

#finalbox,columncounts = finaliseBoxes(row)

def extractText(finalboxes,bitnot):
  """
  The function to extract text from image.
  Parameters: 
            array[array[int]] : final boxes
            array[int] : inverted boxes
        
        Returns: 
            List[String] : list of extractd strings
  """
  outer=[]
  for i in range(len(finalboxes)):
    for j in range(len(finalboxes[i])):
      inner=''
      if(len(finalboxes[i][j])==0):
        outer.append(' ')
      else:
        for k in range(len(finalboxes[i][j])):
          y,x,w,h = finalboxes[i][j][k][0],finalboxes[i][j][k][1], finalboxes[i][j][k][2],finalboxes[i][j][k][3]
          finalimg = bitnot[x:x+h, y:y+w]
          kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
          border = cv2.copyMakeBorder(finalimg,2,2,2,2,   cv2.BORDER_CONSTANT,value=[255,255])
          resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
          dilation = cv2.dilate(resizing, kernel,iterations=1)
          erosion = cv2.erode(dilation, kernel,iterations=1)
          out = pytesseract.image_to_string(erosion)
          if(len(out)==0):
            out = pytesseract.image_to_string(erosion, config='--psm 3')
          inner = inner +" "+ out
        outer.append(inner)
  return outer

#Creating a dataframe of the generated OCR list
def exportOCR(outer,row,countcol,excelpath):
  """
  The function to write dataframe to excel sheet.
  Parameters: 
            List[String] : list extracted string
            array[array[int]] : row-wise boxes
            int : column counts
            String : path to output excel file
        
        Returns: 
            Dataframe : dataframe of extracted text
  """
  arr = np.array(outer)
  dataframe = pd.DataFrame(arr.reshape(len(row),countcol))
  data = dataframe.style.set_properties(align="left")
  #Converting it in a excel-file
  data.to_excel(excelpath)
  return data

#exportOCR(outer,row,columncounts,"/content/drive/My Drive/hack_space/output/dataset1/excel1.xlsx")

def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    """
  The function to construct image only with table
  Parameters: 
            Dataframe : dataframe of extracted text
            properties : All the properties to format table in image
        
        Returns: 
            figure : figure of constructed table 
  """

    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')

    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)

    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in  six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    return ax

def textExtraction(imgpath,excelpath,destpath):
  """
  The function to call all the helper methods to extract text from image
  Parameters: 
            String : input image path
            String : output excel path
            String : output table image path
        
        Returns: 
            Dataframe : dataframe of extracted text
            array[int]] : cropped image matrix
  """
  img,threshed = threshAndConvert(imgpath)
  kernel,vertical,horizontal = getLines(img)
  vert_img , vert_lines= getVertical(threshed,vertical) 
  hor_img, hor_lines = getHorizontal(threshed,horizontal)
  TableImg,bitnot = AddWeight(img,vert_lines,hor_lines,kernel)
  contours, hierarchy = findContours(TableImg)
  contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")
  cropped = cropForText(contours,img)
  box,mean = createBoxes(img,contours,boundingBoxes)
  column,row = detectCells(box,mean)
  finalbox,columncounts = finaliseBoxes(row)
  outer = extractText(finalbox,bitnot)
  data = exportOCR(outer,row,columncounts,excelpath)
  x = render_mpl_table(data.data, header_columns=0, col_width=2.0)
  x.get_figure().savefig(destpath)
  return cropped,data

#cropped,data = textExtraction("output/dataset1/1.jpg","output/dataset1/excel1.xlsx","output/dataset1/desttable1.jpg")