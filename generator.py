#!/usr/bin/env/python

from jinja2 import Environment
from PyPDF2 import PdfFileWriter, PdfFileReader
import json
import pdfkit
import cheatSheet

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
	{%for x in range(card.count) -%}
	  <div class="box box-card" style="background-image: url({%if card.frontImage %}{{card.frontImage}}{% else %}{{cardType.frontImage}}{% endif %}); background-repeat:no-repeat; background-position: center; background-size: 80%;">
		<div class="inner inner-card">
		  <table style="width:100%; height: 100%; margin: 0px;">
			<tr style="height: 100%; vertical-align: top;">
			  <td>
				<h4>{{ card.title }}</h4>
				<p>{{ card.description }}</p>
				{% for attribute in card.attributes -%}
				<h5>{{ attribute.title }}</h5>
				<p>{{ attribute.description }}</p>
				{% endfor -%}
				{% if cardType.template -%}
				<br>
				{%for x in range(cardType.template|length)-%}
				<p><b>{{cardType.template[x]}}:</b> {{card['values'][x]}}</p>
				<br>
				{% endfor -%}
				{% endif -%}
				{% if cardType.countText -%}
				<p><b>{{ cardType.countText }}</b> {{card.count}}</p>
				{% endif -%}
			  </td>
			</tr>
			{% if card.turns -%}
			<tr style="height: 0;">
			  <td>
				<table style="width:100%; text-align: center;">
				<tr>
				  {% for t in range(card.turns) -%}
				  <td><div class="circle"><span>{{t+1}}</span></div></td>
				  {% endfor -%}
				</tr>
				</table>
			  </td>
			</tr>
			{% endif -%}
			{% if card.summation -%}
			<tr style="height: 0;">
			  <td>
				<p class="summation">{{ card.summation }}</p>
			  </td>
			</tr>
			{% endif -%}
		  </table>
		</div>
	  </div>{% endfor -%}
	  {% endfor -%}
	  <br>
	  {% endfor -%}
	  {% for t in range(numerOfCheatSheet) -%}{{ cheatSheet }}{% endfor -%}
	</div>
  </body>
</html>
"""

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
	{% for x in range(card.count)-%}
	  <div class="box box-card">
		<div class="inner inner-card" style="display: table;">
		  <h4 style="display: table-row;">{{ cardType.name }}</h4>
		  <div  style="display: table-row; height:100%;">
			<table style="height:100%; vertical-align: middle;">
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
		  </div>
		</div>
	  </div>{% endfor -%}
	  {% endfor -%}
	  <br>
	  {% endfor -%}
	  {% for t in range(numerOfCheatSheet) -%}{{cheatSheet}}{% endfor -%}
	</div>
  </body>
</html>
"""

def debug(text):
    print(text)
    return ''

def read_json_file():
    numerOfCheatSheet = 3

    with open('data.json') as json_file:  
        data = json.load(json_file)

        environment = Environment()
        environment.filters['debug']=debug
        frontPages = environment.from_string(frontTemplate).render(cardTypes=data, cheatSheet=cheatSheet.cheatSheetFront, numerOfCheatSheet=numerOfCheatSheet)
        with open('fronts.html', 'w', encoding='utf8') as outfile:  
            outfile.write(frontPages)

        backPages = Environment().from_string(backTemplate).render(cardTypes=data, cheatSheet=cheatSheet.cheatSheetBack, numerOfCheatSheet=numerOfCheatSheet)
        with open('backs.html', 'w', encoding='utf8') as outfile:  
            outfile.write(backPages)

def pdf_from_html():
    path_wkthmltopdf = r'.\lib\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    pdfkit.from_file('fronts.html', 'fronts.pdf', configuration=config)
    pdfkit.from_file('backs.html', 'backs.pdf', configuration=config)
    pdfkit.from_file('instructions.html', 'instructions.pdf', configuration=config)

def pdf_mix_it_up():
    output = PdfFileWriter()
    fronts = PdfFileReader(open("fronts.pdf", "rb"))
    backs = PdfFileReader(open("backs.pdf", "rb"))

    if not fronts.getNumPages() == backs.getNumPages():
        raise AssertionError()
    print("Front and back html documents has %d sides each." % fronts.getNumPages())

    for index in range(fronts.getNumPages()):
        output.addPage(fronts.getPage(index))
        output.addPage(backs.getPage(index))

    outputStream = open("cards.pdf", "wb")
    output.write(outputStream)

if __name__ == '__main__':
    read_json_file()
    pdf_from_html()
    pdf_mix_it_up()