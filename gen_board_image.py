#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2019 Håkan Olsson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from jinja2 import Environment
import json
import imgkit

boardTemplate = """
<!DOCTYPE html>
<html>
  <head>
	<title>Game</title>
	<meta charset="UTF-8" />
	<link rel="stylesheet" type="text/css" href="mystyle.css">
  </head>
  <body class="main">
	<div style="text-align:center;">
	{% for x in range(16) -%}
	{% set card = cardType.cards[x] -%}
	  <div class="box box-card" {% if card.count > 1 -%}; style="box-shadow: 1px 1px white, 5px 5px white, 5px 5px 0px 1px black{% if card.count > 2 -%}, 10px 10px white, 10px 10px 0px 1px black{% endif -%};"{% endif -%}>
		<div class="inner" style="width:100%; height: 100%;">
		  <div style="width:100%; height: 100%; display: table; background-image: url({%if card.frontImage %}{{card.frontImage}}{% else %}{{cardType.frontImage}}{% endif %}); background-repeat:no-repeat; background-position: center; background-size: 80%;">
			<div class="inner-card" style="width:100%; height: 100%;">
			  <h4>{{ card.title }}</h4>
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
			</div>
		  </div>
		</div>
	  </div>
	  {% if (x+1) % 4 == 0 -%}<br><br>{% else -%}&nbsp;&nbsp;{% endif -%}{% endfor -%}
	</div>
  </body>
</html>
"""

def debug(text):
    print(text)
    return ''
	
def generate_board_image():
    with open('data.json') as json_file:  
        data = json.load(json_file)
	
        environment = Environment()
        environment.filters['debug']=debug
        board = environment.from_string(boardTemplate).render(cardType=data[4])
        with open('board.html', 'w', encoding='utf8') as outfile:  
            outfile.write(board)

    svg_options = {
        'format': 'svg'
    }
    svg_config = imgkit.config(wkhtmltoimage=r'.\lib\wkhtmltopdf\bin\wkhtmltoimage.exe')
    imgkit.from_file('board.html', 'board.svg', options=svg_options, config=svg_config)

if __name__ == '__main__':
    generate_board_image()
