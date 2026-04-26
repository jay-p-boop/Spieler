#!/usr/bin/env python3
"""Generate players.json — Part 1: Bayern, BVB, RBL, B04, SGE, VfB"""
import json, os

def w(tid): return f"https://tmssl.akamaized.net/images/wappen/head/{tid}.png"
def i(pid): return f"https://img.a.transfermarkt.technology/portrait/medium/{pid}-1700000000.jpg?lm=1"
def p(n,pid,mv,v,vid): return {"Name":n,"Bild":i(pid),"Marktwert":mv,"Wappen":w(vid),"Verein":v}

V="FC Bayern München";T=27
d1=[
p("Jonas Urbig",607720,"15,00 Mio. €",V,T),p("Manuel Neuer",17259,"4,00 Mio. €",V,T),
p("Sven Ulreich",40680,"500 Tsd. €",V,T),p("Dayot Upamecano",344695,"70,00 Mio. €",V,T),
p("Jonathan Tah",196357,"30,00 Mio. €",V,T),p("Min-jae Kim",503482,"25,00 Mio. €",V,T),
p("Hiroki Ito",353892,"18,00 Mio. €",V,T),p("Alphonso Davies",424204,"45,00 Mio. €",V,T),
p("Josip Stanisic",483046,"35,00 Mio. €",V,T),p("Konrad Laimer",223967,"32,00 Mio. €",V,T),
p("Aleksandar Pavlovic",792380,"75,00 Mio. €",V,T),p("Joshua Kimmich",161056,"40,00 Mio. €",V,T),
p("Tom Bischof",822959,"40,00 Mio. €",V,T),p("Leon Goretzka",153084,"15,00 Mio. €",V,T),
p("Jamal Musiala",580195,"120,00 Mio. €",V,T),p("Lennart Karl",1075147,"60,00 Mio. €",V,T),
p("Raphaël Guerreiro",170986,"6,00 Mio. €",V,T),p("Luis Díaz",480692,"70,00 Mio. €",V,T),
p("Michael Olise",566723,"140,00 Mio. €",V,T),p("Serge Gnabry",159471,"20,00 Mio. €",V,T),
p("Harry Kane",132098,"65,00 Mio. €",V,T),p("Nicolas Jackson",776890,"40,00 Mio. €",V,T),
]

V="Borussia Dortmund";T=16
d2=[
p("Gregor Kobel",257814,"40,00 Mio. €",V,T),p("Alexander Meyer",76158,"800 Tsd. €",V,T),
p("Nico Schlotterbeck",388198,"55,00 Mio. €",V,T),p("Waldemar Anton",193004,"18,00 Mio. €",V,T),
p("Ramy Bensebaini",284732,"7,00 Mio. €",V,T),p("Emre Can",119296,"4,00 Mio. €",V,T),
p("Niklas Süle",166601,"4,00 Mio. €",V,T),p("Daniel Svensson",579287,"22,00 Mio. €",V,T),
p("Julian Ryerson",370789,"25,00 Mio. €",V,T),p("Felix Nmecha",406640,"50,00 Mio. €",V,T),
p("Jobe Bellingham",796297,"30,00 Mio. €",V,T),p("Carney Chukwuemeka",659459,"20,00 Mio. €",V,T),
p("Marcel Sabitzer",106987,"7,00 Mio. €",V,T),p("Yan Couto",627228,"20,00 Mio. €",V,T),
p("Julian Brandt",187492,"20,00 Mio. €",V,T),p("Karim Adeyemi",496094,"50,00 Mio. €",V,T),
p("Serhou Guirassy",270541,"40,00 Mio. €",V,T),p("Maximilian Beier",578392,"40,00 Mio. €",V,T),
p("Fábio Silva",505653,"28,00 Mio. €",V,T),
]

V="RB Leipzig";T=23826
d3=[
p("Maarten Vandevoordt",486046,"8,00 Mio. €",V,T),p("Péter Gulácsi",57071,"2,00 Mio. €",V,T),
p("Leopold Zingerle",160971,"400 Tsd. €",V,T),p("Castello Lukeba",618472,"45,00 Mio. €",V,T),
p("El Chadaille Bitshiabu",787912,"15,00 Mio. €",V,T),p("Willi Orbán",93740,"6,00 Mio. €",V,T),
p("Lukas Klostermann",215599,"3,50 Mio. €",V,T),p("David Raum",318204,"22,00 Mio. €",V,T),
p("Max Finkgräfe",810649,"3,00 Mio. €",V,T),p("Ridle Baku",327251,"12,00 Mio. €",V,T),
p("Benjamin Henrichs",202591,"9,00 Mio. €",V,T),p("Kosta Nedeljkovic",848682,"6,00 Mio. €",V,T),
p("Nicolas Seiwald",404950,"22,00 Mio. €",V,T),p("Assan Ouédraogo",897424,"28,00 Mio. €",V,T),
p("Ezechiel Banzuzi",865682,"18,00 Mio. €",V,T),p("Xaver Schlager",223979,"10,00 Mio. €",V,T),
p("Christoph Baumgartner",324278,"30,00 Mio. €",V,T),p("Brajan Gruda",700106,"28,00 Mio. €",V,T),
p("Andrija Maksimovic",952779,"12,00 Mio. €",V,T),p("Yan Diomande",1390649,"75,00 Mio. €",V,T),
p("Antonio Nusa",894914,"32,00 Mio. €",V,T),p("Johan Bakayoko",565424,"22,00 Mio. €",V,T),
p("Rômulo",957874,"30,00 Mio. €",V,T),p("Conrad Harder",807386,"20,00 Mio. €",V,T),
]

