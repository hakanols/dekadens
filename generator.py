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

div = """

"""

def print_html_doc():
    page = Environment().from_string(doc).render(body='Hellow Gist from GutHub')
    with open('gris.html', 'w') as outfile:  
        outfile.write(page)
	
def read_json_file():
    with open('data.txt') as json_file:  
        data = json.load(json_file)
        for p in data['people']:
            print('Name: ' + p['name'])
            print('Website: ' + p['website'])
            print('From: ' + p['from'])
            print('')
    with open('data.json') as json_file:  
        data = json.load(json_file)
        for item in data:
            print(item)

			
def pdf_from_html():
    path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    #pdfkit.from_string('Game', 'out.pdf', configuration=config)
    pdfkit.from_file('Game.html', 'out.pdf', configuration=config)
	
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
    print_html_doc()
    read_json_file()
    pdf_from_html()
    pdf_mix_it_up()