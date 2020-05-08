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

rects['Not_Total'] = (748, 355, 173, 68)
rects['Conf_Total'] = (748, 435, 173, 68)
rects['Desc_Total'] = (748, 503, 173, 68)
rects['Susp_Total'] = (748, 571, 173, 68)

rects['Inter_Total'] = (748, 698, 173, 68)

rects['Obito_Total'] = (748, 776, 173, 68)

rects['Curados'] = (748, 853, 173, 68)


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




