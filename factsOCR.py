from PIL import Image
import pytesseract as pyt
import textParser as p
import cv2
import os

def returnFacts(path):
	imPath = path
	clear = cv2.threshold(cv2.cvtColor(cv2.imread(imPath), 
						  cv2.COLOR_BGR2GRAY), 0, 255, 
						  cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	cv2.imwrite("greyocr.png", clear)

	greyImPath = "greyocr.png"
	img = Image.open(greyImPath)
	pyt.pytesseract.tesseract_cmd = r'C:/Users/prana/AppData/Local/Tesseract-OCR/tesseract'
	text = pyt.image_to_string(greyImPath)

	img.close()
	os.remove("greyocr.png")

	a = p.convertToDict(p.removeMultiLines(text))
	al = []

	return a[0]



