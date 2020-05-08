# OCR: Boletim de Catanduva

Implementação de solução de reconhecimento de caracteres para melhor acompanhamento epidemiológico na cidade de Catanduva, por meio de classe `OCRBoletimCatanduva`.

A versão mais atualizada está em `/python/`, dia **08/05/2020**, com as versões mostradas abaixo.

## Como funciona?

![Representação](https://github.com/rafaeldefazio/ocr-boletim-catanduva/raw/master/schema.png)

### Funcionamento:
1. Site da prefeitura é acessado
2. Boletim do dia é baixado
3. Imagem é pré-processada
4. Dados são extraídos e salvos em formato `csv` ou `json`


## Objetivo

## Versão 1
![Exemplo](https://github.com/rafaeldefazio/ocr-boletim-catanduva/raw/master/exemplo.jpg)

## Versão 2

![Exemplo 2](https://github.com/rafaeldefazio/ocr-boletim-catanduva/raw/master/exemplo2.jpg)


## Versão 2

![Exemplo 3](https://github.com/rafaeldefazio/ocr-boletim-catanduva/raw/master/exemplo3.jpg)


## Requisitos:


- Python 2.7
- - pytesseract
- - numpy
- - BeautifulSoup4
- OpenCV 4
- Tesseract 4.0

OU

- C++
- OpenCV 4
- Tesseract 4.0




## Configurações

```python
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
```
- `FORMAT`: formato do output (json ou csv)
- `BOLETIM_URL`: site da Prefeitura contendo boletim epidemiológico
- `TEMP_IMAGE_FOLDER`: localização da pasta em que ficarão armazenadas as imagens para análise
- `OUTPUT_FOLDER`: localização da pasta em que ficarão as saídas dos dados
- `TAMANHO_IMAGEM` tamanho da imagem para padronizar processamento


## Estrutura HTML

- Caminho XPath: `/html/body/div[4]/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div[1]/p[1]/img`
- Via Beautiful Soup: `div.blog-single > div.inner-box > p::first-child > img['src']`

# Limitações

O padrão da imagem deve ser mantido, os números devem ficar dentro dos limites, sem alteração de estrutura da imagem. A estrutura do site também deve ser mantida. Caso haja alterações, será necessário adaptar o script.

# Roadmap
- Cron diário com script
- `roi.cpp` contém código experimental em C++, ainda não finalizado.
