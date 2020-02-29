from PIL import Image
import pytesseract as pyt
import textParser as p
import wikipedia
import cv2
import os

def returnText(path, allergens):
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

	n = p.normalizeIngredients(text)

	results = []
	aresults = []

	for x in n:
		try:
		 	wpinfo = x + ": " + wikipedia.summary(x, sentences=1)
		 	results.append(wpinfo)
		 	if x in allergens:
		 		aresults.append(wpinfo)
		except:
			pass

	return [aresults, results]