V="Bayer 04 Leverkusen";T=15
d4=[
p("Mark Flekken",125714,"8,00 Mio. €",V,T),p("Jonas Omlin",247915,"1,50 Mio. €",V,T),
p("Jarell Quansah",632349,"45,00 Mio. €",V,T),p("Edmond Tapsoba",564545,"35,00 Mio. €",V,T),
p("Loïc Badé",730581,"25,00 Mio. €",V,T),p("Axel Tape",1077670,"8,00 Mio. €",V,T),
p("Alejandro Grimaldo",193082,"24,00 Mio. €",V,T),p("Arthur",977464,"7,00 Mio. €",V,T),
p("Lucas Vázquez",221316,"2,50 Mio. €",V,T),p("Equi Fernández",664708,"22,00 Mio. €",V,T),
p("Robert Andrich",159088,"7,00 Mio. €",V,T),p("Exequiel Palacios",401578,"30,00 Mio. €",V,T),
p("Aleix García",261504,"20,00 Mio. €",V,T),p("Ibrahim Maza",905011,"40,00 Mio. €",V,T),
p("Malik Tillman",467437,"30,00 Mio. €",V,T),p("Jonas Hofmann",7161,"2,00 Mio. €",V,T),
p("Eliesse Ben Seghir",810895,"20,00 Mio. €",V,T),p("Martin Terrier",442891,"12,00 Mio. €",V,T),
p("Ernest Poku",718303,"25,00 Mio. €",V,T),p("Nathan Tella",340322,"15,00 Mio. €",V,T),
p("Christian Kofane",1364454,"40,00 Mio. €",V,T),p("Patrik Schick",242086,"20,00 Mio. €",V,T),
]

V="Eintracht Frankfurt";T=24
d5=[
p("Kauã Santos",997861,"7,00 Mio. €",V,T),p("Michael Zetterer",196813,"4,50 Mio. €",V,T),
p("Jens Grahl",40034,"200 Tsd. €",V,T),p("Arthur Theate",368891,"20,00 Mio. €",V,T),
p("Nnamdi Collins",684315,"20,00 Mio. €",V,T),p("Robin Koch",328784,"15,00 Mio. €",V,T),
p("Aurèle Amenda",635645,"8,00 Mio. €",V,T),p("Nathaniel Brown",691892,"35,00 Mio. €",V,T),
p("Rasmus Kristensen",369684,"12,00 Mio. €",V,T),p("Ellyes Skhiri",290587,"6,00 Mio. €",V,T),
p("Hugo Larsson",931838,"32,00 Mio. €",V,T),p("Oscar Højlund",846310,"10,00 Mio. €",V,T),
p("Can Uzun",816585,"45,00 Mio. €",V,T),p("Farès Chaïbi",855015,"15,00 Mio. €",V,T),
p("Mario Götze",74842,"3,50 Mio. €",V,T),p("Jean-Mattéo Bahoya",939964,"25,00 Mio. €",V,T),
p("Ritsu Doan",358504,"20,00 Mio. €",V,T),p("Ansgar Knauff",429874,"15,00 Mio. €",V,T),
p("Jonathan Burkardt",333647,"35,00 Mio. €",V,T),p("Arnaud Kalimuendo",585959,"25,00 Mio. €",V,T),
]

V="VfB Stuttgart";T=79
d6=[
p("Alexander Nübel",195778,"12,00 Mio. €",V,T),p("Fabian Bredlow",187624,"800 Tsd. €",V,T),
p("Finn Jeltsch",924117,"30,00 Mio. €",V,T),p("Ramon Hendriks",436064,"20,00 Mio. €",V,T),
p("Jeff Chabot",303219,"15,00 Mio. €",V,T),p("Luca Jaquez",539798,"10,00 Mio. €",V,T),
p("Maximilian Mittelstädt",282660,"18,00 Mio. €",V,T),p("Josha Vagnoman",448258,"10,00 Mio. €",V,T),
p("Angelo Stiller",443710,"45,00 Mio. €",V,T),p("Chema Andrés",948279,"15,00 Mio. €",V,T),
p("Atakan Karazor",232320,"9,00 Mio. €",V,T),p("Nikolas Nartey",400546,"7,00 Mio. €",V,T),
p("Bilal El Khannouss",654982,"32,00 Mio. €",V,T),p("Chris Führich",272278,"10,00 Mio. €",V,T),
p("Jamie Leweling",518505,"40,00 Mio. €",V,T),p("Badredine Bouanani",707242,"12,00 Mio. €",V,T),
p("Ermedin Demirovic",335457,"22,00 Mio. €",V,T),p("Deniz Undav",339314,"22,00 Mio. €",V,T),
p("Tiago Tomás",616344,"15,00 Mio. €",V,T),
]

all_p = d1+d2+d3+d4+d5+d6
out = "/Users/Jo/Spieler/src/data/players_part1.json"
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out,'w',encoding='utf-8') as f: json.dump(all_p,f,ensure_ascii=False,indent=2)
print(f"Part 1: {len(all_p)} players saved")
