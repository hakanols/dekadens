#!/usr/bin/env/python

from jinja2 import Environment
import json


HTML = """
<html>
<head>
<title>{{ title }}</title>
</head>
<body>
Hello.
</body>
</html>
"""

def print_html_doc():
    page = Environment().from_string(HTML).render(title='Hellow Gist from GutHub')
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

if __name__ == '__main__':
    print_html_doc()
    read_json_file()