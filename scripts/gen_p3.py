#!/usr/bin/env python3
"""Part 3: BMG, M05, KOE, FCU, STP, HDH — then merge all"""
import json, os

def w(tid): return f"https://tmssl.akamaized.net/images/wappen/head/{tid}.png"
def i(pid): return f"https://img.a.transfermarkt.technology/portrait/medium/{pid}-1700000000.jpg?lm=1"
def p(n,pid,mv,v,vid): return {"Name":n,"Bild":i(pid),"Marktwert":mv,"Wappen":w(vid),"Verein":v}

V="Borussia Mönchengladbach";T=18
d13=[
p("Moritz Nicolas",284270,"6,00 Mio. €",V,T),p("Jan Olschowsky",455922,"450 Tsd. €",V,T),
p("Tobias Sippel",31653,"300 Tsd. €",V,T),p("Nico Elvedi",192635,"8,00 Mio. €",V,T),
p("Kevin Diks",335209,"5,00 Mio. €",V,T),p("Kota Takai",671108,"5,00 Mio. €",V,T),
p("Fabio Chiarodia",724104,"3,00 Mio. €",V,T),p("Marvin Friedrich",196231,"1,80 Mio. €",V,T),
p("Lukas Ullrich",787151,"7,00 Mio. €",V,T),p("Joe Scally",504153,"7,00 Mio. €",V,T),
p("Yannik Engelhardt",405670,"6,00 Mio. €",V,T),p("Philipp Sander",388409,"4,00 Mio. €",V,T),
p("Rocco Reitz",467434,"20,00 Mio. €",V,T),p("Jens Castrop",613192,"6,00 Mio. €",V,T),
p("Florian Neuhaus",278332,"3,50 Mio. €",V,T),p("Wael Mohya",1070979,"10,00 Mio. €",V,T),
p("Giovanni Reyna",504215,"4,00 Mio. €",V,T),p("Kevin Stöger",106872,"2,00 Mio. €",V,T),
p("Robin Hack",284010,"9,00 Mio. €",V,T),p("Hugo Bolin",667251,"6,00 Mio. €",V,T),
p("Franck Honorat",229006,"10,00 Mio. €",V,T),p("Nathan Ngoumou",629588,"3,50 Mio. €",V,T),
p("Tim Kleindienst",193033,"10,00 Mio. €",V,T),p("Shuto Machino",550580,"5,00 Mio. €",V,T),
p("Haris Tabakovic",203123,"3,00 Mio. €",V,T),p("Alejo Sarco",1000675,"2,00 Mio. €",V,T),
]

V="1. FSV Mainz 05";T=39
d14=[
p("Robin Zentner",160963,"3,00 Mio. €",V,T),p("Daniel Batz",90317,"350 Tsd. €",V,T),
p("Kacper Potulski",1073748,"12,00 Mio. €",V,T),p("Stefan Posch",223974,"5,50 Mio. €",V,T),
p("Andreas Hanche-Olsen",370683,"4,00 Mio. €",V,T),p("Dominik Kohr",118847,"2,00 Mio. €",V,T),
p("Danny da Costa",85906,"1,20 Mio. €",V,T),p("Maxim Leitsch",334207,"1,00 Mio. €",V,T),
p("Stefan Bell",82350,"600 Tsd. €",V,T),p("Phillipp Mwene",127573,"1,50 Mio. €",V,T),
p("Anthony Caci",453016,"8,00 Mio. €",V,T),p("Silvan Widmer",168989,"800 Tsd. €",V,T),
p("Kaishu Sano",643574,"25,00 Mio. €",V,T),p("Lennard Maloney",392710,"2,50 Mio. €",V,T),
p("Nadiem Amiri",232454,"17,00 Mio. €",V,T),p("Paul Nebel",503160,"15,00 Mio. €",V,T),
p("Jae-sung Lee",314398,"2,00 Mio. €",V,T),p("Silas",612826,"3,00 Mio. €",V,T),
p("Armindo Sieb",569033,"3,00 Mio. €",V,T),p("Nelson Weiper",796213,"10,00 Mio. €",V,T),
p("Benedict Hollerbach",453870,"8,00 Mio. €",V,T),p("Phillip Tietz",288340,"3,50 Mio. €",V,T),
]

V="1. FC Köln";T=3
d15=[
p("Marvin Schwäbe",160929,"3,00 Mio. €",V,T),p("Ron-Robert Zieler",21327,"500 Tsd. €",V,T),
p("Rav van den Berg",640556,"8,00 Mio. €",V,T),p("Jahmai Simpson-Pusey",942497,"6,00 Mio. €",V,T),
p("Joël Schmied",322517,"3,50 Mio. €",V,T),p("Cenk Özkacar",615350,"3,00 Mio. €",V,T),
p("Timo Hübers",236981,"2,50 Mio. €",V,T),p("Kristoffer Lund",623773,"4,00 Mio. €",V,T),
p("Sebastian Sebulonsen",592387,"5,50 Mio. €",V,T),p("Eric Martel",597000,"8,00 Mio. €",V,T),
p("Tom Krauß",405687,"4,50 Mio. €",V,T),p("Ísak Jóhannesson",579565,"8,00 Mio. €",V,T),
p("Denis Huseinbasic",678479,"3,00 Mio. €",V,T),p("Alessio Castro-Montes",340166,"3,00 Mio. €",V,T),
p("Said El Mala",1168219,"35,00 Mio. €",V,T),p("Jakub Kamiński",407098,"12,00 Mio. €",V,T),
p("Linton Maina",335103,"3,00 Mio. €",V,T),p("Jan Thielmann",472249,"5,00 Mio. €",V,T),
p("Ragnar Ache",416380,"8,00 Mio. €",V,T),p("Luca Waldschmidt",196095,"2,00 Mio. €",V,T),
]

