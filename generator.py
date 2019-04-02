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
	{% for cardType in cardTypes %}
	  {% for card in cardType.cards %}
	    {%for x in range(card.count)%}
		  <div class="ruta">
		    {{ cardType.name }}
		    <table style="width:100%; height:90%; vertical-align: middle;">
		      <tr>
		        <th><img src='Images/bird1.svg' style="max-width:90%; height: auto;"></th>
		        <th><img src='Images/bird2.svg' style="max-width:90%; height: auto;"></th>
		      </tr>
		      <tr>
		        <td><img src='Images/bird3.svg' style="max-width:90%; height: auto;"></td>
		        <td><img src='Images/bird4.svg' style="max-width:90%; height: auto;"></td>
		      </tr>
		    </table>
		  </div>
		{% endfor %}
	  {% endfor %}
	  <br>
	{% endfor %}
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
	{% for cardType in cardTypes %}
	  {% for card in cardType.cards %}
	    {%for x in range(card.count)%}
		  <div class="ruta" style="background-image: linear-gradient( rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7) ),url({{image}}); background-repeat:no-repeat; background-position: center; background-size: 90%;">
		    {{ card.title }}
			{{ card.description }}
			{% for attribute in card.attributes %}
			<br>
			{{ attribute.title }}
			{{ attribute.description }}
			{% endfor %}
			
			{% if cardType.template %}
			{%for x in range(cardType.template|length)%}
			<br>
			{{cardType.template[x]}}
			{{card['values'][x]}}
			{% endfor %}
			{% endif %} 
		  </div>
		{% endfor %}
	  {% endfor %}
	  <br>
	{% endfor %}
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