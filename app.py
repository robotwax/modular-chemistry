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
import pandas as pd
import html5lib
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pandas import DataFrame

external_stylesheets = ['/assets/code.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions'] = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


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

periodics={'A': 'mwKA', 'B': 'mwBBM', 'C': ('mwB1w', 'mwEtM'), 'D': 'mwGao', 'E': 'mwGfc', 'F': 'mwGoA', 'G': 'mwIJQ', 'H': 'mwISM', 'I': 'mwJBE', 'K': 'mwJOo', 'L': 'mwJdM', 'M': 'mwJxk', 'N': 'mwKS8', 'O': 'mwLNU', 'P': 'mwLRk', 'R': 'mwLeA', 'S': 'mwLoU', 'T': 'mwMNw', 'U': 'mwMgg', 'V': 'mwMnA', 'W': 'mwMrI', 'Y': 'mwM34', 'Z': 'mwNCM'}

edit={'A': 52, 'B': 212, 'C': [337,  675], 'D': 946, 'E': 952, 'F': 980, 'G': 1231, 'H': 1252, 'I': 1360, 'K': 1394, 'L': 1430, 'M': 1480, 'N': 1558, 'O': 1694, 'P': 1703, 'R': 1734, 'S': 1761, 'T': 1852, 'U': 1900, 'V': 1914, 'W': 1923, 'X': 1955, 'Y': 1981}

