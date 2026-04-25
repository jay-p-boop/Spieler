#!/usr/bin/env python3
"""
Parse scraped Transfermarkt markdown files and generate jsonspieler.json
for the Poki Bundesliga 2025/26 app.
"""
import json
import re
import os

BASE = "/Users/Jo/.gemini/antigravity/brain/46bb6e20-5167-4759-ac9c-a95a84653b97/.system_generated/steps"

# Map step directories to club data
CLUBS = [
    {"step": "51", "name": "FC Bayern München", "id": 27, "wappen": "https://tmssl.akamaized.net/images/wappen/head/27.png?lm=1498251238"},
    {"step": "63", "name": "Borussia Dortmund", "id": 16, "wappen": "https://tmssl.akamaized.net/images/wappen/head/16.png?lm=1396275280"},
    {"step": "64", "name": "RB Leipzig", "id": 23826, "wappen": "https://tmssl.akamaized.net/images/wappen/head/23826.png?lm=1619431624"},
    {"step": "65", "name": "Bayer 04 Leverkusen", "id": 15, "wappen": "https://tmssl.akamaized.net/images/wappen/head/15.png?lm=1651221781"},
    {"step": "66", "name": "Eintracht Frankfurt", "id": 24, "wappen": "https://tmssl.akamaized.net/images/wappen/head/24.png?lm=1603277045"},
    {"step": "67", "name": "VfB Stuttgart", "id": 79, "wappen": "https://tmssl.akamaized.net/images/wappen/head/79.png?lm=1618158538"},
    {"step": "70", "name": "TSG 1899 Hoffenheim", "id": 533, "wappen": "https://tmssl.akamaized.net/images/wappen/head/533.png?lm=1462358637"},
    {"step": "71", "name": "VfL Wolfsburg", "id": 82, "wappen": "https://tmssl.akamaized.net/images/wappen/head/82.png?lm=1467356331"},
    {"step": "72", "name": "SC Freiburg", "id": 60, "wappen": "https://tmssl.akamaized.net/images/wappen/head/60.png?lm=1517249279"},
    {"step": "73", "name": "SV Werder Bremen", "id": 86, "wappen": "https://tmssl.akamaized.net/images/wappen/head/86.png?lm=1596112862"},
    {"step": "74", "name": "Hamburger SV", "id": 41, "wappen": "https://tmssl.akamaized.net/images/wappen/head/41.png?lm=1702627785"},
    {"step": "75", "name": "FC Augsburg", "id": 167, "wappen": "https://tmssl.akamaized.net/images/wappen/head/167.png?lm=1656073509"},
    {"step": "78", "name": "Borussia Mönchengladbach", "id": 18, "wappen": "https://tmssl.akamaized.net/images/wappen/head/18.png?lm=1656585791"},
    {"step": "79", "name": "1. FSV Mainz 05", "id": 39, "wappen": "https://tmssl.akamaized.net/images/wappen/head/39.png?lm=1564476037"},
    {"step": "80", "name": "1. FC Köln", "id": 3, "wappen": "https://tmssl.akamaized.net/images/wappen/head/3.png?lm=1656585763"},
    {"step": "81", "name": "1. FC Union Berlin", "id": 89, "wappen": "https://tmssl.akamaized.net/images/wappen/head/89.png?lm=1656585817"},
    {"step": "82", "name": "FC St. Pauli", "id": 35, "wappen": "https://tmssl.akamaized.net/images/wappen/head/35.png?lm=1698741498"},
    {"step": "83", "name": "1. FC Heidenheim 1846", "id": 2036, "wappen": "https://tmssl.akamaized.net/images/wappen/head/2036.png?lm=1700207555"},
]

