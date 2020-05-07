#coding: utf8
import urllib2
import urllib
import cv2
import pytesseract
import numpy as np
import os
from bs4 import BeautifulSoup as bs

import csv
import json


# VARIÁVEIS
FORMAT = 'json'
WD = '/home/rafaelbdefazio/Imagens/covid-catanduva/exemplo/'
SITE_URL = 'http://www.catanduva.sp.gov.br/coronavirus/'

temp_images_folder = 'temp_images/'
output_folder = 'output/'


# TENTA ACESSAR PÁGINA
try:

	page = urllib2.urlopen(SITE_URL)

except urllib2.HTTPError, e:
	print("[!] Erro ao abrir pagina: %s" % e.code)

else:
	print("[!] %s aberto com sucesso..." % SITE_URL)


# PROCESSAMENTO DE HTML

soup = bs(page, 'html.parser')

post = soup.find("div", {"class": "blog-single"})

post = post.find("div", {"class": "inner-box"})

boletim = post.select('div > p')[0]

boletim = boletim.find('img')['src']


image_src = WD + temp_images_folder + os.path.basename(boletim)


# TENTA BAIXAR IMAGEM

try:
	urllib.urlretrieve(boletim, image_src)
except Exception,e:
	print("[!] Nao foi possivel localizar imagem: %s" % e.code)
else:
	print("[!] Imagem carregada e salva com sucesso...")



# image_src = WD + temp_images_folder + 'boletim_do_coronavirus_05-05-20.jpg'


# COMEÇA OPENCV
img = cv2.imread(image_src, cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (1134, 1134), interpolation = cv2.INTER_CUBIC)


blur = cv2.GaussianBlur(img,(3,3),0)
ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

result = th3


# VERIFICAR DATA

rect_data= (588, 386, 140, 40);
x = rect_data[0] + rect_data[2]
y = rect_data[1] + rect_data[3]
data_crop = result[int(rect_data[1]):int(y), int(rect_data[0]):int(x)]
scale_percent = 50 # percent of original size
width = int(data_crop.shape[1] * scale_percent / 100)
height = int(data_crop.shape[0] * scale_percent / 100)
dim = (width, height)
vresized_crop = cv2.resize(data_crop, dim, interpolation = cv2.INTER_AREA)

ocr_txt_data = pytesseract.image_to_string(vresized_crop, lang='por', \
		  config='--psm 8 --oem 0 -c tessedit_char_whitelist=0123456789.')

mdY = ocr_txt_data.split('.')

data_slash = "%s-%s-%s" % (mdY[2], mdY[1], mdY[0])

filename = "%s.%s" % (data_slash, FORMAT)


data_file = WD + output_folder + filename



if os.path.isfile(data_file):
	print("[!] Arquivo já existe (%s%s%s.%s)" % (WD, output_folder, str(data_slash), FORMAT))
	exit()
else:
	


# ÁREAS DA IMAGEM

	rects = {}

	rects['Not_Total'] = (45, 571, 510, 133)
	rects['Not_Susp'] = (45, 720, 168, 95);
	rects['Not_Desc'] = (219, 720, 168, 95);
	rects['Not_Conf'] = (392, 720, 168, 95);


	  #// -- INTERNADOS


	rects['Int_Susp'] = (576, 571, 171, 75);
	rects['Int_Conf'] = (748, 571, 171, 75);
	rects['Int_Tot'] = (918, 571, 171, 75);



	  #// -- ÓBITOS


	rects['Obt_Susp'] = (576, 741, 171, 75);
	rects['Obt_Conf'] = (748, 741, 171, 75);
	rects['Obt_Tot'] = (918, 741, 171, 75);


	  #// -- Data

	rects['Data'] = (588, 386, 140, 40);


	  #// -- CASOS LEVES

	rects['Lev_Tot'] = (661, 1008, 260, 80);


	rois = {}



# CRIA REGIÕES DE INTERESSE

	for k, v in rects.iteritems():

		x = v[0] + v[2]
		y = v[1] + v[3]

		crop = result[int(v[1]):int(y), int(v[0]):int(x)]

		rois[k] = crop



# REALIZA RECONHECIMENTO

	ocr = {}

	print("\n\n---\tATUALIZANDO %s\t---" % data_slash)
	print("---\tUtilizando formato %s\t---\n\n" % FORMAT)


	for k, v in rois.iteritems():



		if (k == 'Data'):
			ocr_txt = ocr_txt_data
			mdY = ocr_txt_data.split('.')
			ocr_txt = "%s-%s-%s" % (mdY[2], mdY[1], mdY[0])

			ocr[k.lower()] = ocr_txt
			

		scale_percent = 50 # percent of original size
		width = int(v.shape[1] * scale_percent / 100)
		height = int(v.shape[0] * scale_percent / 100)
		dim = (width, height)
		# resize image
		vresized = cv2.resize(v, dim, interpolation = cv2.INTER_AREA)


		# cv2.imshow('pre', vresized)
		# cv2.waitKey(0)



		ocr_txt = pytesseract.image_to_string(vresized, lang='por', \
			   config='--psm 8 --oem 0 -c tessedit_char_whitelist=0123456789.')


		


		ocr[k.lower()] = ocr_txt



		print("[%s] sendo atualizado...\t%s" % (k, ocr_txt))





# SALVA ARQUIVOS


	if FORMAT is "csv":

		with open(data_file, 'w') as csvf:
			writer = csv.writer(csvf)

			for key, value in ocr.items():
				writer.writerow([key, value])



	elif FORMAT is "json":
		with open(data_file, 'w') as fp:
			json.dump(ocr, fp)


	print("\nSalvo com sucesso:\n\t%s.%s" % (data_file, FORMAT))
		






