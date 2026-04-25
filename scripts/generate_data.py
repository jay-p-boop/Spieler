#!/usr/bin/env python3
"""
Generate jsonspieler.json with Bundesliga 2025/26 squad data.
Data sourced from Transfermarkt Kader pages (April 2026).
"""
import json

def img(pid):
    """Construct Transfermarkt portrait URL from player ID."""
    return f"https://img.a.transfermarkt.technology/portrait/medium/{pid}-1700000000.jpg?lm=1"

def wappen(tid):
    """Construct Transfermarkt club badge URL from team ID."""
    lm_map = {
        27: "1498251238", 16: "1396275280", 23826: "1619431624",
        15: "1651221781", 24: "1603277045", 79: "1618158538",
        533: "1462358637", 82: "1467356331", 60: "1517249279",
        86: "1596112862", 41: "1702627785", 167: "1656073509",
        18: "1656585791", 39: "1564476037", 3: "1656585763",
        89: "1656585817", 35: "1698741498", 2036: "1700207555",
    }
    return f"https://tmssl.akamaized.net/images/wappen/head/{tid}.png?lm={lm_map.get(tid, '1')}"

def p(name, pid, mv, verein, verein_id):
    """Create a player entry."""
    return {
        "Name": name,
        "Bild": img(pid),
        "Marktwert": mv,
        "Wappen": wappen(verein_id),
        "Verein": verein,
    }

# ============================================================================
# FC BAYERN MÜNCHEN (ID: 27)
# ============================================================================
V = "FC Bayern München"
VID = 27
bayern = [
    p("Jonas Urbig", 607720, "15,00 Mio. €", V, VID),
    p("Manuel Neuer", 17259, "4,00 Mio. €", V, VID),
    p("Sven Ulreich", 40680, "500 Tsd. €", V, VID),
    p("Dayot Upamecano", 344695, "70,00 Mio. €", V, VID),
    p("Jonathan Tah", 196357, "30,00 Mio. €", V, VID),
    p("Min-jae Kim", 503482, "25,00 Mio. €", V, VID),
    p("Hiroki Ito", 353892, "18,00 Mio. €", V, VID),
    p("Alphonso Davies", 424204, "45,00 Mio. €", V, VID),
    p("Josip Stanisic", 483046, "35,00 Mio. €", V, VID),
    p("Konrad Laimer", 223967, "32,00 Mio. €", V, VID),
    p("Aleksandar Pavlovic", 792380, "75,00 Mio. €", V, VID),
    p("Joshua Kimmich", 161056, "40,00 Mio. €", V, VID),
    p("Tom Bischof", 822959, "40,00 Mio. €", V, VID),
    p("Leon Goretzka", 153084, "15,00 Mio. €", V, VID),
    p("Jamal Musiala", 580195, "120,00 Mio. €", V, VID),
    p("Lennart Karl", 1075147, "60,00 Mio. €", V, VID),
    p("Raphaël Guerreiro", 170986, "6,00 Mio. €", V, VID),
    p("Luis Díaz", 480692, "70,00 Mio. €", V, VID),
    p("Michael Olise", 566723, "140,00 Mio. €", V, VID),
    p("Serge Gnabry", 159471, "20,00 Mio. €", V, VID),
    p("Harry Kane", 132098, "65,00 Mio. €", V, VID),
    p("Nicolas Jackson", 776890, "40,00 Mio. €", V, VID),
]

# ============================================================================
# BORUSSIA DORTMUND (ID: 16)
# ============================================================================
V = "Borussia Dortmund"
VID = 16
dortmund = [
    p("Gregor Kobel", 257814, "40,00 Mio. €", V, VID),
    p("Alexander Meyer", 76158, "800 Tsd. €", V, VID),
    p("Nico Schlotterbeck", 388198, "55,00 Mio. €", V, VID),
    p("Waldemar Anton", 193004, "18,00 Mio. €", V, VID),
    p("Ramy Bensebaini", 284732, "7,00 Mio. €", V, VID),
    p("Emre Can", 119296, "4,00 Mio. €", V, VID),
    p("Niklas Süle", 166601, "4,00 Mio. €", V, VID),
    p("Daniel Svensson", 579287, "22,00 Mio. €", V, VID),
    p("Julian Ryerson", 370789, "25,00 Mio. €", V, VID),
    p("Felix Nmecha", 406640, "50,00 Mio. €", V, VID),
    p("Jobe Bellingham", 796297, "30,00 Mio. €", V, VID),
    p("Carney Chukwuemeka", 659459, "20,00 Mio. €", V, VID),
    p("Marcel Sabitzer", 106987, "7,00 Mio. €", V, VID),
    p("Yan Couto", 627228, "20,00 Mio. €", V, VID),
    p("Julian Brandt", 187492, "20,00 Mio. €", V, VID),
    p("Karim Adeyemi", 496094, "50,00 Mio. €", V, VID),
    p("Serhou Guirassy", 270541, "40,00 Mio. €", V, VID),
    p("Maximilian Beier", 578392, "40,00 Mio. €", V, VID),
    p("Fábio Silva", 505653, "28,00 Mio. €", V, VID),
]

# ============================================================================
# RB LEIPZIG (ID: 23826)
# ============================================================================
V = "RB Leipzig"
VID = 23826
# Need to read this data
leipzig = []

# ============================================================================
# BAYER 04 LEVERKUSEN (ID: 15)
# ============================================================================
V = "Bayer 04 Leverkusen"
VID = 15
leverkusen = []

# ============================================================================
# EINTRACHT FRANKFURT (ID: 24)
# ============================================================================
V = "Eintracht Frankfurt"
VID = 24
frankfurt = []

# ============================================================================
# VFB STUTTGART (ID: 79)
# ============================================================================
V = "VfB Stuttgart"
VID = 79
stuttgart = []

# Placeholder - these will be filled from the remaining club pages
# For now, let's output what we have
print("This script needs the remaining club data to be added manually.")
print("Use the read_all_clubs.py script instead.")

all_players = bayern + dortmund
print(f"Players so far: {len(all_players)}")

# Save partial output
with open("/Users/Jo/Spieler/src/jsonspieler.json", 'w', encoding='utf-8') as f:
    json.dump(all_players, f, ensure_ascii=False, indent=2)

print("Partial data saved.")
