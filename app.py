# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event
import json
import numpy as np
import numpy as nd
import numpy.ma as ma
import re

external_stylesheets = ['/assets/code.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions'] = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

import pandas as pd
import html5lib
from tabulate import tabulate
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pandas import DataFrame

server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
    <head>
	<meta charset="utf-8">
	
	<title>Modular Chemistry</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        
    </footer>
    </body>
</html>'''

defaults = '''<!DOCTYPE html>
<html>
    <head>
    <head>
	<meta charset="utf-8">
    </head>
    <body>
		<h4>Modular Chemistry</h4>
         <p>When I was fourteen I learnt modular arithmetic at school. The examples we got seemed to come in a pattern. The answers were always 2, 8, 7, or 2, 8, 5… This immediately got me thinking about the configuration of electrons in atomic shells. Perhaps, I thought, there was a connection between these two disciplines that would explain the mysterious pattern of the electron configuration once and for all. I later realised that there was no such link - at least not in the way I had envisaged. The relationship between the modular arithmetic examples and the electron configuration had been a mere coincidence (either that or whoever set the maths questions was trying to stimulate thought or possibly impart some kind of information).</p>
		<p>At first I tried to reconfigure the Periodic Table so that the electron count was based on remainder. This meant that a chemical reaction was balanced when the all of the elements summed to zero. Creating a table based on this method would make matching different stable reactions more easy. The problem is that modular arithmetic is only able to take place in a set number. So you can have mod 7 or mod 8, but you can’t have a number system that jumps around through different modular bases without rendering either one or all of them useless. And that is exactly what we see in electron configuration. The first orbital shell, called the “S” orbital only has 2 spaces for electrons to sit. The next shell, depending on which model you choose, either has 6 or 8 spaces. The first one is too complicated because it starts off at 2, then goes to 6, then back to 2, then 6 again and so on. Whereas the second one is much more regular in its way, starting off; 2, 8, 18. Obviously the number 8 appears here quite regularly, and since atoms with even numbers of electrons are generally less reactive than atoms with odd numbers (i.e. making them more stable) it is possible to rearrange this sequence into the following more manageable pattern; 2, 8, 2, 8, 8… The difficulty here is to deal with the twos, especially that beginning number two.</p>
		 <img src='/assets/mod-form.png'> 
		<p>I tried a number of different methods, trying to shoe horn the first two elements into the beginning or the end of my modular table and always succeeded in either putting the entire table out of whack or generally coming up with something unsatisfactory. Then I struck upon what I thought was a brilliant idea. Electron shells were circular and concentric in arrangement and here was me trying to push them into modular grid patterns. So, I decided to use a spiral pattern instead, which worked much better.</p>		<p>I selected the number 8 as my modular number system, which makes sense because it is the most obviously reoccurring numeral in electron configurations. This meant that I had a number system that went from 7 down to zero, with the numbers representing how many spaces were left for electrons to fill in each orbital. So if the number is zero, then you know that there are eight electrons in that shell, it is full (or very nearly full) and is not so reactive or entirely inert. Whereas if you have a 1, you know that there is only one electron needed in order to fill the shell, which means that this element is fairly reactive, but not as reactive as some as the alkaline metals, which are 1. The numeral 1 means that they are very reactive. The spiral made perfect sense because you could rotate the start point of the spiral into any position you want. In this case there were two atoms outside the mod 8 table; Hydrogen and Helium, which meant that I had to rotate the spiral around the modular table by a factor of two.</p>
		<p>This allows us, for the most part, to keep all of the alkaloids in their respective groupings with the other alkaloids, the halogens with the halogens and the noble gases, who don\'t like to interact with the other more common metals, off together in their own group. In the periodic table below, I have tried to stick to a certain colour scheme so that the different groupings can be identified and you can see that, for the most part there is a remarkable conformity among them. With this model you it is easy to see how different elements could match up to form compounds. For instance, Hydrogen, Fluorine, and Chlorine all need one more electron to fill their last electron shell, which means that they will all happily interact with each other. But they will also happily interact with any of the odd numbered elements, because two odds make an even. Even numbers will also happily interact with even numbers, as two evens also make up an even number, unless they are at 0, which means that they have become inert. So, 2 will interact with 4, 4 with itself and with 6 and so on. The image below explains this in a more intuitive fashion.</p>
		 <img src='/assets/mod_table_elements.png'> 
		<p>You may also notice in this new modular spiral rendition of the elemental table that some of the elements are repeated. This was a conscious decision I made not to leave any gaps, but it also helps get a better picture of just how interactive some of these elements are with each other, as the whole network becomes far more interconnected. Obviously, I could only use so many of the elements as I ran out of space. I suppose I could try to draw a bigger spiral, but I was afraid that it would take up too much space. So, instead I just decided to render all of the elements into a table, which works just as well.</p>		 <p>In any case, I was expecting that I would only be able to get a few more lines of elements done, before the whole modular system fell apart and I had to leave off. So I was pleasantly surprised when I was able to fit the entire table, all 118 elements (plus duplicates) into a single mod 8 table. The end result is, I think, quite pleasing and should be helpful to anyone looking to either memorise the table or become more familiar with how the different elements interact with each other. Meditation on the table may also bring to light new understandings of how the chemical elements complement each other and lead one down different and interesting areas of research and study.</p>
    <footer>
    </footer>
    </body>