V="1. FC Union Berlin";T=89
d16=[
p("Frederik Rönnow",107775,"2,50 Mio. €",V,T),p("Matheo Raab",386685,"600 Tsd. €",V,T),
p("Leopold Querfeld",597432,"18,00 Mio. €",V,T),p("Danilho Doekhi",387047,"13,00 Mio. €",V,T),
p("Diogo Leite",357156,"12,00 Mio. €",V,T),p("Tom Rothe",798043,"10,00 Mio. €",V,T),
p("Derrick Köhn",391780,"4,00 Mio. €",V,T),p("Josip Juranovic",362977,"2,50 Mio. €",V,T),
p("Christopher Trimmel",75921,"600 Tsd. €",V,T),p("Aljoscha Kemlein",692737,"12,00 Mio. €",V,T),
p("Rani Khedira",124410,"2,00 Mio. €",V,T),p("András Schäfer",454863,"4,50 Mio. €",V,T),
p("Alex Král",337333,"2,50 Mio. €",V,T),p("Robert Skov",270393,"2,50 Mio. €",V,T),
p("Woo-yeong Jeong",297583,"3,50 Mio. €",V,T),p("Livan Burcu",519872,"4,00 Mio. €",V,T),
p("Ilyas Ansah",1035765,"12,00 Mio. €",V,T),p("Andrej Ilic",583699,"6,00 Mio. €",V,T),
p("Oliver Burke",341317,"4,00 Mio. €",V,T),
]

V="FC St. Pauli";T=35
d17=[
p("Nikola Vasilj",248454,"4,50 Mio. €",V,T),p("Ben Voll",453742,"500 Tsd. €",V,T),
p("Eric Smith",292534,"5,00 Mio. €",V,T),p("David Nemeth",451906,"3,00 Mio. €",V,T),
p("Tomoya Ando",610795,"3,00 Mio. €",V,T),p("Hauke Wahl",154147,"1,50 Mio. €",V,T),
p("Karol Mets",139304,"800 Tsd. €",V,T),p("Louis Oppie",605265,"2,50 Mio. €",V,T),
p("Lars Ritzka",333903,"1,00 Mio. €",V,T),p("Arkadiusz Pyrka",599733,"3,50 Mio. €",V,T),
p("Manolis Saliakas",242661,"2,50 Mio. €",V,T),p("James Sands",393321,"5,00 Mio. €",V,T),
p("Joel Chima Fujita",697277,"10,00 Mio. €",V,T),p("Mathias Rasmussen",268327,"2,50 Mio. €",V,T),
p("Connor Metcalfe",522223,"2,00 Mio. €",V,T),p("Jackson Irvine",192557,"1,50 Mio. €",V,T),
p("Danel Sinani",346499,"3,00 Mio. €",V,T),p("Mathias Pereira Lage",424072,"3,50 Mio. €",V,T),
p("Andréas Hountondji",704155,"5,00 Mio. €",V,T),p("Martijn Kaars",377729,"3,00 Mio. €",V,T),
p("Taichi Hara",495752,"1,50 Mio. €",V,T),
]

V="1. FC Heidenheim 1846";T=2036
d18=[
p("Diant Ramaj",448705,"7,00 Mio. €",V,T),p("Frank Feller",806948,"500 Tsd. €",V,T),
p("Tim Siersleben",337092,"2,50 Mio. €",V,T),p("Patrick Mainka",133731,"2,50 Mio. €",V,T),
p("Benedikt Gimber",227084,"2,00 Mio. €",V,T),p("Hennes Behrens",829838,"2,00 Mio. €",V,T),
p("Jonas Föhrenbach",192169,"1,20 Mio. €",V,T),p("Leart Paçarada",107219,"1,00 Mio. €",V,T),
p("Leonidas Stergiou",507345,"3,00 Mio. €",V,T),p("Omar Traoré",388294,"2,50 Mio. €",V,T),
p("Marnon Busch",117478,"1,20 Mio. €",V,T),p("Niklas Dorsch",251302,"3,00 Mio. €",V,T),
p("Jan Schöppner",581357,"3,50 Mio. €",V,T),p("Luca Kerber",809498,"2,00 Mio. €",V,T),
p("Arijon Ibrahimovic",744728,"6,00 Mio. €",V,T),p("Adrian Beck",273669,"2,00 Mio. €",V,T),
p("Mathias Honsak",283497,"2,00 Mio. €",V,T),p("Eren Dinkçi",645774,"6,00 Mio. €",V,T),
p("Marvin Pieringer",471055,"4,00 Mio. €",V,T),p("Budu Zivzivadze",187097,"1,20 Mio. €",V,T),
]

# Merge all parts
all_p = d13+d14+d15+d16+d17+d18
base = "/Users/Jo/Spieler/src/data"
with open(f"{base}/players_part3.json",'w',encoding='utf-8') as f:
    json.dump(all_p,f,ensure_ascii=False,indent=2)

# Now merge all 3 parts
p1 = json.load(open(f"{base}/players_part1.json",'r',encoding='utf-8'))
p2 = json.load(open(f"{base}/players_part2.json",'r',encoding='utf-8'))
final = p1 + p2 + all_p
with open(f"{base}/players.json",'w',encoding='utf-8') as f:
    json.dump(final,f,ensure_ascii=False,indent=2)

clubs = set(x["Verein"] for x in final)
print(f"Part 3: {len(all_p)} players")
print(f"FINAL: {len(final)} players from {len(clubs)} clubs")
for c in sorted(clubs):
    cnt = sum(1 for x in final if x["Verein"]==c)
    print(f"  {c}: {cnt}")
