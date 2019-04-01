#!/usr/bin/env/python

from jinja2 import Environment
import json
import pdfkit
from PyPDF2 import PdfFileWriter, PdfFileReader


doc = """
<html>
<head>
<title>Game</title>
</head>
  <body>
    {{ body }}
  </body>
</html>
"""

bob = """
<!DOCTYPE html>
<html>
  <head>
    <title>Game</title>
	<meta charset="UTF-8" />
    <link rel="stylesheet" type="text/css" href="mystyle.css">
  </head>
  <body class="main">
	<div style="text-align:center;">
		{{ cards }}
	</div>
  </body>
</html>
"""

back = """
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
"""

front = """
		<div class="ruta" style="background-image: linear-gradient( rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7) ),url({{image}}); background-repeat:no-repeat; background-position: center; background-size: 90%;">
			{{title}}
		</div>
"""

def print_html_doc():
    page = Environment().from_string(doc).render(body='Hellow Gist from GutHub')
    with open('gris.html', 'w') as outfile:  
        outfile.write(page)
	
def read_json_file():
    with open('data.json') as json_file:  
        data = json.load(json_file)
        #for item in data:
        #    print(item)
        print(data[0])
        bib = Environment().from_string(front).render(image='Images/bird3.svg', title=data[0]['name'])
        print(bib)
        page = Environment().from_string(bob).render(cards=bib)
        with open('gris.html', 'w') as outfile:  
            outfile.write(page)

			
def pdf_from_html():
    path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    #pdfkit.from_string('Game', 'out.pdf', configuration=config)
    pdfkit.from_file('play.html', 'out.pdf', configuration=config)
	
def pdf_mix_it_up():
    output = PdfFileWriter()
    input1 = PdfFileReader(open("out.pdf", "rb"))
    
    # print how many pages input1 has:
    print("document1.pdf has %d pages." % input1.getNumPages())
    output.addPage(input1.getPage(0))
    output.addPage(input1.getPage(1))
    output.addPage(input1.getPage(0))
    
    # finally, write "output" to document-output.pdf
    outputStream = open("PyPDF2-output.pdf", "wb")
    output.write(outputStream)

if __name__ == '__main__':
    #print_html_doc()
    read_json_file()
    pdf_from_html()
    pdf_mix_it_up()