</html>'''

app.layout = html.Div([
    html.Div([
        html.H1('Modular Chemisty', style={'font-size':100, 'margin-top':30}, className='seven columns'),
        html.Img( src="/assets/geogaff2.jpg", style={'width': '25%', 'float': 'right'}, className='five columns'),
    ], className = "row"),
    html.Hr(),
    html.Br(),
    html.P('This app was made for people who are interested in learning Chemisty and to demonstrate the fundamentals of Modular Chemistry. To use this app, simply select from one of the four Compound Structures; \'Organic\', \'Ionic\', \'Oxide\' or \'Hydroxide\' and then click on the names of the elements in the table below. To help you form stable compounds, you can refer to the numbers above the table. For instance, we see that \'Lithium\' is directly underneath the number 7, this means that it needs 7 electrons to form a stable compound, you can therefore click on any compound whose numbers add up to 8; \'Mg\' (6) and \'O\' (2) sum to 8, as does \'Boron\' (5) and three \'Hydrogens\' (1). This is called the Rule of Eight. Of course you can have compounds which are not as stable as these which sum to seven, or ten, even twenty, so this is more of a guideline (or rule of thumb) rather than a strict rule. As you move further down into the centre of the periodic table, the Rule of Eight becomes less applicable, as the number of electron spaces increases from 8 to 18 to 32, this is why some of the elements in this area are repeated twice, to show that they can accept more electrons. If you play around with this you might be able to discover new compounds or existing ones. If the compound you find is in our databse, you will recieve a printout with the Chemical Name, Synonym and CAS Number. When this happens information from Wikipedia will (more often than not) appear on the screen. NOTE: This feature is still in Beta and can return unexpected results. You must hit the reset button to clear the field and start a new compound structure. Disclaimer; the app is super slow at times, have patience and trust the program; It should work.' ,
    className="ten columns offset-by-one"),
    html.Br(),
    html.H4(children='Table of Elements',
    className="eleven columns offset-by-one"),
    html.Div([
            html.Div([
                html.Button('7', id='7', n_clicks = 0, style={'width':'11.9%'}),
                html.Button('6', id='6', n_clicks = 0, style={'width':'11.9%'}),
                html.Button('5', id='5', n_clicks = 0, style={'width':'11.9%'}),
                html.Button('4', id='4', n_clicks = 0, style={'width':'11.9%'}),
                html.Button('3', id='3', n_clicks = 0, style={'width':'11.9%'}),
                html.Button('2', id='2', n_clicks = 0, style={'width':'11.9%'}),
                html.Button('1', id='1', n_clicks = 0, style={'width':'11.9%'}),
                html.Button('0', id='0', n_clicks = 0, style={'width':'11.9%'}),
			], className="ten columns offset-by-one"),
            html.Div([
                html.Button('_', style={'width':'11.9%', 'color':'white', 'background-color':'white'}),
                html.Button('_', style={'width':'11.9%', 'color':'white', 'background-color':'white'}),
                html.Button('_', style={'width':'11.9%', 'color':'white', 'background-color':'white'}),
                html.Button('_', style={'width':'11.9%', 'color':'white', 'background-color':'white'}),
                html.Button('_', style={'width':'11.9%', 'color':'white', 'background-color':'white'}),
                html.Button('_', style={'width':'11.9%', 'color':'white', 'background-color':'white'}),
                html.Button('Hydrogen', id='H', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(103, 179, 221)'}),
                html.Button('Helium', id='He', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(107, 38, 131)'}),
			], className="ten columns offset-by-one"),
            html.Div([
                html.Button('Lithium', id='Li', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(252, 48, 45)'}),
                html.Button('Berylium', id='Be', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':' rgb(253, 169, 71)'}),
                html.Button('Boron', id='B', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':' rgb(77, 156, 199)'}),
                html.Button('Carbon', id='C', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(103, 179, 221)'}),
                html.Button('Nitrogen', id='N', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(103, 179, 221)'}),
                html.Button('Oxygen', id='O', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(103, 179, 221)'}),
                html.Button('Flourine', id='F', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(154, 72, 180)'}),
                html.Button('Neon', id='Ne', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(107, 38, 131)'}),
			], className="ten columns offset-by-one"),
            html.Div([
                html.Button('Sodium', id='Na', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(252, 48, 45)'}),
                html.Button('Magnesium', id='Mg', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(253, 169, 71)'}),
                html.Button('Aluminium', id='Al', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(158, 224, 98)'}),
                html.Button('Silicon', id='Si', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(77, 156, 199)'}),
                html.Button('Phosorous', id='P', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(103, 179, 221'}),
                html.Button('Sulphur', id='S', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(103, 179, 221'}),
                html.Button('Chlorine', id='Cl', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(154, 72, 180)'}),
                html.Button('Argon', id='Ar', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(107, 38, 131)'}),
			], className="ten columns offset-by-one"),
            html.Div([
                html.Button('Potassium', id='K', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(252, 48, 45)'}),
                html.Button('Calcium', id='Ca', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(253, 169, 71)'}),
                html.Button('Scandium', id='Sc', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Titanium', id='Ti', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Vanadium', id='V', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Chromium', id='Cr', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Potassium', id='K1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(252, 48, 45)'}),
                html.Button('Calcium', id='Ca1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(253, 169, 71)'}),
			], className="ten columns offset-by-one"),
			html.Div([
                html.Button('Scandium', id='Sc1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Titanium', id='Ti1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Vanadium', id='V1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Chromium', id='Cr1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Manganese', id='Mn', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Iron', id='Fe', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Cobalt', id='Co', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Nickel', id='Ni', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
			], className="ten columns offset-by-one"),	
            html.Div([
                html.Button('Copper', id='Cu', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Zinc', id='Zn', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Gallium', id='Ga', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(158, 224, 98)'}),
                html.Button('Germanium', id='Ge', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(77, 156, 199)'}),
                html.Button('Arsenic', id='As', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(77, 156, 199)'}),
                html.Button('Selenium', id='Se', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(103, 179, 221)'}),
                html.Button('Bromium', id='Br', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(154, 72, 180)'}),
                html.Button('Krypton', id='Kr', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(107, 38, 131)'}),
			], className="ten columns offset-by-one"),
            html.Div([
                html.Button('Rubinium', id='Rb', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(252, 48, 45)'}),
                html.Button('Strontium', id='Sr', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(253, 169, 71)'}),
                html.Button('Yttrium', id='Y', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Zirconium', id='Zr', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Niobium', id='Nb', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Molybdenum', id='Mo', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Rubinium', id='Rb1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(252, 48, 45)'}),
                html.Button('Strontium', id='Sr1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(253, 169, 71)'}),
			], className="ten columns offset-by-one"),
            html.Div([
                html.Button('Yttrium', id='Y1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Zirconium', id='Zr1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Niobium', id='Nb1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Molybdenum', id='Mo1', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Technetium', id='Tc', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Ruthenium', id='Ru', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Rhodium', id='Rh', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Palladium', id='Pd', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
			], className="ten columns offset-by-one"),
            html.Div([
                html.Button('Silver', id='Ag', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Cadmium', id='Cd', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Indium', id='In', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(158, 224, 98)'}),
                html.Button('Tin', id='Sn', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(158, 224, 98)'}),
                html.Button('Antimony', id='Sb', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(77, 156, 199)'}),
                html.Button('Tellurium', id='Te', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(77, 156, 199)'}),
                html.Button('Iodine', id='I', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(154, 72, 180)'}),
                html.Button('Xenon', id='Xe', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(107, 38, 131)'}),
			], className="ten columns offset-by-one"),
			            html.Div([
                html.Button('Cesium', id='Cs', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(252, 48, 45)'}),
                html.Button('Barium', id='Ba', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(253, 169, 71)'}),
                html.Button('Lanthanum', id='La', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Cerium', id='Ce', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Praseodymium', id='Pr', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Neodymium', id='Nd', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Promethium', id='Pm', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Samarium', id='Sm', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
			], className="ten columns offset-by-one"),
            html.Div([
                html.Button('Europium', id='Eu', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Gadolinium', id='Gd', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Terbium', id='Tb', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Dysprosium', id='Dy', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Holmium', id='Ho', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Erbium', id='Er', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Thulium', id='Tm', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Ytterbium', id='Yb', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
			], className="ten columns offset-by-one"),
			html.Div([
                html.Button('Lutetium', id='Lu', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Hafnium', id='Hf', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Tantalum', id='Ta', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Tungsten', id='W', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Rhenium', id='Re', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Osmium', id='Os', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Iridium', id='Ir', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Platinum', id='Pt', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
			], className="ten columns offset-by-one"),
			html.Div([
                html.Button('Gold', id='Au', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Mercury', id='Hg', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Thallium', id='Tl', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(158, 224, 98)'}),
                html.Button('Lead', id='Pb', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(158, 224, 98)'}),
                html.Button('Bismuth', id='Bi', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(158, 224, 98)'}),
                html.Button('Polonium', id='Po', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(103, 179, 221)'}),
                html.Button('Astatine', id='At', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(154, 72, 180)'}),
                html.Button('Radon', id='Rn', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(107, 38, 131)'}),
			], className="ten columns offset-by-one"),
			html.Div([
                html.Button('Francium', id='Fr', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(252, 48, 45)'}),
                html.Button('Radium', id='Ra', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(253, 169, 71)'}),
                html.Button('Actinium', id='Ac', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Thorium', id='Th', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Protactinium', id='Pa', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Uranium', id='U', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Neptunium', id='Np', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Plutonium', id='Pu', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
			], className="ten columns offset-by-one"),
			html.Div([
                html.Button('Americium', id='Am', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Curium', id='Cm', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Berkelium', id='Bk', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Californium', id='Cf', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Einsteinium', id='Es', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Fermium', id='Fm', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Mendelevium', id='Md', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Nobelium', id='No', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
			], className="ten columns offset-by-one"),
			html.Div([
                html.Button('Lawrencium', id='Lr', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
                html.Button('Rutherfordiu', id='Rf', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Dubnium', id='Db', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Seaborgium', id='Sg', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Bohrium', id='Bh', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Hassium', id='Hs', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Meitnerium', id='Mt', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Darmstadtium', id='Ds', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(113, 191, 66)'}),
			], className="ten columns offset-by-one"),
			html.Div([
                html.Button('Roentgenium', id='Rg', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Copernicium', id='Cn', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(254, 223, 107)'}),
                html.Button('Nihonium', id='Uut', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(158, 224, 98)'}),
                html.Button('Flerovium', id='Fl', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(158, 224, 98)'}),
                html.Button('Moscovium', id='Uup', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(158, 224, 98)'}),
                html.Button('Livermorium', id='Lv', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(158, 224, 98)'}),
                html.Button('Tennessine', id='Uus', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(154, 72, 180)'}),
                html.Button('Oganesson', id='Uuo', n_clicks = 0, style={'width':'11.9%', 'color':'white', 'background-color':'rgb(107, 38, 131)'}),
			], className="ten columns offset-by-one"),		
	], className="row"),
    html.Br(),
    html.Div([
            html.Hr(style={'width':'80%'}, className='ten columns offset-by-one'),
                html.Button('Organic', id='organic', n_clicks_timestamp='1', style={'width':'11.9%', 'color': 'white', 'background-color':'rgb(253, 169, 71)'},
			className="two columns offset-by-one"),
                html.Button('Ionic', id='ionic', n_clicks_timestamp='0', style={'width':'11.9%', 'color': 'white', 'background-color':'rgb(253, 169, 71)'},
			className="two columns"),
                html.Button('Oxides', id='oxide',n_clicks_timestamp='0', style={'width':'11.9%', 'color':'white', 'background-color':'rgb(253, 169, 71)'},
			className="two columns"),
                html.Button('Hydroxides', id='hydro', n_clicks_timestamp='0', style={'width':'11.9%', 'color':'white', 'background-color':'rgb(253, 169, 71)'},
			className="two columns"),
                html.Button('Reset', id='reset', n_clicks_timestamp='0', style={'width':'11.9%', 'color': 'black', 'background-color':'white'},
            className="two columns"),
	], className="row"),
    html.Br(),
    html.Div(id='inter-button', style={'display': 'none'}),
    html.Div([
            html.Div(id='container',
            className="five columns offset-by-one")
    ], className="row"),
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Div([
        dcc.Textarea(id='textbox-1', readOnly = 'False', style={'width': '30%', 'border-radius': 1, 'resize':'none'},
        className='four columns offset-by-one'),
        dcc.Textarea(id='textbox-2', readOnly = 'False', style={'width': '40%', 'border-radius': 1, 'resize':'none'},
        className='four columns offset-by-onehalf'),
    ], className="row"),
    html.Br(),
    html.Div(id='interweb', style={'display': 'none'}),
    html.Div([
            html.Div(id='container2'),
    ], className="row"),
    html.Br(),
    html.Div([
        html.Br(),
        html.Hr(),
        html.Br(),
        html.Footer(
            html.Center(
            dcc.Markdown('''[Cataphysical Research Society - 2019.](cataphysical-research-society.herokuapp.com)''')),
        ),
        html.Br(),
    ], className = "row"),
])

@app.callback(
    Output('H', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('He', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Li', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Be', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('B', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('C', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('N', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('O', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('F', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ne', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Na', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Mg', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Al', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Si', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('P', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('S', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Cl', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ar', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('K', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ca', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Sc', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ti', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('V', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Cr', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('K1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ca1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Sc1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ti1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('V1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Cr1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Mn', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Fe', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Co', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ni', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Cu', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Zn', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ga', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ge', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('As', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Se', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Br', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Kr', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Rb', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Sr', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Y', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Zr', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Nb', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Mo', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Rb1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Sr1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Y1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Zr1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Nb1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Mo1', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Tc', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ru', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Rh', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Pd', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ag', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Cd', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('In', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Sn', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Sb', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Te', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('I', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Xe', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Cs', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ba', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('La', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ce', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Pr', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Nd', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Pm', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Sm', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Eu', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Gd', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Tb', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Dy', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ho', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Er', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Tm', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Yb', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Lu', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Hf', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ta', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('W', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Re', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Os', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ir', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Pt', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Au', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Hg', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Tl', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Pb', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Bi', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Po', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('At', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Rn', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Fr', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ra', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ac', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Th', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Pa', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('U', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Np', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Pu', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Am', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Cm', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Bk', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Cf', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Es', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Fm', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Md', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('No', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Lr', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Rf', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Db', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Sg', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Bh', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Hs', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Mt', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Ds', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Rg', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Cn', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Uut', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Fl', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Uup', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Lv', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Uus', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output('Uuo', 'n_clicks'),
    events=[Event('reset', 'click')])
def update():
    return 0

@app.callback(
    Output(component_id='inter-button', component_property='children'),
    [Input(component_id='organic', component_property='n_clicks_timestamp'),
    Input(component_id='ionic', component_property='n_clicks_timestamp'),
    Input(component_id='oxide', component_property='n_clicks_timestamp'),
    Input(component_id='hydro', component_property='n_clicks_timestamp')])
def update(organic, ionic, oxide, hydro):
    if int(organic) > int(ionic) and int(organic) > int(oxide):
        if int(organic) > int(hydro):
            compound='organic'
            return json.dumps(compound)
    elif int(ionic) > int(organic) and int(ionic) > int(oxide):
        if int(ionic) > int(hydro):
            compound='ionic'
            return json.dumps(compound)
    elif int(oxide) > int(organic) and int(oxide) > int(ionic):
        if int(oxide) > int(hydro):
            compound='oxide'
            return json.dumps(compound)
    start = True
    while start and int(hydro) > int(organic) and int(hydro) > int(ionic) and int(hydro) > int(oxide):
        compound='hydro'
        return json.dumps(compound)
        start = False 


@app.callback(dash.dependencies.Output('intermediate-value', 'children'),
 					  [dash.dependencies.Input('inter-button', 'children'),
     					dash.dependencies.Input('H', 'n_clicks'),
     					dash.dependencies.Input('He', 'n_clicks'),
     					dash.dependencies.Input('Li', 'n_clicks'),
     					dash.dependencies.Input('Be', 'n_clicks'),
     					dash.dependencies.Input('B', 'n_clicks'),
     					dash.dependencies.Input('C', 'n_clicks'),
     					dash.dependencies.Input('N', 'n_clicks'),
     					dash.dependencies.Input('O', 'n_clicks'),
     					dash.dependencies.Input('F', 'n_clicks'),
     					dash.dependencies.Input('Ne', 'n_clicks'),
     					dash.dependencies.Input('Na', 'n_clicks'),
     					dash.dependencies.Input('Mg', 'n_clicks'),
     					dash.dependencies.Input('Al', 'n_clicks'),
     					dash.dependencies.Input('Si', 'n_clicks'),
     					dash.dependencies.Input('P', 'n_clicks'),
     					dash.dependencies.Input('S', 'n_clicks'),
     					dash.dependencies.Input('Cl', 'n_clicks'),
     					dash.dependencies.Input('Ar', 'n_clicks'),
     					dash.dependencies.Input('K', 'n_clicks'),
     					dash.dependencies.Input('Ca', 'n_clicks'),
     					dash.dependencies.Input('Sc', 'n_clicks'),
     					dash.dependencies.Input('Ti', 'n_clicks'),
     					dash.dependencies.Input('V', 'n_clicks'),
     					dash.dependencies.Input('Cr', 'n_clicks'),
     					dash.dependencies.Input('K1', 'n_clicks'),
     					dash.dependencies.Input('Ca1', 'n_clicks'),
     					dash.dependencies.Input('Sc1', 'n_clicks'),
     					dash.dependencies.Input('Ti1', 'n_clicks'),
     					dash.dependencies.Input('V1', 'n_clicks'),
     					dash.dependencies.Input('Cr1', 'n_clicks'),
     					dash.dependencies.Input('Mn', 'n_clicks'),
     					dash.dependencies.Input('Fe', 'n_clicks'),
     					dash.dependencies.Input('Co', 'n_clicks'),
     					dash.dependencies.Input('Ni', 'n_clicks'),
     					dash.dependencies.Input('Cu', 'n_clicks'),
     					dash.dependencies.Input('Zn', 'n_clicks'),
     					dash.dependencies.Input('Ga', 'n_clicks'),
     					dash.dependencies.Input('Ge', 'n_clicks'),
     					dash.dependencies.Input('As', 'n_clicks'),
     					dash.dependencies.Input('Se', 'n_clicks'),
     					dash.dependencies.Input('Br', 'n_clicks'),
     					dash.dependencies.Input('Kr', 'n_clicks'),
     					dash.dependencies.Input('Rb', 'n_clicks'),
     					dash.dependencies.Input('Sr', 'n_clicks'),
     					dash.dependencies.Input('Y', 'n_clicks'),
     					dash.dependencies.Input('Zr', 'n_clicks'),
     					dash.dependencies.Input('Nb', 'n_clicks'),
     					dash.dependencies.Input('Mo', 'n_clicks'),
     					dash.dependencies.Input('Rb1', 'n_clicks'),
     					dash.dependencies.Input('Sr1', 'n_clicks'),
     					dash.dependencies.Input('Y1', 'n_clicks'),
     					dash.dependencies.Input('Zr1', 'n_clicks'),
     					dash.dependencies.Input('Nb1', 'n_clicks'),
     					dash.dependencies.Input('Mo1', 'n_clicks'),
     					dash.dependencies.Input('Tc', 'n_clicks'),
     					dash.dependencies.Input('Ru', 'n_clicks'),
     					dash.dependencies.Input('Rh', 'n_clicks'),
     					dash.dependencies.Input('Pd', 'n_clicks'),
     					dash.dependencies.Input('Ag', 'n_clicks'),
     					dash.dependencies.Input('Cd', 'n_clicks'),
     					dash.dependencies.Input('In', 'n_clicks'),
     					dash.dependencies.Input('Sn', 'n_clicks'),
     					dash.dependencies.Input('Sb', 'n_clicks'),
     					dash.dependencies.Input('Te', 'n_clicks'),
     					dash.dependencies.Input('I', 'n_clicks'),
     					dash.dependencies.Input('Xe', 'n_clicks'),
     					dash.dependencies.Input('Cs', 'n_clicks'),
     					dash.dependencies.Input('Ba', 'n_clicks'),
     					dash.dependencies.Input('La', 'n_clicks'),
     					dash.dependencies.Input('Ce', 'n_clicks'),
     					dash.dependencies.Input('Pr', 'n_clicks'),
     					dash.dependencies.Input('Nd', 'n_clicks'),
     					dash.dependencies.Input('Pm', 'n_clicks'),
     					dash.dependencies.Input('Sm', 'n_clicks'),
     					dash.dependencies.Input('Eu', 'n_clicks'),
     					dash.dependencies.Input('Gd', 'n_clicks'),
     					dash.dependencies.Input('Tb', 'n_clicks'),
     					dash.dependencies.Input('Dy', 'n_clicks'),
     					dash.dependencies.Input('Ho', 'n_clicks'),
     					dash.dependencies.Input('Er', 'n_clicks'),
     					dash.dependencies.Input('Tm', 'n_clicks'),
     					dash.dependencies.Input('Yb', 'n_clicks'),
     					dash.dependencies.Input('Lu', 'n_clicks'),
     					dash.dependencies.Input('Hf', 'n_clicks'),
     					dash.dependencies.Input('Ta', 'n_clicks'),
     					dash.dependencies.Input('W', 'n_clicks'),
     					dash.dependencies.Input('Re', 'n_clicks'),
     					dash.dependencies.Input('Os', 'n_clicks'),
     					dash.dependencies.Input('Ir', 'n_clicks'),
     					dash.dependencies.Input('Pt', 'n_clicks'),
     					dash.dependencies.Input('Au', 'n_clicks'),
     					dash.dependencies.Input('Hg', 'n_clicks'),
     					dash.dependencies.Input('Tl', 'n_clicks'),
     					dash.dependencies.Input('Pb', 'n_clicks'),
     					dash.dependencies.Input('Bi', 'n_clicks'),
     					dash.dependencies.Input('Po', 'n_clicks'),
     					dash.dependencies.Input('At', 'n_clicks'),
     					dash.dependencies.Input('Rn', 'n_clicks'),
     					dash.dependencies.Input('Fr', 'n_clicks'),
     					dash.dependencies.Input('Ra', 'n_clicks'),
     					dash.dependencies.Input('Ac', 'n_clicks'),
     					dash.dependencies.Input('Th', 'n_clicks'),
     					dash.dependencies.Input('Pa', 'n_clicks'),
     					dash.dependencies.Input('U', 'n_clicks'),
     					dash.dependencies.Input('Np', 'n_clicks'),
     					dash.dependencies.Input('Pu', 'n_clicks'),
     					dash.dependencies.Input('Am', 'n_clicks'),
     					dash.dependencies.Input('Cm', 'n_clicks'),
     					dash.dependencies.Input('Bk', 'n_clicks'),
     					dash.dependencies.Input('Cf', 'n_clicks'),
     					dash.dependencies.Input('Es', 'n_clicks'),
     					dash.dependencies.Input('Fm', 'n_clicks'),
     					dash.dependencies.Input('Md', 'n_clicks'),
     					dash.dependencies.Input('No', 'n_clicks'),
     					dash.dependencies.Input('Lr', 'n_clicks'),
     					dash.dependencies.Input('Rf', 'n_clicks'),
     					dash.dependencies.Input('Db', 'n_clicks'),
     					dash.dependencies.Input('Sg', 'n_clicks'),
     					dash.dependencies.Input('Bh', 'n_clicks'),
     					dash.dependencies.Input('Hs', 'n_clicks'),
     					dash.dependencies.Input('Mt', 'n_clicks'),
     					dash.dependencies.Input('Ds', 'n_clicks'),
     					dash.dependencies.Input('Rg', 'n_clicks'),
     					dash.dependencies.Input('Cn', 'n_clicks'),
     					dash.dependencies.Input('Uut', 'n_clicks'),
     					dash.dependencies.Input('Fl', 'n_clicks'),
     					dash.dependencies.Input('Uup', 'n_clicks'),
     					dash.dependencies.Input('Lv', 'n_clicks'),
     					dash.dependencies.Input('Uus', 'n_clicks'),
     					dash.dependencies.Input('Uuo', 'n_clicks')])
def func(inter_button, H, He, Li, Be, B, C, N, O, F, Ne, Na, Mg, Al, Si, P, S, Cl, Ar, K, Ca, Sc, Ti, V, Cr, K1, Ca1, Sc1, Ti1, V1, Cr1, Mn, Fe, Co, Ni, Cu, Zn, Ga, Ge, As, Se, Br, Kr, Rb, Sr, Y, Zr, Nb, Mo, Rb1, Sr1, Y1, Zr1, Nb1, Mo1, Tc, Ru, Rh, Pd, Ag, Cd, In, Sn, Sb, Te, I, Xe, Cs, Ba, La, Ce, Pr, Nd, Pm, Sm, Eu, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu, Hf, Ta, W, Re, Os, Ir, Pt, Au, Hg, Tl, Pb, Bi, Po, At, Rn, Fr, Ra, Ac, Th, Pa, U, Np, Pu, Am, Cm, Bk, Cf, Es, Fm, Md, No, Lr, Rf, Db, Sg, Bh, Hs, Mt, Ds, Rg, Cn, Uut, Fl, Uup, Lv, Uus, Uuo):
    button = json.loads(inter_button)
    elements = nd.array(['C', 'H', 'Ac', 'Ag', 'Al', 'Am', 'Ar', 'As', 'At', 'Au', 'B', 'Ba', 'Be', 'Bh', 'Bi', 'Bk', 'Br', 'Ca', 'Ca', 'Cd', 'Ce', 'Cf', 'Cl', 'Cm', 'Cn', 'Co', 'Cr', 'Cr', 'Cs', 'Cu', 'Db', 'Ds', 'Dy', 'Er', 'Es', 'Eu', 'F', 'Fe', 'Fl', 'Fm', 'Fr', 'Ga', 'Gd', 'Ge', 'He', 'Hf', 'Hg', 'Ho', 'Hs', 'I', 'In', 'Ir', 'K', 'K', 'Kr', 'La', 'Li', 'Lr', 'Lu', 'Lv', 'Md', 'Mg', 'Mn', 'Mo', 'Mo', 'Mt', 'N', 'Na', 'Nb', 'Nb', 'Nd', 'Ne', 'Ni', 'No', 'Np', 'O', 'Os', 'P', 'Pa', 'Pb', 'Pd', 'Pm', 'Po', 'Pr', 'Pt', 'Pu', 'Ra', 'Rb', 'Rb', 'Re', 'Rf', 'Rg', 'Rh', 'Rn', 'Ru', 'S', 'Sb', 'Sc', 'Sc', 'Se', 'Sg', 'Si', 'Sm', 'Sn', 'Sr', 'Sr', 'Ta', 'Tb', 'Tc', 'Te', 'Th', 'Ti', 'Ti', 'Tl', 'Tm', 'U', 'Uuo', 'Uup', 'Uus', 'Uut', 'V', 'V', 'W', 'Xe', 'Y', 'Y', 'Yb', 'Zn', 'Zr', 'Zr'])
    clicks = np.array([int(C), int(H), int(Ac), int(Ag), int(Al), int(Am), int(Ar), int(As), int(At), int(Au), int(B), int(Ba), int(Be), int(Bh), int(Bi), int(Bk), int(Br), int(Ca), int(Ca1), int(Cd), int(Ce), int(Cf), int(Cl), int(Cm), int(Cn), int(Co), int(Cr), int(Cr1), int(Cs), int(Cu), int(Db), int(Ds), int(Dy), int(Er), int(Es), int(Eu), int(F), int(Fe), int(Fl), int(Fm), int(Fr), int(Ga), int(Gd), int(Ge), int(He), int(Hf), int(Hg), int(Ho), int(Hs), int(I), int(In), int(Ir), int(K), int(K1), int(Kr), int(La), int(Li), int(Lr), int(Lu), int(Lv), int(Md), int(Mg), int(Mn), int(Mo), int(Mo1), int(Mt), int(N), int(Na), int(Nb), int(Nb1), int(Nd), int(Ne), int(Ni), int(No), int(Np), int(O), int(Os), int(P), int(Pa), int(Pb), int(Pd), int(Pm), int(Po), int(Pr), int(Pt), int(Pu), int(Ra), int(Rb), int(Rb1), int(Re), int(Rf), int(Rg), int(Rh), int(Rn), int(Ru), int(S), int(Sb), int(Sc), int(Sc1), int(Se), int(Sg), int(Si), int(Sm), int(Sn), int(Sr), int(Sr1), int(Ta), int(Tb), int(Tc), int(Te), int(Th), int(Ti), int(Ti1), int(Tl), int(Tm), int(U), int(Uuo), int(Uup), int(Uus), int(Uut), int(V), int(V1), int(W), int(Xe), int(Y), int(Y1), int(Yb), int(Zn), int(Zr), int(Zr1)])
    ions = nd.array(['Cs', 'Fr', 'K', 'K', 'Rb', 'Rb', 'Ba', 'Ra', 'Na', 'Sr', 'Sr', 'Li', 'Ca', 'Ca', 'Yb', 'La', 'Ac', 'Ce', 'Pr', 'Pm', 'Nd', 'Sm', 'Tb', 'Gd', 'Eu', 'Dy', 'Y', 'Y', 'Ho', 'Er', 'Tm', 'Lu', 'Pu', 'No', 'Es', 'Th', 'Hf', 'Md', 'Bk', 'Am', 'Lr', 'Cf', 'Cm', 'Fm', 'Mg', 'Zr', 'Zr', 'Np', 'Sc', 'Sc', 'U', 'Ta', 'Pa', 'Ti', 'Ti', 'Mn', 'Be', 'Nb', 'Nb', 'Al', 'V', 'V', 'Zn', 'Cr', 'Cr', 'Cd', 'In', 'Ga', 'Fe', 'Co', 'Si', 'Re', 'Tc', 'Cu', 'Ni', 'Ag', 'Sn', 'Po', 'Hg', 'Ge', 'Bi', 'Tl', 'B', 'Sb', 'Te', 'Mo', 'Mo', 'As', 'P', 'H', 'Ir', 'Ru', 'Os', 'At', 'Rn', 'Pd', 'Pt', 'Rh', 'Pb', 'W', 'Au', 'C', 'Se', 'S', 'Xe', 'I', 'Br', 'Kr', 'N', 'Cl', 'O', 'F', 'He', 'Ne', 'Ar', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Uut', 'Fl', 'Uup', 'Lv', 'Uus', 'Uuo'])
    ionclicks = np.array([int(Cs), int(Fr), int(K), int(K1), int(Rb), int(Rb1), int(Ba), int(Ra), int(Na), int(Sr), int(Sr1), int(Li), int(Ca), int(Ca1), int(Yb), int(La), int(Ac), int(Ce), int(Pr), int(Pm), int(Nd), int(Sm), int(Tb), int(Gd), int(Eu), int(Dy), int(Y), int(Y1), int(Ho), int(Er), int(Tm), int(Lu), int(Pu), int(No), int(Es), int(Th), int(Hf), int(Md), int(Bk), int(Am), int(Lr), int(Cf), int(Cm), int(Fm), int(Mg), int(Zr), int(Zr1), int(Np), int(Sc), int(Sc1), int(U), int(Ta), int(Pa), int(Ti), int(Ti1), int(Mn), int(Be), int(Nb), int(Nb1), int(Al), int(V), int(V1), int(Zn), int(Cr), int(Cr1), int(Cd), int(In), int(Ga), int(Fe), int(Co), int(Si), int(Re), int(Tc), int(Cu), int(Ni), int(Ag), int(Sn), int(Po), int(Hg), int(Ge), int(Bi), int(Tl), int(B), int(Sb), int(Te), int(Mo), int(Mo1), int(As), int(P), int(H), int(Ir), int(Ru), int(Os), int(At), int(Rn), int(Pd), int(Pt), int(Rh), int(Pb), int(W), int(Au), int(C), int(Se), int(S), int(Xe), int(I), int(Br), int(Kr), int(N), int(Cl), int(O), int(F), int(He), int(Ne), int(Ar), int(Rf), int(Db), int(Sg), int(Bh), int(Hs), int(Mt), int(Ds), int(Rg), int(Cn), int(Uut), int(Fl), int(Uup), int(Lv), int(Uus), int(Uuo)])
    oxelements = nd.array(['Ac', 'Ag', 'Al', 'Am', 'Ar', 'As', 'At', 'Au', 'B', 'Ba', 'Be', 'Bh', 'Bi', 'Bk', 'Br', 'C', 'Ca', 'Ca', 'Cd', 'Ce', 'Cf', 'Cl', 'Cm', 'Cn', 'Co', 'Cr', 'Cr', 'Cs', 'Cu', 'Db', 'Ds', 'Dy', 'Er', 'Es', 'Eu', 'F', 'Fe', 'Fl', 'Fm', 'Fr', 'Ga', 'Gd', 'Ge', 'H', 'He', 'Hf', 'Hg', 'Ho', 'Hs', 'I', 'In', 'Ir', 'K', 'K', 'Kr', 'La', 'Li', 'Lr', 'Lu', 'Lv', 'Md', 'Mg', 'Mn', 'Mo', 'Mo', 'Mt', 'N', 'Na', 'Nb', 'Nb', 'Nd', 'Ne', 'Ni', 'No', 'Np', 'Os', 'P', 'Pa', 'Pb', 'Pd', 'Pm', 'Po', 'Pr', 'Pt', 'Pu', 'Ra', 'Rb', 'Rb', 'Re', 'Rf', 'Rg', 'Rh', 'Rn', 'Ru', 'S', 'Sb', 'Sc', 'Sc', 'Se', 'Sg', 'Si', 'Sm', 'Sn', 'Sr', 'Sr', 'Ta', 'Tb', 'Tc', 'Te', 'Th', 'Ti', 'Ti', 'Tl', 'Tm', 'U', 'Uuo', 'Uup', 'Uus', 'Uut', 'V', 'V', 'W', 'Xe', 'Y', 'Y', 'Yb', 'Zn', 'Zr', 'Zr', 'O'])
    oxclicks = np.array([int(Ac), int(Ag), int(Al), int(Am), int(Ar), int(As), int(At), int(Au), int(B), int(Ba), int(Be), int(Bh), int(Bi), int(Bk), int(Br), int(C), int(Ca), int(Ca1), int(Cd), int(Ce), int(Cf), int(Cl), int(Cm), int(Cn), int(Co), int(Cr), int(Cr1), int(Cs), int(Cu), int(Db), int(Ds), int(Dy), int(Er), int(Es), int(Eu), int(F), int(Fe), int(Fl), int(Fm), int(Fr), int(Ga), int(Gd), int(Ge), int(H), int(He), int(Hf), int(Hg), int(Ho), int(Hs), int(I), int(In), int(Ir), int(K), int(K1), int(Kr), int(La), int(Li), int(Lr), int(Lu), int(Lv), int(Md), int(Mg), int(Mn), int(Mo), int(Mo1), int(Mt), int(N), int(Na), int(Nb), int(Nb1), int(Nd), int(Ne), int(Ni), int(No), int(Np), int(Os), int(P), int(Pa), int(Pb), int(Pd), int(Pm), int(Po), int(Pr), int(Pt), int(Pu), int(Ra), int(Rb), int(Rb1), int(Re), int(Rf), int(Rg), int(Rh), int(Rn), int(Ru), int(S), int(Sb), int(Sc), int(Sc1), int(Se), int(Sg), int(Si), int(Sm), int(Sn), int(Sr), int(Sr1), int(Ta), int(Tb), int(Tc), int(Te), int(Th), int(Ti), int(Ti1), int(Tl), int(Tm), int(U), int(Uuo), int(Uup), int(Uus), int(Uut), int(V), int(V1), int(W), int(Xe), int(Y), int(Y1), int(Yb), int(Zn), int(Zr), int(Zr1), int(O)])
    hydelements = nd.array(['Ac', 'Ag', 'Al', 'Am', 'Ar', 'As', 'At', 'Au', 'B', 'Ba', 'Be', 'Bh', 'Bi', 'Bk', 'Br', 'C', 'Ca', 'Ca', 'Cd', 'Ce', 'Cf', 'Cl', 'Cm', 'Cn', 'Co', 'Cr', 'Cr', 'Cs', 'Cu', 'Db', 'Ds', 'Dy', 'Er', 'Es', 'Eu', 'F', 'Fe', 'Fl', 'Fm', 'Fr', 'Ga', 'Gd', 'Ge', 'He', 'Hf', 'Hg', 'Ho', 'Hs', 'I', 'In', 'Ir', 'K', 'K1', 'Kr', 'La', 'Li', 'Lr', 'Lu', 'Lv', 'Md', 'Mg', 'Mn', 'Mo', 'Mo', 'Mt', 'N', 'Na', 'Nb', 'Nb', 'Nd', 'Ne', 'Ni', 'No', 'Np', 'Os', 'P', 'Pa', 'Pb', 'Pd', 'Pm', 'Po', 'Pr', 'Pt', 'Pu', 'Ra', 'Rb', 'Rb', 'Re', 'Rf', 'Rg', 'Rh', 'Rn', 'Ru', 'S', 'Sb', 'Sc', 'Sc', 'Se', 'Sg', 'Si', 'Sm', 'Sn', 'Sr', 'Sr', 'Ta', 'Tb', 'Tc', 'Te', 'Th', 'Ti', 'Ti', 'Tl', 'Tm', 'U', 'Uuo', 'Uup', 'Uus', 'Uut', 'V', 'V', 'W', 'Xe', 'Y', 'Y', 'Yb', 'Zn', 'Zr', 'Zr', 'O', 'H'])
    hydclicks = np.array([int(Ac), int(Ag), int(Al), int(Am), int(Ar), int(As), int(At), int(Au), int(B), int(Ba), int(Be), int(Bh), int(Bi), int(Bk), int(Br), int(C), int(Ca), int(Ca1), int(Cd), int(Ce), int(Cf), int(Cl), int(Cm), int(Cn), int(Co), int(Cr), int(Cr1), int(Cs), int(Cu), int(Db), int(Ds), int(Dy), int(Er), int(Es), int(Eu), int(F), int(Fe), int(Fl), int(Fm), int(Fr), int(Ga), int(Gd), int(Ge), int(He), int(Hf), int(Hg), int(Ho), int(Hs), int(I), int(In), int(Ir), int(K), int(K1), int(Kr), int(La), int(Li), int(Lr), int(Lu), int(Lv), int(Md), int(Mg), int(Mn), int(Mo), int(Mo1), int(Mt), int(N), int(Na), int(Nb), int(Nb1), int(Nd), int(Ne), int(Ni), int(No), int(Np), int(Os), int(P), int(Pa), int(Pb), int(Pd), int(Pm), int(Po), int(Pr), int(Pt), int(Pu), int(Ra), int(Rb), int(Rb1), int(Re), int(Rf), int(Rg), int(Rh), int(Rn), int(Ru), int(S), int(Sb), int(Sc), int(Sc1), int(Se), int(Sg), int(Si), int(Sm), int(Sn), int(Sr), int(Sr1), int(Ta), int(Tb), int(Tc), int(Te), int(Th), int(Ti), int(Ti1), int(Tl), int(Tm), int(U), int(Uuo), int(Uup), int(Uus), int(Uut), int(V), int(V1), int(W), int(Xe), int(Y), int(Y1), int(Yb), int(Zn), int(Zr), int(Zr1), int(O), int(H)])
    if button == 'organic':
        elements = elements
        clicks = clicks
    elif button == 'ionic':
        temp1 = elements
        elements = ions
        ions = temp1
        temp2 = clicks
        clicks = ionclicks
        ionclicks = temp2  
    elif button == 'oxide':
        temp3 = elements
        elements = oxelements
        oxelements = temp3
        temp4 = clicks
        clicks = oxclicks
        oxclicks = temp4
    elif button == 'hydro':
        temp5 = elements
        elements = hydelements
        hydelements = temp5
        temp6 = clicks
        clicks = hydclicks
        hydclicks = temp6
    elimin9 = [clicks == 0]
    mask2 = ma.masked_array(elements, elimin9)
    mask2=mask2.tolist()
    abb= [i for i in mask2 if i is not None]
    elimin10 = [clicks == 0]
    mask4 = ma.masked_array(elimin10, clicks)
    mask5 = ma.masked_array(clicks, mask4)
    mask5=mask5.tolist()
    num= [i for i in mask5 if i is not None]
    zipped=zip(abb, num)
    ziplist=(list(zipped))
    ziplist=str(ziplist)
    ziplist=ziplist.replace(' 1), ', '')
    ziplist=ziplist.replace("(\'", "")
    ziplist=ziplist.replace(" 1)]", "")
    ziplist=ziplist.replace("\', ", "")
    ziplist=ziplist.replace("\',", "")
    ziplist=ziplist.replace(")]", "")
    ziplist=ziplist.replace("[", "")
    ziplist=ziplist.replace("), ", "")
    ziplist=ziplist.replace("]", "")
    ziplist=ziplist.replace("\'-\'", "-")
    if ziplist == 'HN4Cl':
        ziplist = 'NH4Cl'
    elif ziplist == 'AlO3H3':
        ziplist = 'Al(OH)3'
    elif ziplist == 'AlN3O6':
        ziplist = 'Al(NO2)3'
    elif ziplist == 'AlN3O9':
        ziplist = 'Al(NO3)3'
    elif ziplist == 'Al2C3O9':
        ziplist = 'Al2(CO3)3'
    elif ziplist == 'Al2S3O12':
        ziplist = 'Al2(SO4)3'
    elif ziplist == 'Al2Si2O9H4':
        ziplist = 'Al2Si2O5(OH)4'
    elif ziplist == 'AuO3H3':
        ziplist = 'Au(OH)3'
    elif ziplist == 'Au2Se3O12':
        ziplist = 'Au2(SeO4)3'
    elif ziplist == 'LiH':
        ziplist = 'DLi'
    elif ziplist == 'HBr':
        ziplist = 'DBr'
    elif ziplist == 'KBr':
        ziplist = 'KBR'
    ziplist1=[]
    ziplist1.append(ziplist)
    sum_clicks = np.sum(clicks).tolist()
    sum_clicks2=str(sum_clicks)
    total=[]
    if sum_clicks >= 1:
        total.append(sum_clicks2)
        total.append(abb)
        total.append(ziplist1)
        return json.dumps(total)
    elif sum_clicks==0:
        reset = ['']
        total.append(sum_clicks2)
        total.append(abb)
        total.append(ziplist1)
        return json.dumps(total)

@app.callback(
    Output(component_id='container', component_property='children'),
    [Input('inter-button', 'children')])
def label(interbutton):
    button = json.loads(interbutton)
    if button == 'organic':
        return html.Div([
                html.Div('Organic Compound'),
            ])
    elif button == 'ionic':
        return html.Div([
                html.Div('Ionic Compound'),
            ])
    elif button == 'oxide':
        return html.Div([
                html.Div('Oxide Compound'),
            ])
    else:
        return html.Div([
                html.Div('Hydroxide Compound'),
            ])


@app.callback(
    Output('textbox-1', 'value'),
    [Input('intermediate-value', 'children')])
def update(intermediatevalue):
    jg=json.loads(intermediatevalue)
    fg=jg[-1]
    return fg[0]
        

@app.callback(
    Output('textbox-2', 'value'),
    [Input('intermediate-value', 'children')])
def update(intermediatevalue):
    jg=json.loads(intermediatevalue)
    zsum = int(jg[0])
    fg=jg[-1]
    chem = fg[0]
    if zsum == 0:
        return 'No data'
    else:
        try:
            url = "https://ipfs.io/ipfs/QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco/wiki/Dictionary_of_chemical_formulas.html"
            html = urlopen(url)
            
            soup = BeautifulSoup(html, 'lxml')
            type(soup)
            
            c1 = soup.findChildren(attrs={'id': 'mwB1w'})[0] 
            c1 = pd.read_html(str(c1))
            c1= (c1[0].to_json(orient='split'))
            c1 = pd.read_json(c1, orient='split')
            
            c2 = soup.findChildren(attrs={'id': 'mwEtM'})[0] 
            c2 = pd.read_html(str(c2))
            c2= (c2[0].to_json(orient='split'))
            c2 = pd.read_json(c2, orient='split')
            
            cframes = [c1, c2]
            cframes = pd.concat(cframes, sort=True)
        
            chem1 = str(chem)
            chem1=chem1.replace("[", "")
            chem1=chem1.replace("]", "")
            chemlen = len(chem1)
    
        # Get the title
    
            if chem[0] == 'A':
                a = soup.findChildren(attrs={'id': 'mwKA'})[0] 
                a = pd.read_html(str(a))
                a= (a[0].to_json(orient='split'))
                df = pd.read_json(a, orient='split')
        
            elif chem[0] == 'B':
                b = soup.findChildren(attrs={'id': 'mwBBM'})[0] 
                b = pd.read_html(str(b))
                b= (b[0].to_json(orient='split'))
                df = pd.read_json(b, orient='split')
        
            elif chem[0] == 'C':
                df = cframes
        
            elif chem[0] == 'D':
                d = soup.findChildren(attrs={'id': 'mwGao'})[0] 
                d = pd.read_html(str(d))
                d= (d[0].to_json(orient='split'))
                df = pd.read_json(d, orient='split')
        
            elif chem[0] == 'E':
                e = soup.findChildren(attrs={'id': 'mwGfc'})[0] 
                e = pd.read_html(str(e))
                e= (e[0].to_json(orient='split'))
                df = pd.read_json(e, orient='split')
        
            elif chem[0] == 'F':
                f = soup.findChildren(attrs={'id': 'mwGoA'})[0] 
                f = pd.read_html(str(f))
                f= (f[0].to_json(orient='split'))
                df = pd.read_json(f, orient='split')
        
            elif chem[0] == 'G':
                g = soup.findChildren(attrs={'id': 'mwIJQ'})[0] 
                g = pd.read_html(str(g))
                g= (g[0].to_json(orient='split'))
                df = pd.read_json(g, orient='split')
        
            elif chem[0] == 'H':
                h = soup.findChildren(attrs={'id': 'mwISM'})[0] 
                h = pd.read_html(str(h))
                h= (h[0].to_json(orient='split'))
                df = pd.read_json(h, orient='split')
        
            elif chem[0] == 'I':
                i = soup.findChildren(attrs={'id': 'mwJBE'})[0] 
                i = pd.read_html(str(i))
                i= (i[0].to_json(orient='split'))
                df = pd.read_json(i, orient='split')
        
            elif chem[0] == 'K':
                k = soup.findChildren(attrs={'id': 'mwJOo'})[0] 
                k = pd.read_html(str(k))
                k= (k[0].to_json(orient='split'))
                df = pd.read_json(k, orient='split')
        
            elif chem[0] == 'L':
                k4 = soup.findChildren(attrs={'id': 'mwJdM'})[0]
                k4 = pd.read_html(str(k4))
                k4= (k4[0].to_json(orient='split'))
                df = pd.read_json(k4, orient='split')
        
            elif chem[0] == 'M':
                m = soup.findChildren(attrs={'id': 'mwJxk'})[0] 
                m = pd.read_html(str(m))
                m= (m[0].to_json(orient='split'))
                df = pd.read_json(m, orient='split')
        
            elif chem[0] == 'N':
                n = soup.findChildren(attrs={'id': 'mwKS8'})[0] 
                n = pd.read_html(str(n))
                n= (n[0].to_json(orient='split'))
                df = pd.read_json(n, orient='split')
        
            elif chem[0] == 'O':
                o = soup.findChildren(attrs={'id': 'mwLNU'})[0] 
                o = pd.read_html(str(o))
                o= (o[0].to_json(orient='split'))
                df = pd.read_json(o, orient='split')
        
            elif chem[0] == 'P':
                p = soup.findChildren(attrs={'id': 'mwLRk'})[0] 
                p = pd.read_html(str(p))
                p= (p[0].to_json(orient='split'))
                df = pd.read_json(p, orient='split')
        
            elif chem[0] == 'R':
                r = soup.findChildren(attrs={'id': 'mwLeA'})[0] 
                r = pd.read_html(str(r))
                r= (r[0].to_json(orient='split'))
                df = pd.read_json(r, orient='split')
        
            elif chem[0] == 'S':
                s = soup.findChildren(attrs={'id': 'mwLoU'})[0] 
                s = pd.read_html(str(s))
                s= (s[0].to_json(orient='split'))
                df = pd.read_json(s, orient='split')
        
            elif chem[0] == 'T':
                t = soup.findChildren(attrs={'id': 'mwMNw'})[0] 
                t = pd.read_html(str(t))
                t= (t[0].to_json(orient='split'))
                df = pd.read_json(t, orient='split')
        
            elif chem[0] == 'U':
                u = soup.findChildren(attrs={'id': 'mwMgg'})[0] 
                u = pd.read_html(str(u))
                u= (u[0].to_json(orient='split'))
                df = pd.read_json(u, orient='split')
        
            elif chem[0] == 'V':
                v = soup.findChildren(attrs={'id': 'mwMnA'})[0] 
                v = pd.read_html(str(v))
                v= (v[0].to_json(orient='split'))
                df = pd.read_json(v, orient='split')
        
            elif chem[0] == 'W':
                
                w = soup.findChildren(attrs={'id': 'mwMrI'})[0] 
                w = pd.read_html(str(w))
                w= (w[0].to_json(orient='split'))
                df = pd.read_json(w, orient='split')
        
            elif chem[0] == 'Y':
                y = soup.findChildren(attrs={'id': 'mwM34'})[0] 
                y = pd.read_html(str(y))
                y= (y[0].to_json(orient='split'))
                df = pd.read_json(y, orient='split')
        
            elif chem[0] == 'Z':
                z = soup.findChildren(attrs={'id': 'mwNCM'})[0] 
                z = pd.read_html(str(z))
                z= (z[0].to_json(orient='split'))
                df = pd.read_json(z, orient='split')
            df = pd.DataFrame(df)    
            df = df.loc[df[0] == chem]
            df.columns = ['Chemical Formula', 'Synonyms', 'CAS Number']
            df = str(df)
            if df[0:5] == 'Empty':
                return 'No data. Either our database is incomplete, the element you entered is physically impossible, or you have discovered a new chemical compound.'
            else:
                return df
        except KeyError:
            return 'No data.'


@app.callback(
    Output('interweb', 'children'),
    [Input('intermediate-value', 'children')])
def update(intermediatevalue):
    zsum1 = json.loads(intermediatevalue)
    zsum = int(zsum1[0])
    fg=zsum1[-1]
    chem = fg[0]
    if zsum != 0:
        try:
            chemlen = len(chem)
            #get hrefs
            url = "https://en.wikipedia.org/wiki/Dictionary_of_chemical_formulas?oldid=752654140"
            html = urlopen(url)
            soup = BeautifulSoup(html, 'lxml')
            type(soup)
            all_links = soup.find_all("a")
            list_links = []
            for link in all_links:
                cleaned = link.get("href")
                list_links.append(cleaned)
            a1 = list_links[:245]
            b1=list_links[246:273]
            c1=list_links[274:311]
            d1=list_links[312:441]
            e1=list_links[442:443]
            f1=list_links[444:448]
            g1=list_links[449:455]
            h1=list_links[456:463]
            i1=list_links[464:467]
            j1=list_links[470:489]
            k1=list_links[490:496]
            l1=list_links[498:501]
            m1=list_links[502:508]
            n1=list_links[515:533]
            o1=list_links[534:543]
            p1=list_links[544:555]
            q1=list_links[557:561]
            r1=list_links[565:568]
            s1=list_links[569:570]
            t1=list_links[572:573]
            u1=list_links[576:577]
            v1=list_links[578:580]
            w1=list_links[581:583]
            x1=list_links[585:590]
            y1=list_links[591:595]
            z1=list_links[596:597]
            a2=list_links[598:599]
            b2=list_links[600:615]
            c2=list_links[616:621]
            d2=list_links[622:623]
            e2=list_links[624:627]
            f2=list_links[628:641]
            g2=list_links[642:643]
            h2=list_links[647:650]
            i2=list_links[652:653]
            j2=list_links[654:655]
            k2=list_links[656:657]
            l2=list_links[660:663]
            m2=list_links[664:699]
            n2=list_links[700:718]
            o2=list_links[720:749]
            q2=list_links[752:982]
            r2=list_links[983:1012]
            s2=list_links[1013:1277]
            t2=list_links[1278:1287]
            u2=list_links[1289:1289]
            v2=list_links[1290:1299]
            w2=list_links[1301:1308]
            x2=list_links[1309:1350]
            y2=list_links[1351:1567]
            z2=list_links[1568:1585]
            a3=list_links[1586:1587]
            b3=list_links[1588:1625]
            c3=list_links[1626:2121]
            d3=list_links[2122:2128]
            
            list_links2= a1 + b1 + c1 + d1 + e1 + f1 + g1 + h1 + i1 + j1 + k1 + l1 + m1 + n1 + o1 + p1 + q1 + r1 + s1 + t1 + u1 + v1 + w1 + x1 + y1 + z1 + a2 + b2 + c2 + d2 + e2 + f2 + g2 + h2 + i2 + j2 + k2 + l2 + m2 + n2 + o2 + q2 + r2 + s2 + t2 + u2 + v2 + w2 + x2 + y2 + z2 + a3 + b3 + c3 + d3
            
            #Edit hrefs
            #/wiki/1-Aminocyclopropanecarboxylic_acid
            url3 = "https://ipfs.io/ipfs/QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco/wiki/Dictionary_of_chemical_formulas.html"
            html3 = urlopen(url3)
            
            soup = BeautifulSoup(html3, 'lxml')
            type(soup)
               
            #List location
            edit = [52, 212, 337, 675, 946, 952, 980, 1231, 1252, 1360, 1394, 1430, 1480, 1558, 1694, 1703, 1734, 1761, 1852, 1900, 1914, 1923, 1955, 1981]
        
            # Get the ref
            if chemlen > 0:
                if chem[0] == 'A':
                    a = soup.findChildren(attrs={'id': 'mwKA'})[0] 
                    a = pd.read_html(str(a))
                    a= (a[0].to_json(orient='split'))
                    df = pd.read_json(a, orient='split')
                    startpos = edit[0]
            
                elif chem[0] == 'B':
                    b = soup.findChildren(attrs={'id': 'mwBBM'})[0] 
                    b = pd.read_html(str(b))
                    b= (b[0].to_json(orient='split'))
                    df = pd.read_json(b, orient='split')
                    startpos = edit[1]
            
                elif chem[0] == 'C':
                    abb =zsum1[1]
                    if abb[0] == 'C':
                            c1 = soup.findChildren(attrs={'id': 'mwB1w'})[0] 
                            c1 = pd.read_html(str(c1))
                            c1= (c1[0].to_json(orient='split'))
                            df = pd.read_json(c1, orient='split')
                            startpos = edit[2]
                    else:
                            c2 = soup.findChildren(attrs={'id': 'mwEtM'})[0] 
                            c2 = pd.read_html(str(c2))
                            c2= (c2[0].to_json(orient='split'))
                            df = pd.read_json(c2, orient='split')
                            startpos = edit[3]
            
                elif chem[0] == 'D':
                    d = soup.findChildren(attrs={'id': 'mwGao'})[0] 
                    d = pd.read_html(str(d))
                    d= (d[0].to_json(orient='split'))
                    df = pd.read_json(d, orient='split')
                    startpos = edit[4]
            
                elif chem[0] == 'E':
                    e = soup.findChildren(attrs={'id': 'mwGfc'})[0] 
                    e = pd.read_html(str(e))
                    e= (e[0].to_json(orient='split'))
                    df = pd.read_json(e, orient='split')
                    startpos = edit[5]
            
                elif chem[0] == 'F':
                    f = soup.findChildren(attrs={'id': 'mwGoA'})[0] 
                    f = pd.read_html(str(f))
                    f= (f[0].to_json(orient='split'))
                    df = pd.read_json(f, orient='split')
                    startpos = edit[6]
            
                elif chem[0] == 'G':
                    g = soup.findChildren(attrs={'id': 'mwIJQ'})[0] 
                    g = pd.read_html(str(g))
                    g= (g[0].to_json(orient='split'))
                    df = pd.read_json(g, orient='split')
                    startpos = edit[7]
            
                elif chem[0] == 'H':
                    h = soup.findChildren(attrs={'id': 'mwISM'})[0] 
                    h = pd.read_html(str(h))
                    h= (h[0].to_json(orient='split'))
                    df = pd.read_json(h, orient='split')
                    startpos = edit[8]
            
                elif chem[0] == 'I':
                    i = soup.findChildren(attrs={'id': 'mwJBE'})[0] 
                    i = pd.read_html(str(i))
                    i= (i[0].to_json(orient='split'))
                    df = pd.read_json(i, orient='split')
                    startpos = edit[9]
            
                elif chem[0] == 'K':
                    k = soup.findChildren(attrs={'id': 'mwJOo'})[0] 
                    k = pd.read_html(str(k))
                    k= (k[0].to_json(orient='split'))
                    df = pd.read_json(k, orient='split')
                    startpos = edit[10]
            
                elif chem[0] == 'L':
                    k4 = soup.findChildren(attrs={'id': 'mwJdM'})[0]
                    k4 = pd.read_html(str(k4))
                    k4= (k4[0].to_json(orient='split'))
                    df = pd.read_json(k4, orient='split')
                    startpos = edit[11]
            
                elif chem[0] == 'M':
                    m = soup.findChildren(attrs={'id': 'mwJxk'})[0] 
                    m = pd.read_html(str(m))
                    m= (m[0].to_json(orient='split'))
                    df = pd.read_json(m, orient='split')
                    startpos = edit[12]
            
                elif chem[0] == 'N':
                    n = soup.findChildren(attrs={'id': 'mwKS8'})[0] 
                    n = pd.read_html(str(n))
                    n= (n[0].to_json(orient='split'))
                    df = pd.read_json(n, orient='split')
                    startpos = edit[13]
            
                elif chem[0] == 'O':
                    o = soup.findChildren(attrs={'id': 'mwLNU'})[0] 
                    o = pd.read_html(str(o))
                    o= (o[0].to_json(orient='split'))
                    df = pd.read_json(o, orient='split')
                    
                    startpos = edit[14]
            
                elif chem[0] == 'P':
                    p = soup.findChildren(attrs={'id': 'mwLRk'})[0] 
                    p = pd.read_html(str(p))
                    p= (p[0].to_json(orient='split'))
                    df = pd.read_json(p, orient='split')
                    
                    startpos = edit[15]
            
                elif chem[0] == 'R':
                    r = soup.findChildren(attrs={'id': 'mwLeA'})[0] 
                    r = pd.read_html(str(r))
                    r= (r[0].to_json(orient='split'))
                    df = pd.read_json(r, orient='split')
                    startpos = edit[16]
            
                elif chem[0] == 'S':
                    s = soup.findChildren(attrs={'id': 'mwLoU'})[0] 
                    s = pd.read_html(str(s))
                    s= (s[0].to_json(orient='split'))
                    df = pd.read_json(s, orient='split')
                    startpos = edit[17]
            
                elif chem[0] == 'T':
                    t = soup.findChildren(attrs={'id': 'mwMNw'})[0] 
                    t = pd.read_html(str(t))
                    t= (t[0].to_json(orient='split'))
                    df = pd.read_json(t, orient='split')
                    startpos = edit[18]
            
                elif chem[0] == 'U':
                    u = soup.findChildren(attrs={'id': 'mwMgg'})[0] 
                    u = pd.read_html(str(u))
                    u= (u[0].to_json(orient='split'))
                    df = pd.read_json(u, orient='split')
                    startpos = edit[19]
            
                elif chem[0] == 'V':
                    v = soup.findChildren(attrs={'id': 'mwMnA'})[0] 
                    v = pd.read_html(str(v))
                    v= (v[0].to_json(orient='split'))
                    df = pd.read_json(v, orient='split')
                    startpos = edit[20]
            
                elif chem[0] == 'W':
                    
                    w = soup.findChildren(attrs={'id': 'mwMrI'})[0] 
                    w = pd.read_html(str(w))
                    w= (w[0].to_json(orient='split'))
                    df = pd.read_json(w, orient='split')
                    startpos = edit[21]
            
                elif chem[0] == 'Y':
                    y = soup.findChildren(attrs={'id': 'mwM34'})[0] 
                    y = pd.read_html(str(y))
                    y= (y[0].to_json(orient='split'))
                    df = pd.read_json(y, orient='split')
                    
                    startpos = edit[22]
            
                elif chem[0] == 'Z':
                    z = soup.findChildren(attrs={'id': 'mwNCM'})[0] 
                    z = pd.read_html(str(z))
                    z= (z[0].to_json(orient='split'))
                    df = pd.read_json(z, orient='split')
                    startpos = edit[23]
                try:        
                    dft=df.loc[df[0] == chem].index[0]
                    a = dft + startpos
                    b = a + 1
                    link = list_links2[a:b]
                    link = str(link)
                    link = link.replace("\'", '')
                    link = link.replace('[', '')
                    link = link.replace(']', '')
                    url2 = 'https://en.wikipedia.org{}'.format(link)
                    print(url2)
                    html2 = urlopen(url2)
                    soup = BeautifulSoup(html2, 'lxml')
                    type(soup)
                    body = soup.find('body')
                    body = body.findChildren()
                    body = str(body)
                    return json.dumps(body)
                except IndexError:
                    return json.dumps(defaults)  
        except KeyError:
            return json.dumps(defaults)

@app.callback(
    Output('container2', 'children'),
    [Input('interweb', 'children')])
def update(interweb):
    try:
        body = json.loads(interweb)
        body = body.replace('[', '')
        body = body.replace(']', '')
        return  html.Iframe(
            sandbox='',
            style={'width': '80%', 'border-color': 'rgb(59, 57, 57)', 'background-color':'white', 'height':520,  'font-family': 'inherit',},
            srcDoc=(body),
        className="ten columns offset-by-one")
    except:
        return  html.Iframe(
            sandbox='',
            style={'width': '80%', 'border-color': 'rgb(59, 57, 57)', 'background-color':'white', 'height':520,  'font-family': 'inherit',},
            srcDoc=(defaults),
        className="ten columns offset-by-one")


if __name__ == '__main__':
    app.run_server(debug=True)