app.layout = html.Div([
    html.Div([
        html.Div(children=[
        html.H1(['Modular ', html.Span('Chemisty', style={'color':'#fda947'})], style={'font-size':100, 'margin-top':30}),
        ], className='seven columns'),
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
        className='seven columns offset-by-one'),
        html.Button('Search', id='search', n_clicks='0', style={'width':'11.9%', 'color': 'white', 'margin-top':12, 'background-color':'lightblue'},
        className="two columns"),
    ], className="row"),
    html.Br(),
    html.Div([
        dcc.Textarea(id='textbox-2', readOnly = 'False', style={'width': '40%', 'border-radius': 1, 'resize':'none'},
        className='three columns offset-by-one'),
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
            dcc.Markdown('''[Cataphysical Research Society - 2019](https://cataphysical-research-society.herokuapp.com)''')),
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
    elements = {'C': int(C), 'H': int(H), 'Ac': int(Ac), 'Ag': int(Ag), 'Al': int(Al), 'Am': int(Am), 'Ar': int(Ar), 'As': int(As), 'At': int(At), 'Au': int(Au), 'B': int(B), 'Ba': int(Ba), 'Be': int(Be), 'Bh': int(Bh), 'Bi': int(Bi), 'Bk': int(Bk), 'Br': int(Br), 'Ca': int(Ca), 'Ca': int(Ca1), 'Cd': int(Cd), 'Ce': int(Ce), 'Cf': int(Cf), 'Cl': int(Cl), 'Cm': int(Cm), 'Cn': int(Cn), 'Co': int(Co), 'Cr': int(Cr), 'Cr': int(Cr1), 'Cs': int(Cs), 'Cu': int(Cu), 'Db': int(Db), 'Ds': int(Ds), 'Dy': int(Dy), 'Er': int(Er), 'Es': int(Es), 'Eu': int(Eu), 'F': int(F), 'Fe': int(Fe), 'Fl': int(Fl), 'Fm': int(Fm), 'Fr': int(Fr), 'Ga': int(Ga), 'Gd': int(Gd), 'Ge': int(Ge), 'He': int(He), 'Hf': int(Hf), 'Hg': int(Hg), 'Ho': int(Ho), 'Hs': int(Hs), 'I': int(I), 'In': int(In), 'Ir': int(Ir), 'K': int(K), 'K': int(K1), 'Kr': int(Kr), 'La': int(La), 'Li': int(Li), 'Lr': int(Lr), 'Lu': int(Lu), 'Lv': int(Lv), 'Md': int(Md), 'Mg': int(Mg), 'Mn': int(Mn), 'Mo': int(Mo), 'Mo': int(Mo1), 'Mt': int(Mt), 'N': int(N), 'Na': int(Na), 'Nb': int(Nb), 'Nb': int(Nb1), 'Nd': int(Nd), 'Ne': int(Ne), 'Ni': int(Ni), 'No': int(No), 'Np': int(Np), 'O': int(O), 'Os': int(Os), 'P': int(P), 'Pa': int(Pa), 'Pb': int(Pb), 'Pd': int(Pd), 'Pm': int(Pm), 'Po': int(Po), 'Pr': int(Pr), 'Pt': int(Pt), 'Pu': int(Pu), 'Ra': int(Ra), 'Rb': int(Rb), 'Rb': int(Rb1), 'Re': int(Re), 'Rf': int(Rf), 'Rg': int(Rg), 'Rh': int(Rh), 'Rn': int(Rn), 'Ru': int(Ru), 'S': int(S), 'Sb': int(Sb), 'Sc': int(Sc), 'Sc': int(Sc1), 'Se': int(Se), 'Sg': int(Sg), 'Si': int(Si), 'Sm': int(Sm), 'Sn': int(Sn), 'Sr': int(Sr), 'Sr': int(Sr1), 'Ta': int(Ta), 'Tb': int(Tb), 'Tc': int(Tc), 'Te': int(Te), 'Th': int(Th), 'Ti': int(Ti), 'Ti': int(Ti1), 'Tl': int(Tl), 'Tm': int(Tm), 'U': int(U), 'Uuo': int(Uuo), 'Uup': int(Uup), 'Uus': int(Uus), 'Uut': int(Uut), 'V': int(V), 'V': int(V1), 'W': int(W), 'Xe': int(Xe), 'Y': int(Y), 'Y': int(Y1), 'Yb': int(Yb), 'Zn': int(Zn), 'Zr': int(Zr), 'Zr': int(Zr1)}
    
    ions = {'Cs': int(Cs),'Fr': int(Fr),'K': int(K),'K': int(K1),'Rb': int(Rb),'Rb': int(Rb1),'Ba': int(Ba),'Ra': int(Ra),'Na': int(Na),'Sr': int(Sr),'Sr': int(Sr1),'Li': int(Li),'Ca': int(Ca),'Ca': int(Ca1),'Yb': int(Yb),'La': int(La),'Ac': int(Ac),'Ce': int(Ce),'Pr': int(Pr),'Pm': int(Pm),'Nd': int(Nd),'Sm': int(Sm),'Tb': int(Tb),'Gd': int(Gd),'Eu': int(Eu),'Dy': int(Dy),'Y': int(Y),'Y': int(Y1),'Ho': int(Ho),'Er': int(Er),'Tm': int(Tm),'Lu': int(Lu),'Pu': int(Pu),'No': int(No),'Es': int(Es),'Th': int(Th),'Hf': int(Hf),'Md': int(Md),'Bk': int(Bk),'Am': int(Am),'Lr': int(Lr),'Cf': int(Cf),'Cm': int(Cm),'Fm': int(Fm),'Mg': int(Mg),'Zr': int(Zr),'Zr': int(Zr1),'Np': int(Np),'Sc': int(Sc),'Sc': int(Sc1),'U': int(U),'Ta': int(Ta),'Pa': int(Pa),'Ti': int(Ti),'Ti': int(Ti1),'Mn': int(Mn),'Be': int(Be),'Nb': int(Nb),'Nb': int(Nb1),'Al': int(Al),'V': int(V),'V': int(V1),'Zn': int(Zn),'Cr': int(Cr),'Cr': int(Cr1),'Cd': int(Cd),'In': int(In),'Ga': int(Ga),'Fe': int(Fe),'Co': int(Co),'Si': int(Si),'Re': int(Re),'Tc': int(Tc),'Cu': int(Cu),'Ni': int(Ni),'Ag': int(Ag),'Sn': int(Sn),'Po': int(Po),'Hg': int(Hg),'Ge': int(Ge),'Bi': int(Bi),'Tl': int(Tl),'B': int(B),'Sb': int(Sb),'Te': int(Te),'Mo': int(Mo),'Mo': int(Mo1),'As': int(As),'P': int(P),'H': int(H),'Ir': int(Ir),'Ru': int(Ru),'Os': int(Os),'At': int(At),'Rn': int(Rn),'Pd': int(Pd),'Pt': int(Pt),'Rh': int(Rh),'Pb': int(Pb),'W': int(W),'Au': int(Au),'C': int(C),'Se': int(Se),'S': int(S),'Xe': int(Xe),'I': int(I),'Br': int(Br),'Kr': int(Kr),'N': int(N),'Cl': int(Cl),'O': int(O),'F': int(F),'He': int(He),'Ne': int(Ne),'Ar': int(Ar),'Rf': int(Rf),'Db': int(Db),'Sg': int(Sg),'Bh': int(Bh),'Hs': int(Hs),'Mt': int(Mt),'Ds': int(Ds),'Rg': int(Rg),'Cn': int(Cn),'Uut': int(Uut),'Fl': int(Fl),'Uup': int(Uup),'Lv': int(Lv),'Uus': int(Uus),'Uuo': int(Uuo)}
    
    oxelements = {'Ac': int(Ac), 'Ag': int(Ag), 'Al': int(Al), 'Am': int(Am), 'Ar': int(Ar), 'As': int(As), 'At': int(At), 'Au': int(Au), 'B': int(B), 'Ba': int(Ba), 'Be': int(Be), 'Bh': int(Bh), 'Bi': int(Bi), 'Bk': int(Bk), 'Br': int(Br), 'C': int(C), 'Ca': int(Ca), 'Ca': int(Ca1), 'Cd': int(Cd), 'Ce': int(Ce), 'Cf': int(Cf), 'Cl': int(Cl), 'Cm': int(Cm), 'Cn': int(Cn), 'Co': int(Co), 'Cr': int(Cr), 'Cr': int(Cr1), 'Cs': int(Cs), 'Cu': int(Cu), 'Db': int(Db), 'Ds': int(Ds), 'Dy': int(Dy), 'Er': int(Er), 'Es': int(Es), 'Eu': int(Eu), 'F': int(F), 'Fe': int(Fe), 'Fl': int(Fl), 'Fm': int(Fm), 'Fr': int(Fr), 'Ga': int(Ga), 'Gd': int(Gd), 'Ge': int(Ge), 'H': int(H), 'He': int(He), 'Hf': int(Hf), 'Hg': int(Hg), 'Ho': int(Ho), 'Hs': int(Hs), 'I': int(I), 'In': int(In), 'Ir': int(Ir), 'K': int(K), 'K': int(K1), 'Kr': int(Kr), 'La': int(La), 'Li': int(Li), 'Lr': int(Lr), 'Lu': int(Lu), 'Lv': int(Lv), 'Md': int(Md), 'Mg': int(Mg), 'Mn': int(Mn), 'Mo': int(Mo), 'Mo': int(Mo1), 'Mt': int(Mt), 'N': int(N), 'Na': int(Na), 'Nb': int(Nb), 'Nb': int(Nb1), 'Nd': int(Nd), 'Ne': int(Ne), 'Ni': int(Ni), 'No': int(No), 'Np': int(Np), 'Os': int(Os), 'P': int(P), 'Pa': int(Pa), 'Pb': int(Pb), 'Pd': int(Pd), 'Pm': int(Pm), 'Po': int(Po), 'Pr': int(Pr), 'Pt': int(Pt), 'Pu': int(Pu), 'Ra': int(Ra), 'Rb': int(Rb), 'Rb': int(Rb1), 'Re': int(Re), 'Rf': int(Rf), 'Rg': int(Rg), 'Rh': int(Rh), 'Rn': int(Rn), 'Ru': int(Ru), 'S': int(S), 'Sb': int(Sb), 'Sc': int(Sc), 'Sc': int(Sc1), 'Se': int(Se), 'Sg': int(Sg), 'Si': int(Si), 'Sm': int(Sm), 'Sn': int(Sn), 'Sr': int(Sr), 'Sr': int(Sr1), 'Ta': int(Ta), 'Tb': int(Tb), 'Tc': int(Tc), 'Te': int(Te), 'Th': int(Th), 'Ti': int(Ti), 'Ti': int(Ti1), 'Tl': int(Tl), 'Tm': int(Tm), 'U': int(U), 'Uuo': int(Uuo), 'Uup': int(Uup), 'Uus': int(Uus), 'Uut': int(Uut), 'V': int(V), 'V': int(V1), 'W': int(W), 'Xe': int(Xe), 'Y': int(Y), 'Y': int(Y1), 'Yb': int(Yb), 'Zn': int(Zn), 'Zr': int(Zr), 'Zr': int(Zr1), 'O': int(O)}
    
    hydelements = {'Ac': int(Ac), 'Ag': int(Ag), 'Al': int(Al), 'Am': int(Am), 'Ar': int(Ar), 'As': int(As), 'At': int(At), 'Au': int(Au), 'B': int(B), 'Ba': int(Ba), 'Be': int(Be), 'Bh': int(Bh), 'Bi': int(Bi), 'Bk': int(Bk), 'Br': int(Br), 'C': int(C), 'Ca': int(Ca), 'Ca': int(Ca1), 'Cd': int(Cd), 'Ce': int(Ce), 'Cf': int(Cf), 'Cl': int(Cl), 'Cm': int(Cm), 'Cn': int(Cn), 'Co': int(Co), 'Cr': int(Cr), 'Cr': int(Cr1), 'Cs': int(Cs), 'Cu': int(Cu), 'Db': int(Db), 'Ds': int(Ds), 'Dy': int(Dy), 'Er': int(Er), 'Es': int(Es), 'Eu': int(Eu), 'F': int(F), 'Fe': int(Fe), 'Fl': int(Fl), 'Fm': int(Fm), 'Fr': int(Fr), 'Ga': int(Ga), 'Gd': int(Gd), 'Ge': int(Ge), 'He': int(He), 'Hf': int(Hf), 'Hg': int(Hg), 'Ho': int(Ho), 'Hs': int(Hs), 'I': int(I), 'In': int(In), 'Ir': int(Ir), 'K': int(K), 'K1': int(K1), 'Kr': int(Kr), 'La': int(La), 'Li': int(Li), 'Lr': int(Lr), 'Lu': int(Lu), 'Lv': int(Lv), 'Md': int(Md), 'Mg': int(Mg), 'Mn': int(Mn), 'Mo': int(Mo), 'Mo': int(Mo1), 'Mt': int(Mt), 'N': int(N), 'Na': int(Na), 'Nb': int(Nb), 'Nb': int(Nb1), 'Nd': int(Nd), 'Ne': int(Ne), 'Ni': int(Ni), 'No': int(No), 'Np': int(Np), 'Os': int(Os), 'P': int(P), 'Pa': int(Pa), 'Pb': int(Pb), 'Pd': int(Pd), 'Pm': int(Pm), 'Po': int(Po), 'Pr': int(Pr), 'Pt': int(Pt), 'Pu': int(Pu), 'Ra': int(Ra), 'Rb': int(Rb), 'Rb': int(Rb1), 'Re': int(Re), 'Rf': int(Rf), 'Rg': int(Rg), 'Rh': int(Rh), 'Rn': int(Rn), 'Ru': int(Ru), 'S': int(S), 'Sb': int(Sb), 'Sc': int(Sc), 'Sc': int(Sc1), 'Se': int(Se), 'Sg': int(Sg), 'Si': int(Si), 'Sm': int(Sm), 'Sn': int(Sn), 'Sr': int(Sr), 'Sr': int(Sr1), 'Ta': int(Ta), 'Tb': int(Tb), 'Tc': int(Tc), 'Te': int(Te), 'Th': int(Th), 'Ti': int(Ti), 'Ti': int(Ti1), 'Tl': int(Tl), 'Tm': int(Tm), 'U': int(U), 'Uuo': int(Uuo), 'Uup': int(Uup), 'Uus': int(Uus), 'Uut': int(Uut), 'V': int(V), 'V': int(V1), 'W': int(W), 'Xe': int(Xe), 'Y': int(Y), 'Y': int(Y1), 'Yb': int(Yb), 'Zn': int(Zn), 'Zr': int(Zr), 'Zr': int(Zr1), 'O': int(O), 'H': int(H)}
    if button == 'organic':
        elements = elements
    elif button == 'ionic':
        temp1 = elements
        elements = ions
        ions = temp1
    elif button == 'oxide':
        temp3 = elements
        elements = oxelements
        oxelements = temp3
    elif button == 'hydro':
        temp5 = elements
        elements = hydelements
        hydelements = temp5


    vip = dict((k, v) for k, v in elements.items() if v >= 1)
    ziplist=str(vip)
    ziplist=ziplist.replace(": 1, \'", "")
    ziplist=ziplist.replace("{/''", "")
    ziplist=ziplist.replace(" 1}", "")
    ziplist=ziplist.replace(", \'", "")
    ziplist=ziplist.replace("\'", "")
    ziplist=ziplist.replace("}", "")
    ziplist=ziplist.replace("{", "")
    ziplist=ziplist.replace(":", "")
    ziplist=ziplist.replace(" ", "")
    if ziplist !='':
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
        return json.dumps(ziplist)
    else:
        reset = ['']
        return json.dumps(reset)

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
    return jg
        

@app.callback(
    Output('textbox-2', 'value'),
    [Input('intermediate-value', 'children'),
     Input('search', 'n_clicks')])
def update(intermediatevalue, nclicks):
    if int(nclicks) > 0:
        chem=json.loads(intermediatevalue)
        if chem[0] == '':
            return 'No data'
        else:
            try:
                url = "https://ipfs.io/ipfs/QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco/wiki/Dictionary_of_chemical_formulas.html"
                html = urlopen(url)
                
                soup = BeautifulSoup(html, 'lxml')
                type(soup)
                
                chem1 = str(chem)
                chem1=chem1.replace("[", "")
                chem1=chem1.replace("]", "")
                chemlen = len(chem1)
        
            # Get the title
        
                if chem[0] == 'C':
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
                    df = cframes
            
                else:
                    d = soup.findChildren(attrs={'id': periodics[chem[0]]})[0] 
                    d = pd.read_html(str(d))
                    d= (d[0].to_json(orient='split'))
                    df = pd.read_json(d, orient='split')

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
    else:
        return 'No data.'


@app.callback(
    Output('interweb', 'children'),
    [Input('intermediate-value', 'children'),
     Input('search', 'n_clicks')])
def update(intermediatevalue, nclicks):
    if int(nclicks) > 0:
        chem = json.loads(intermediatevalue)
        if chem[0] != '':
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
            
                # Get the ref
                if chemlen > 0:
                    vibe=periodics[chem[0]]
                    vide=edit[chem[0]]
                    if chem[0] == 'C':
                        abb =chem[1]
                        ty = ['a', 'd', 'e', 'F', 'l', 'o', 'r', 's', 'u']
                        try:
                            ind=ty.index(abb)
                            if ind == 4:
                                abb2=chem[2]
                                if abb2 == 'C':
                                    d = soup.findChildren(attrs={'id': vibe[0]})[0] 
                                    startpos = vide[0]
                                else:
                                    d = soup.findChildren(attrs={'id': vibe[1]})[0] 
                                    startpos = vide[1]
                            else:
                                d = soup.findChildren(attrs={'id': vibe[1]})[0] 
                                startpos = vide[1]
                        except:
                                d = soup.findChildren(attrs={'id': vibe[0]})[0] 
                                startpos = vide[0]
                        d = pd.read_html(str(d))
                        d= (d[0].to_json(orient='split'))
                        df = pd.read_json(d, orient='split')
                
                    else:
                        d = soup.findChildren(attrs={'id': vibe})[0] 
                        d = pd.read_html(str(d))
                        d= (d[0].to_json(orient='split'))
                        df = pd.read_json(d, orient='split')
                        startpos = vide
 
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
    else:
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
