# coding: utf8
from OCRCatanduva import OCRBoletimCatanduva, SaveImage, SaveFile
import sys
import datetime


TEMP_IMAGE_FOLDER = './temp_images'
OUTPUT_FOLDER = './output'
FILE_FORMAT = 'json'
BOLETIM_URL = 'http://www.catanduva.sp.gov.br/coronavirus/'
TAMANHO_IMAGEM = (1134, 1134)


date = (588, 386, 140, 40)

rects = {}

rects['Not_Total'] = (45, 571, 510, 133)
rects['Not_Susp'] = (45, 720, 168, 95)
rects['Not_Desc'] = (219, 720, 168, 95)
rects['Not_Conf'] = (392, 720, 168, 95)


  #// -- INTERNADOS


rects['Int_Susp'] = (576, 571, 171, 75)
rects['Int_Conf'] = (748, 571, 171, 75)
rects['Int_Total'] = (918, 571, 171, 75)



  #// -- ÓBITOS


rects['Obt_Susp'] = (576, 741, 171, 75)
rects['Obt_Conf'] = (748, 741, 171, 75)
rects['Obt_Total'] = (918, 741, 171, 75)

  #// -- CASOS LEVES

rects['Lev_Total'] = (661, 1008, 260, 80);




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