#!/usr/bin/env python3
"""Part 2: TSG, WOB, SCF, SVW, HSV, FCA"""
import json, os

def w(tid): return f"https://tmssl.akamaized.net/images/wappen/head/{tid}.png"
def i(pid): return f"https://img.a.transfermarkt.technology/portrait/medium/{pid}-1700000000.jpg?lm=1"
def p(n,pid,mv,v,vid): return {"Name":n,"Bild":i(pid),"Marktwert":mv,"Wappen":w(vid),"Verein":v}

V="TSG 1899 Hoffenheim";T=533
d7=[
p("Oliver Baumann",55089,"3,00 Mio. €",V,T),p("Luca Philipp",432671,"750 Tsd. €",V,T),
p("Albian Hajdari",579459,"20,00 Mio. €",V,T),p("Robin Hranac",620217,"10,00 Mio. €",V,T),
p("Ozan Kabak",361260,"10,00 Mio. €",V,T),p("Koki Machida",415035,"7,00 Mio. €",V,T),
p("Kevin Akpoguma",160241,"2,00 Mio. €",V,T),p("Bernardo",364258,"5,00 Mio. €",V,T),
p("Valentin Gendrey",569387,"7,00 Mio. €",V,T),p("Leon Avdullahu",667457,"25,00 Mio. €",V,T),
p("Wouter Burger",412953,"20,00 Mio. €",V,T),p("Grischa Prömel",234029,"3,50 Mio. €",V,T),
p("Alexander Prass",434116,"7,00 Mio. €",V,T),p("Muhammed Damar",789898,"5,00 Mio. €",V,T),
p("Andrej Kramaric",46580,"3,00 Mio. €",V,T),p("Bazoumana Touré",1067904,"35,00 Mio. €",V,T),
p("Fisnik Asllani",524290,"30,00 Mio. €",V,T),p("Tim Lemperle",553285,"15,00 Mio. €",V,T),
p("Adam Hlozek",552057,"12,00 Mio. €",V,T),p("Max Moerstedt",923595,"7,00 Mio. €",V,T),
p("Ihlas Bebou",237164,"800 Tsd. €",V,T),
]

V="VfL Wolfsburg";T=82
d8=[
p("Kamil Grabara",346551,"12,00 Mio. €",V,T),p("Marius Müller",118161,"1,00 Mio. €",V,T),
p("Konstantinos Koulierakis",669380,"25,00 Mio. €",V,T),p("Jeanuël Belocian",919515,"12,00 Mio. €",V,T),
p("Jonas Adjetey",734676,"7,00 Mio. €",V,T),p("Denis Vavro",239962,"5,00 Mio. €",V,T),
p("Jenson Seelt",617755,"5,00 Mio. €",V,T),p("Moritz Jenz",460245,"5,00 Mio. €",V,T),
p("Joakim Maehle",369674,"7,00 Mio. €",V,T),p("Aaron Zehnter",730484,"6,00 Mio. €",V,T),
p("Saël Kumbedi",951579,"12,00 Mio. €",V,T),p("Kilian Fischer",435796,"5,00 Mio. €",V,T),
p("Vini Souza",663581,"8,00 Mio. €",V,T),p("Mattias Svanberg",342405,"9,00 Mio. €",V,T),
p("Maximilian Arnold",117674,"4,50 Mio. €",V,T),p("Lovro Majer",387106,"10,00 Mio. €",V,T),
p("Bence Dárdai",789252,"7,00 Mio. €",V,T),p("Christian Eriksen",69633,"3,00 Mio. €",V,T),
p("Patrick Wimmer",533295,"15,00 Mio. €",V,T),p("Adam Daghim",881297,"7,50 Mio. €",V,T),
p("Mohamed Amoura",746910,"27,00 Mio. €",V,T),p("Dzenan Pejcinovic",819636,"10,00 Mio. €",V,T),
p("Jonas Wind",391004,"5,00 Mio. €",V,T),
]

V="SC Freiburg";T=60
d9=[
p("Noah Atubolu",526845,"20,00 Mio. €",V,T),p("Florian Müller",284769,"1,20 Mio. €",V,T),
p("Philipp Lienhart",225657,"12,00 Mio. €",V,T),p("Bruno Ogbus",863759,"10,00 Mio. €",V,T),
p("Matthias Ginter",124502,"6,00 Mio. €",V,T),p("Max Rosenfelder",599419,"6,00 Mio. €",V,T),
p("Jordy Makengo",815078,"6,00 Mio. €",V,T),p("Christian Günter",93707,"2,00 Mio. €",V,T),
p("Philipp Treu",335993,"10,00 Mio. €",V,T),p("Patrick Osterhage",443331,"12,00 Mio. €",V,T),
p("Johan Manzambi",927353,"35,00 Mio. €",V,T),p("Maximilian Eggestein",190284,"10,00 Mio. €",V,T),
p("Derry Scherhant",820957,"6,00 Mio. €",V,T),p("Vincenzo Grifo",185077,"5,00 Mio. €",V,T),
p("Cyriaque Irié",1145064,"8,00 Mio. €",V,T),p("Niklas Beste",342967,"7,00 Mio. €",V,T),
p("Yuito Suzuki",668606,"18,00 Mio. €",V,T),p("Igor Matanovic",605268,"10,00 Mio. €",V,T),
p("Lucas Höler",248999,"3,00 Mio. €",V,T),
]