# Known non-player link texts to filter out
EXCLUDED = {
    'News', 'Transfers', 'Profil', 'Leistungsdaten', 'Video ▶️',
    'Neueste Transfers', 'Gerüchteküche', 'Alle Foren', 'Alle News',
    'Marktwert-Analyse', 'Vereinsforen Bundesliga', 'Vereinsforen 2. Bundesliga',
    'Vereinsforen 3. Liga', 'Sportwetten', 'Berater-Support', 'Berater-Firmen',
    'PremiumService', 'Kompakt', 'Erweitert', 'Galerie', '#', 'Spieler',
    'Alter', 'Vertrag', 'Marktwert', 'Wertvollste Spieler der Welt',
    'Aktuelle Gerüchte', 'Aktuelle Marktwert-Updates', 'FIFA-Weltrangliste',
    'Wettanbieter Deutschland', 'Paten und Datenpfleger',
    'Als Pate oder Datenpfleger bewerben', '11 Gebote', 'Fehler gefunden?',
    'Offene Stellen', 'Kontakt', 'Das TM-Team', 'FAQ', 'Wahretabelle',
    'Soccerdonna.de', 'Scoutastic.com', 'Impressum', 'Datenschutz',
    'Privatsphäre', 'Widerruf Tracking', 'Nutzungsbedingungen', 'Media',
    'Bundesliga', '1.Liga',
}

def parse_club_file(filepath, club):
    """Parse a single club's markdown file to extract player data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    players = []
    
    # Pattern: [Player Name](https://www.transfermarkt.de/SLUG/profil/spieler/ID)
    profil_pattern = re.compile(
        r'\[([^\]]+)\]\(https://www\.transfermarkt\.de/[^/]+/profil/spieler/(\d+)\)'
    )
    
    # Pattern: [Market Value](https://www.transfermarkt.de/SLUG/marktwertverlauf/spieler/ID)
    mv_pattern = re.compile(
        r'\[([^\]]+)\]\(https://www\.transfermarkt\.de/[^/]+/marktwertverlauf/spieler/(\d+)\)'
    )
    
    # Build market value lookup
    mv_map = {}
    for mv_match in mv_pattern.finditer(content):
        mv_value = mv_match.group(1).strip()
        mv_id = mv_match.group(2)
        mv_map[mv_id] = mv_value
    
    # Extract players from profile links
    seen_ids = set()
    for match in profil_pattern.finditer(content):
        name = match.group(1).strip()
        player_id = match.group(2)
        
        # Skip duplicates
        if player_id in seen_ids:
            continue
        
        # Skip non-player names
        if name in EXCLUDED:
            continue
        if len(name) < 2:
            continue
        
        # Skip links that are obviously navigation
        if any(kw in name.lower() for kw in ['u19', 'u17', 'jugend', 'uefa', ' ii']):
            continue
        
        seen_ids.add(player_id)
        
        # Construct image URL
        image_url = f"https://img.a.transfermarkt.technology/portrait/medium/{player_id}-1700000000.jpg?lm=1"
        
        market_value = mv_map.get(player_id, '')
        
        players.append({
            "Nummer": "",
            "Bild": image_url,
            "Name": name,
            "Position": "",
            "Geburtsdatum": "",
            "Marktwert": market_value,
            "Wappen": club['wappen'],
            "Verein": club['name'],
        })
    
    return players


def main():
    all_players = []
    
    for club in CLUBS:
        filepath = os.path.join(BASE, club['step'], 'content.md')
        if not os.path.exists(filepath):
            print(f"WARNING: File not found for {club['name']}: {filepath}")
            continue
        
        players = parse_club_file(filepath, club)
        print(f"{club['name']}: {len(players)} players")
        all_players.extend(players)
    
    print(f"\n{'='*50}")
    print(f"Total players: {len(all_players)}")
    print(f"Total clubs: {len(CLUBS)}")
    
    # Verify clubs
    clubs_found = set(p['Verein'] for p in all_players)
    print(f"Clubs found: {len(clubs_found)}")
    for c in sorted(clubs_found):
        count = sum(1 for p in all_players if p['Verein'] == c)
        print(f"  {c}: {count}")
    
    # Save
    output_path = "/Users/Jo/Spieler/src/jsonspieler.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_players, f, ensure_ascii=False, indent=2)
    
    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    main()
