#!/usr/bin/env/python

from jinja2 import Environment
import json
import pdfkit
from PyPDF2 import PdfFileWriter, PdfFileReader


backTemplate = """
<!DOCTYPE html>
<html>
  <head>
    <title>Game</title>
	<meta charset="UTF-8" />
    <link rel="stylesheet" type="text/css" href="mystyle.css">
  </head>
  <body class="main">
	<div style="text-align:center;">
	{% for cardType in cardTypes -%}
	  {% for card in cardType.cards -%}
	    {%for x in range(card.count)-%}<div class="ruta">
		  <h4>{{ cardType.name }}</h4>
		  <table style="width:100%; height:90%; vertical-align: middle;">
		    {% if cardType.backImages|length == 3 -%}
		    <tr>
		      <th><img src={{cardType.backImages[0]}} style="max-width:90%; height: auto;"></th>
		      <th><img src={{cardType.backImages[1]}} style="max-width:90%; height: auto;"></th>
		    </tr>
		    <tr>
		      <td colspan = "2"><img src={{cardType.backImages[2]}} style="max-width:45%; height: auto;"></td>
		    </tr>
		    {% elif cardType.backImages|length == 2 -%}
		    <tr>
		      <th><img src={{cardType.backImages[0]}} style="max-width:90%; height: auto;"></th>
		      <th><img src={{cardType.backImages[1]}} style="max-width:90%; height: auto;"></th>
		    </tr>
		    {% elif cardType.backImages|length == 1 -%}
		    <tr>
		      <th><img src={{cardType.backImages[0]}} style="max-width:90%; height: auto;"></th>
		    </tr>
		    {% endif -%}
		  </table>
		</div>{% endfor -%}
	  {% endfor -%}
	  <br>
	{% endfor -%}
	</div>
  </body>
</html>
"""


frontTemplate = """
<!DOCTYPE html>
<html>
  <head>
    <title>Game</title>
	<meta charset="UTF-8" />
    <link rel="stylesheet" type="text/css" href="mystyle.css">
  </head>
  <body class="main">
	<div style="text-align:center;">
	{% for cardType in cardTypes -%}
	  {% for card in cardType.cards -%}
	    {%for x in range(card.count) -%}<div class="ruta" style="background-image: linear-gradient( rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7) ),url({%if card.frontImage %}{{card.frontImage}}{% else %}{{cardType.frontImage}}{% endif %}); background-repeat:no-repeat; background-position: center; background-size: 90%;">
		  <h4>{{ card.title }}</h4>
		  <p>{{ card.description }}</p>
		  {% for attribute in card.attributes -%}
		  <h5>{{ attribute.title }}</h5>
		  <p>{{ attribute.description }}</p>
		  {% endfor -%}
		  
		  {% if cardType.template -%}
		  {%for x in range(cardType.template|length)-%}
		  
		  <p><b>{{cardType.template[x]}}:</b> {{card['values'][x]}}</p>
		  {% endfor -%}
		  {% endif -%}
		  {% if cardType.dispCount -%}
		  <p><b>Ligg per spel:</b> {{card.count}}</p>
		  {% endif -%} 
		</div>{% endfor -%}
	  {% endfor -%}
	  <br>
	{% endfor -%}
	</div>
  </body>
</html>
"""

def debug(text):
    print(text)
    return ''

def read_json_file():
    with open('data.json') as json_file:  
        data = json.load(json_file)

        environment = Environment()
        environment.filters['debug']=debug
        frontPages = environment.from_string(frontTemplate).render(cardTypes=data, image='Images/bird1.svg')
        with open('fronts.html', 'w', encoding='utf8') as outfile:  
            outfile.write(frontPages)
		
        backPages = Environment().from_string(backTemplate).render(cardTypes=data)
        with open('backs.html', 'w', encoding='utf8') as outfile:  
            outfile.write(backPages)

def pdf_from_html():
    path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    #pdfkit.from_string('Game', 'out.pdf', configuration=config)
    pdfkit.from_file('fronts.html', 'fronts.pdf', configuration=config)
    pdfkit.from_file('backs.html', 'backs.pdf', configuration=config)
	
def pdf_mix_it_up():
    output = PdfFileWriter()
    fronts = PdfFileReader(open("fronts.pdf", "rb"))
    backs = PdfFileReader(open("backs.pdf", "rb"))
    

    if not fronts.getNumPages() == backs.getNumPages():
        raise AssertionError()
    print("Front and backs take has %d sides eage." % fronts.getNumPages())

    for index in range(fronts.getNumPages()):
        output.addPage(fronts.getPage(index))
        output.addPage(backs.getPage(index))

    outputStream = open("frontsAndBacks.pdf", "wb")
    output.write(outputStream)

if __name__ == '__main__':
    read_json_file()
    pdf_from_html()
    pdf_mix_it_up()