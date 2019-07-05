# What is this?
This is a board game with a humoristic touch. Best played with friends after substantial amount of alcohol.
I once played a home made game called "Most things when you die wins". That inspired me to make my own game.
My game is more like "The one that sleep around most wins". Fictively of course.  
The game cards is completely generated from code and can be printed on an ordinary printer. Translation to
other languages should be quit easy. Only available in Swedish for the moment.

# Vad är nu detta?
Detta är ett brädspel med en humoristisk touch. Bäst spelat med vänner efter en betydande mängd alkohol.
Jag spelade en gång ett hemgjort spel som heter "De med flesta saker när man dör vinner". Det inspirerade 
mig att göra mitt egna spel. Mitt spel är mer som "Den som ligger runt mest vinner". Fiktivt såklart.
Spelkorten genereras fullständigt från kod och kan skrivas ut på en vanlig skrivare. Översättning till
andra språk borde vara lätt. Finns bara på svenska för tillfället.

# Skaffa spelet
* Ladda bara hem cards.pdf och instructions.pdf och skriv ut
* Rota fram en tärning eller kör med simulerad tärning. Se instructions.pdf
* Skaffa fram några tändstickor eller andra markörer
* Sen kanske den svåraste punkten. Skaffa några vänner att spela med

# Att generera kort (windows)
Ladda hem python 3 från:
https://www.python.org/downloads/windows/

Ladda hem detta repo och öppna en terminal och gå till det nerladdeade repots rot

### Uppsättning (Bara första gången)
```
pip install jinja2
pip install pdfkit
pip install imgkit
```
Ladda hem wkhtmltopdf från https://wkhtmltopdf.org/downloads.html och installera under mappen "lib" i repot.

### Bygg
```
python generator.py
```

# License
<p>Kortgenereringen är släppt under <b>MIT</b> licens. Fritt att använda till egna spel.<br>
Spelet Samtycke är släppt under <b>CC BY-NC 3.0</b>. Fritt att skriva ut och spela men förbjudet att sälja vidare.</p>
<a rel="license" href="https://opensource.org/licenses/MIT/"><img alt="MIT-license" src="Images/MIT-license.svg" height="50"/></a>
<a rel="license" href="http://creativecommons.org/licenses/by-nc/3.0/"><img alt="CC by-nc" src="Images/CC-by-nc.svg" height="50"/></a>
