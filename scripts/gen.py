#!/usr/bin/env python3
"""Parse scraped TM markdown files → jsonspieler.json"""
import json, re, os, glob

BASE = "/Users/Jo/.gemini/antigravity/brain/46bb6e20-5167-4759-ac9c-a95a84653b97/.system_generated/steps"

CLUBS = {
    "FC Bayern München": 27, "Borussia Dortmund": 16, "RB Leipzig": 23826,
    "Bayer 04 Leverkusen": 15, "Eintracht Frankfurt": 24, "VfB Stuttgart": 79,
    "TSG 1899 Hoffenheim": 533, "VfL Wolfsburg": 82, "SC Freiburg": 60,
    "SV Werder Bremen": 86, "Hamburger SV": 41, "FC Augsburg": 167,
    "Borussia Mönchengladbach": 18, "1. FSV Mainz 05": 39, "1. FC Köln": 3,
    "1. FC Union Berlin": 89, "FC St. Pauli": 35, "1. FC Heidenheim 1846": 2036,
}

LM = {27:"1498251238",16:"1396275280",23826:"1619431624",15:"1651221781",
      24:"1603277045",79:"1618158538",533:"1462358637",82:"1467356331",
      60:"1517249279",86:"1596112862",41:"1702627785",167:"1656073509",
      18:"1656585791",39:"1564476037",3:"1656585763",89:"1656585817",
      35:"1698741498",2036:"1700207555"}

# Title patterns to identify club files
TITLE_MAP = {
    "FC Bayern": "FC Bayern München",
    "Borussia Dortmund": "Borussia Dortmund",
    "RB Leipzig": "RB Leipzig",
    "Bayer 04 Leverkusen": "Bayer 04 Leverkusen",
    "Eintracht Frankfurt": "Eintracht Frankfurt",
    "VfB Stuttgart": "VfB Stuttgart",
    "TSG 1899 Hoffenheim": "TSG 1899 Hoffenheim",
    "VfL Wolfsburg": "VfL Wolfsburg",
    "SC Freiburg": "SC Freiburg",
    "SV Werder Bremen": "SV Werder Bremen",
    "Hamburger SV": "Hamburger SV",
    "FC Augsburg": "FC Augsburg",
    "Mönchengladbach": "Borussia Mönchengladbach",
    "Mainz 05": "1. FSV Mainz 05",
    "1.FC Köln": "1. FC Köln",
    "Union Berlin": "1. FC Union Berlin",
    "FC St. Pauli": "FC St. Pauli",
    "Heidenheim": "1. FC Heidenheim 1846",
}

EXCLUDE_NAMES = {
    'News','Transfers & Gerüchte','Marktwerte','Wettbewerbe','Statistiken',
    'Community','Gaming','Berater-Support','Berater-Firmen','PremiumService',
    'Video ▶️','Neueste Transfers','Gerüchteküche','Alle Foren','Alle News',
    'Marktwert-Analyse','Vereinsforen Bundesliga','Vereinsforen 2. Bundesliga',
    'Vereinsforen 3. Liga','Sportwetten','Kompakt','Erweitert','Galerie',
    '#','Spieler','Alter','Vertrag','Marktwert','Wertvollste Spieler der Welt',
    'Aktuelle Gerüchte','Aktuelle Marktwert-Updates','FIFA-Weltrangliste',
    'Wettanbieter Deutschland','Paten und Datenpfleger',
    'Als Pate oder Datenpfleger bewerben','11 Gebote','Fehler gefunden?',
    'Offene Stellen','Kontakt','Das TM-Team','FAQ','Wahretabelle',
    'Soccerdonna.de','Scoutastic.com','Impressum','Datenschutz',
    'Privatsphäre','Widerruf Tracking','Nutzungsbedingungen','Media',
    'Bundesliga','1.Liga',
}

def wappen(tid):
    return f"https://tmssl.akamaized.net/images/wappen/head/{tid}.png?lm={LM.get(tid,'1')}"

def img(pid):
    return f"https://img.a.transfermarkt.technology/portrait/medium/{pid}-1700000000.jpg?lm=1"

def parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Identify club from title
    club_name = None
    for key, name in TITLE_MAP.items():
        if key in content[:200]:
            club_name = name
            break
    if not club_name:
        return []
    
    tid = CLUBS[club_name]
    
    # Extract profile links: [Name](url/profil/spieler/ID)
    profil = re.compile(r'\[([^\]]+)\]\(https://www\.transfermarkt\.de/[^/]+/profil/spieler/(\d+)\)')
    mv_re = re.compile(r'\[([^\]]+)\]\(https://www\.transfermarkt\.de/[^/]+/marktwertverlauf/spieler/(\d+)\)')
    
    mv_map = {}
    for m in mv_re.finditer(content):
        mv_map[m.group(2)] = m.group(1).strip()
    
    players = []
    seen = set()
    for m in profil.finditer(content):
        name, pid = m.group(1).strip(), m.group(2)
        if pid in seen or name in EXCLUDE_NAMES or len(name) < 2:
            continue
        # Skip youth/reserve team links
        if any(k in name for k in ['U19','U17','U18','Jugend','UEFA','(- 20','Fußballschule','Breitenfußball',' II ',' III',' IV',' V ',' VI',' VII',' VIII']):
            continue
        # Skip if name ends with II, III etc
        if re.search(r'\s+(II|III|IV|V|VI|VII|VIII)\s*(\(|$)', name):
            continue
        seen.add(pid)
        players.append({
            "Name": name,
            "Bild": img(pid),
            "Marktwert": mv_map.get(pid, ""),
            "Wappen": wappen(tid),
            "Verein": club_name,
        })
    return players

def main():
    all_players = []
    # Find all content.md files in steps directories
    for step_dir in sorted(glob.glob(os.path.join(BASE, "*/"))):
        filepath = os.path.join(step_dir, "content.md")
        if not os.path.exists(filepath):
            continue
        # Only process Kader pages
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        if 'Kader im Detail' not in first_line:
            continue
        
        players = parse_file(filepath)
        if players:
            print(f"{players[0]['Verein']}: {len(players)} Spieler")
            all_players.extend(players)
    
    print(f"\nGesamt: {len(all_players)} Spieler aus {len(set(p['Verein'] for p in all_players))} Vereinen")
    
    out = "/Users/Jo/Spieler/src/data/players.json"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(all_players, f, ensure_ascii=False, indent=2)
    print(f"Saved → {out}")

if __name__ == "__main__":
    main()
