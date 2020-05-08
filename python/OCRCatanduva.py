# coding: utf-8
import cv2
import pytesseract
import urllib2
import urllib
import os
from bs4 import BeautifulSoup as bs
import csv
import json
import sys


def SaveFile(date, folder, FORMAT, ocrData):

	src = folder + '/' +  date + '.' + FORMAT
	print(src)

	if os.path.isfile(src):
		print("[!] Arquivo %s já existe para data %s " % (FORMAT, str(date)))
		sys.exit()


	if FORMAT is "csv":

		with open(src, 'w') as csvf:
			writer = ocrData.writer(csvf)

			for key, value in ocrData.items():
				writer.writerow([key, value])



	elif FORMAT is "json":
		with open(src, 'w') as fp:
			json.dump(ocrData, fp)

	print("\nSalvo com sucesso:\n\t%s.%s" % (src, FORMAT))




def SaveImage(folder, url):

	# TENTA ACESSAR PÁGINA
	try:

		page = urllib2.urlopen(url)

	except urllib2.HTTPError, e:
		print("[!] Erro ao abrir pagina: %s" % e)

	else:
		print("[!] %s aberto com sucesso..." % url)


	soup = bs(page, 'html.parser')

	post = soup.find("div", {"class": "blog-single"})

	post = post.find("div", {"class": "inner-box"})

	boletim = post.select('div > p')[0]

	boletim = boletim.find('img')['src']

	image_src = folder + '/' +  os.path.basename(boletim)


	# TENTA BAIXAR IMAGEM

	try:
		urllib.urlretrieve(boletim, image_src)
	except Exception,e:
		print("[!] Nao foi possivel localizar imagem: %s" % e)
		sys.exit()
	else:
		print("[!] Imagem carregada e salva com sucesso...")


	return image_src



class OCRBoletimCatanduva:

	'''

	imageSrc: Recebe endereço da imagem no computador



	dateRect: recebe lista com a localização da data da imagem

		-> lista (x, y, w, z)

				-onde X e y se referem ao vértice superior esquerdo do retângulo

				- w, largura do retângulo
				- z, altura do retângulo


	imageSize: recebe lista com o tamanho da imagem (x, y)


	rects: Recebe dicionário de retângulos.

		-> Chave: nome da variável

		-> Valor: lista (x, y, w, z)

			-onde X e y se referem ao vértice superior esquerdo do retângulo

			- w, largura do retângulo
			- z, altura do retângulo
	'''

	def __init__(self, imageSrc, imageSize, dateRect, rects):

		self.rects = rects
		self.imageSrc = imageSrc
		self.dateRect = dateRect



		tesseract_config = '--psm 8 --oem 0 -c tessedit_char_whitelist=0123456789.'
		self.roiSquareLambda = lambda rect: self.result[int(rect[1]):int(rect[1]+rect[3]), int(rect[0]):int(rect[0]+rect[2])]
		self.ocrLambda = lambda image: pytesseract.image_to_string(image, lang='por', config=tesseract_config)



		img = cv2.imread(imageSrc, cv2.IMREAD_GRAYSCALE)
		img = cv2.resize(img, imageSize, interpolation = cv2.INTER_CUBIC)


		blur = cv2.GaussianBlur(img,(3,3),0)
		ret3, self.result = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


		self.getDate()
		self.calcRoi()
		self.OCR()


	def getDate(self):

		dateROI = self.roiSquareLambda(self.dateRect)
		dateOCR = self.ocrLambda(dateROI)

		self.date = self.formatDateSlash(dateOCR)



	def calcRoi(self):
		# def Roi(self, image):

		# 	for k, v in rects.iteritems():

		# 		x = v[0] + v[2]
		# 		y = v[1] + v[3]

		# 		crop = result[int(v[1]):int(y), int(v[0]):int(x)]

		# 		rois[k] = crop
		
		self.rois = {key: self.roiSquareLambda(value) for (key, value) in self.rects.iteritems()}



	def resizeImageScale(self, image, scale_percent):

			width = int(image.shape[1] * scale_percent / 100)
			height = int(image.shape[0] * scale_percent / 100)
			dim = (width, height)

			return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)



	def formatDateSlash(self, date):
		dateSplit = date.split('.')
		return "%s-%s-%s" % (dateSplit[2], dateSplit[1], dateSplit[0])


	def OCR(self):

		self.ocrs = {key.lower(): self.ocrLambda(value) for (key, value) in self.rois.iteritems()}
		self.ocrs['data'] = self.date

		