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
	  {% for t in range(numerOfCheatSheet) -%} 
	  <div class="box box-sheet">
	    <div class="inner inner-sheet"">
		  <table style="height:100%; vertical-align: middle; text-align: center;">
			<tr>
			  <th><img src=Images/bird1.svg style="max-width:70%; height: auto;"></th>
			  <th><img src=Images/bird2.svg style="max-width:70%; height: auto;"></th>
			  <th><img src=Images/bird3.svg style="max-width:70%; height: auto;"></th>
			  <th><img src=Images/bird4.svg style="max-width:70%; height: auto;"></th>
			</tr>
			<tr>
			  <td colspan = "4"><h1 style="margin: 0;">Samtycke</h1></td>
			</tr>
			<tr>
			  <th><img src=Images/bird5.svg style="max-width:70%; height: auto;"></th>
			  <th><img src=Images/bird6.svg style="max-width:70%; height: auto;"></th>
			  <th><img src=Images/bird7.svg style="max-width:70%; height: auto;"></th>
			  <th><img src=Images/bird8.svg style="max-width:70%; height: auto;"></th>
			</tr>
		  </table>
		</div>
	  </div>{% endfor -%}
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
	{%for x in range(card.count) -%}
	  <div class="box box-card" style="background-image: url({%if card.frontImage %}{{card.frontImage}}{% else %}{{cardType.frontImage}}{% endif %}); background-repeat:no-repeat; background-position: center; background-size: 80%;">
		<div class="inner inner-card">
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
	  	  {% if card.turns -%}
		  <table style="width:100%; text-align: center;">
		    <tr>
		      {% for t in range(card.turns) -%}
			  <th><div class="circle"><span>{{t+1}}</span></div></th>
			  {% endfor -%}
		    </tr>
		  </table>
		  {% endif -%}
		</div>
	  </div>{% endfor -%}
	  {% endfor -%}
	  <br>
	  {% endfor -%}
	  {% for t in range(numerOfCheatSheet) -%} 
	  <div class="box box-sheet">
		<div class="inner inner-sheet">
		  <ul>
		  	<li>Under din tur välj ett av följande alternativ:</li>
		  	<ul>
		  	  <li>Dra ett händelsekort</li>
		  	  <li>Gå till gymmet (+1<heart/>)</li>
		  	  <li>Försök att ligga med en person i staden (ej medspelare)</li>
		  	</ul>
		  	<li>Ta ditt <heart/> minus personens <flake/> i tabellen nedan för att se vilka tärningsslag som leder till lyckat ligg</li>
		  </ul>
		  <table class="dice">
		  	<tr>
		  	  <th class="dice"><heart/> - <flake/></th>
		  	  <th class="dice"><0</th>
		  	  <th class="dice">0</th>
		  	  <th class="dice">1</th>
		  	  <th class="dice">2</th>
		  	  <th class="dice">3</th>
		  	  <th class="dice">>3</th>
		  	</tr>
		  	<tr>
			  <th class="dice">Tärning</th>
			  <th class="dice">-</th>
			  <th class="dice">1</th>
			  <th class="dice">1-2</th>
			  <th class="dice">1-3</th>
			  <th class="dice">1-4</th>
			  <th class="dice">1-5</th>
		  	</tr>
		  </table>
		  <ul>
		    <li>Efter lyckat ligg tas ett utfallskort</li>
		  </ul>
		</div>
	  </div>{% endfor -%}
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
        frontPages = environment.from_string(frontTemplate).render(cardTypes=data, numerOfCheatSheet=numerOfCheatSheet)
        with open('fronts.html', 'w', encoding='utf8') as outfile:  
            outfile.write(frontPages)
		
        backPages = Environment().from_string(backTemplate).render(cardTypes=data, numerOfCheatSheet=numerOfCheatSheet)
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
    print("Front and back html documents has %d sides each." % fronts.getNumPages())

    for index in range(fronts.getNumPages()):
        output.addPage(fronts.getPage(index))
        output.addPage(backs.getPage(index))

    outputStream = open("frontsAndBacks.pdf", "wb")
    output.write(outputStream)

if __name__ == '__main__':
    read_json_file()
    pdf_from_html()
    pdf_mix_it_up()