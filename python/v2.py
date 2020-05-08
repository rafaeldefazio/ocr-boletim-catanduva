# coding: utf8
from OCRCatanduva import OCRBoletimCatanduva, SaveImage, SaveFile
import sys
import datetime


TEMP_IMAGE_FOLDER = './temp_images'
OUTPUT_FOLDER = './output'
FILE_FORMAT = 'json'
BOLETIM_URL = 'http://www.catanduva.sp.gov.br/coronavirus/'
TAMANHO_IMAGEM = (1134, 1134)


date = (590, 258, 137, 32)

rects = {}

rects['Curados'] = (660, 875, 200, 50)

rects['Not_Grave'] = (507, 406, 240, 60)
rects['Susp_Grave'] = (507, 466, 240, 60)
rects['Desc_Grave'] = (507, 526, 240, 60)
rects['Conf_Grave'] = (507, 586, 240, 50)


rects['Not_Leve'] = (799, 406, 193, 60)
rects['Susp_Leve'] = (799, 466, 193, 60)
rects['Desc_Leve'] = (799, 526, 193, 60)
rects['Conf_Leve'] = (799, 586, 193, 50)

rects['Inter_Susp'] = (507, 729, 240, 60)
rects['Inter_Conf'] = (507, 789, 240, 60)


rects['Obito_Susp'] = (761, 729, 240, 60)
rects['Obito_Conf'] = (761, 789, 240, 60)


salvarBoletim = SaveImage(TEMP_IMAGE_FOLDER, BOLETIM_URL)
ocr = OCRBoletimCatanduva(salvarBoletim, TAMANHO_IMAGEM, date, rects)


ocrDate = datetime.datetime.strptime(ocr.date, "%Y-%m-%d")
ocrDateNow = datetime.datetime.now()


if ocrDate > ocrDateNow:
	print("Data inválida")
	sys.exit()
elif ocrDate.year != 2020:
	print("Data inválida")
	sys.exit()


salvarDados = SaveFile(ocr.date, OUTPUT_FOLDER, FILE_FORMAT, ocr.ocrs)