V="SV Werder Bremen";T=86
d10=[
p("Mio Backhaus",620295,"12,00 Mio. €",V,T),p("Karl Hein",493513,"3,00 Mio. €",V,T),
p("Karim Coulibaly",1084638,"22,00 Mio. €",V,T),p("Marco Friedl",156990,"12,00 Mio. €",V,T),
p("Amos Pieper",334221,"4,00 Mio. €",V,T),p("Niklas Stark",162434,"3,50 Mio. €",V,T),
p("Felix Agu",393512,"6,00 Mio. €",V,T),p("Yukinari Sugawara",405385,"7,50 Mio. €",V,T),
p("Mitchell Weiser",119211,"3,50 Mio. €",V,T),p("Senne Lynen",338668,"10,00 Mio. €",V,T),
p("Jens Stage",289835,"14,00 Mio. €",V,T),p("Romano Schmid",346853,"15,00 Mio. €",V,T),
p("Cameron Puertas",449592,"8,00 Mio. €",V,T),p("Samuel Mbangula",654991,"10,00 Mio. €",V,T),
p("Marco Grüll",391766,"6,00 Mio. €",V,T),p("Justin Njinmah",596153,"7,00 Mio. €",V,T),
p("Jovan Milosevic",943795,"7,00 Mio. €",V,T),p("Victor Boniface",656681,"5,00 Mio. €",V,T),
p("Keke Topp",701757,"3,50 Mio. €",V,T),
]

V="Hamburger SV";T=41
d11=[
p("Sander Tangvik",549378,"3,00 Mio. €",V,T),p("Daniel Heuer Fernandes",84993,"1,20 Mio. €",V,T),
p("Luka Vuskovic",892160,"60,00 Mio. €",V,T),p("Jordan Torunarigha",227110,"4,00 Mio. €",V,T),
p("Daniel Elfadli",529895,"3,50 Mio. €",V,T),p("Warmed Omari",711996,"3,50 Mio. €",V,T),
p("Miro Muheim",298603,"5,00 Mio. €",V,T),p("William Mikelbrencis",743500,"3,00 Mio. €",V,T),
p("Nicolai Remberg",592534,"7,00 Mio. €",V,T),p("Albert Sambi Lokonga",381967,"10,00 Mio. €",V,T),
p("Nicolás Capaldo",649672,"5,00 Mio. €",V,T),p("Fábio Vieira",537598,"18,00 Mio. €",V,T),
p("Albert Grønbaek",503866,"5,00 Mio. €",V,T),p("Philip Otele",678655,"5,00 Mio. €",V,T),
p("Jean-Luc Dompé",291222,"3,50 Mio. €",V,T),p("Damion Downs",820241,"6,00 Mio. €",V,T),
p("Ransford Königsdörffer",470038,"4,00 Mio. €",V,T),p("Robert Glatzel",196139,"1,50 Mio. €",V,T),
p("Yussuf Poulsen",157635,"1,50 Mio. €",V,T),
]

V="FC Augsburg";T=167
d12=[
p("Finn Dahmen",251299,"12,00 Mio. €",V,T),p("Nediljko Labrovic",610190,"2,00 Mio. €",V,T),
p("Chrislain Matsima",569383,"22,00 Mio. €",V,T),p("Noahkai Banks",923945,"22,00 Mio. €",V,T),
p("Keven Schlotterbeck",413843,"6,00 Mio. €",V,T),p("Cédric Zesiger",382478,"5,00 Mio. €",V,T),
p("Jeffrey Gouweleeuw",106405,"1,00 Mio. €",V,T),p("Dimitrios Giannoulis",295630,"3,00 Mio. €",V,T),
p("Marius Wolf",193900,"2,50 Mio. €",V,T),p("Kristijan Jakic",374954,"6,00 Mio. €",V,T),
p("Robin Fellhauer",264960,"3,00 Mio. €",V,T),p("Han-Noah Massengo",536508,"6,00 Mio. €",V,T),
p("Elvis Rexhbecaj",280575,"3,50 Mio. €",V,T),p("Anton Kade",654234,"7,50 Mio. €",V,T),
p("Alexis Claude-Maurice",384593,"15,00 Mio. €",V,T),p("Mert Kömür",777005,"12,00 Mio. €",V,T),
p("Fabian Rieder",507341,"8,00 Mio. €",V,T),p("Rodrigo Ribeiro",726701,"4,00 Mio. €",V,T),
p("Michael Gregoritsch",120205,"1,50 Mio. €",V,T),
]

all_p = d7+d8+d9+d10+d11+d12
out = "/Users/Jo/Spieler/src/data/players_part2.json"
with open(out,'w',encoding='utf-8') as f: json.dump(all_p,f,ensure_ascii=False,indent=2)
print(f"Part 2: {len(all_p)} players saved")
