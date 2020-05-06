# OCR: Boletim de Catanduva

Implementação de solução de reconhecimento de caracteres para melhor acompanhamento epidemiológico na cidade de Catanduva. (`ocr-python.py`).


## Como funciona?

![Representação](https://github.com/rafaeldefazio/ocr-boletim-catanduva/raw/master/schema.png)

### Funcionamento:
1. Site da prefeitura é acessado
2. Boletim do dia é baixado
3. Imagem é pré-processada
4. Dados são extraídos e salvos em formato `csv` ou `json`


## Objetivo
![Exemplo](https://github.com/rafaeldefazio/ocr-boletim-catanduva/raw/master/exemplo.jpg)


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
# VARIÁVEIS
FORMAT = 'json'
WD = '/home/rafaelbdefazio/Imagens/covid-catanduva/exemplo/'
SITE_URL = 'http://www.catanduva.sp.gov.br/coronavirus/'

temp_images_folder = 'temp_images/']
output_folder = 'output/'
```
- `FORMAT`: formato do output (json ou csv)
- `WD`: localização do scripts e pastas (devem estar pré-criadas)
- `SITE_URL`: site da Prefeitura contendo boletim epidemiológico
- `temp_images_folder`: localização da pasta em que ficarão armazenadas as imagens para análise
- `output_folder`: localização da pasta em que ficarão as saídas dos dados


## Estrutura HTML

- Caminho XPath: `/html/body/div[4]/div/div[2]/div/div/div[1]/div/div[1]/div[1]/div[1]/p[1]/img`
- Via Beautiful Soup: `div.blog-single > div.inner-box > p::first-child > img['src']`


# Roadmap
- Cron diário com script
- `roi.cpp` contém código experimental em C++, ainda não finalizado.
