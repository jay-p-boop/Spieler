#!/usr/bin/env python3
"""
Scrape Bundesliga 2025/26 squad data from Transfermarkt.
Generates a clean JSON file for the Poki app.
"""
import json
import re
import urllib.request
import urllib.error
import time
import ssl

# Disable SSL verification for scraping
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'de-DE,de;q=0.9',
}

CLUBS = [
    {"id": 27, "slug": "fc-bayern-munchen", "name": "FC Bayern München", "wappen": "https://tmssl.akamaized.net/images/wappen/head/27.png?lm=1498251238"},
    {"id": 16, "slug": "borussia-dortmund", "name": "Borussia Dortmund", "wappen": "https://tmssl.akamaized.net/images/wappen/head/16.png?lm=1396275280"},
    {"id": 23826, "slug": "rasenballsport-leipzig", "name": "RB Leipzig", "wappen": "https://tmssl.akamaized.net/images/wappen/head/23826.png?lm=1619431624"},
    {"id": 15, "slug": "bayer-04-leverkusen", "name": "Bayer 04 Leverkusen", "wappen": "https://tmssl.akamaized.net/images/wappen/head/15.png?lm=1651221781"},
    {"id": 24, "slug": "eintracht-frankfurt", "name": "Eintracht Frankfurt", "wappen": "https://tmssl.akamaized.net/images/wappen/head/24.png?lm=1603277045"},
    {"id": 79, "slug": "vfb-stuttgart", "name": "VfB Stuttgart", "wappen": "https://tmssl.akamaized.net/images/wappen/head/79.png?lm=1618158538"},
    {"id": 533, "slug": "tsg-1899-hoffenheim", "name": "TSG 1899 Hoffenheim", "wappen": "https://tmssl.akamaized.net/images/wappen/head/533.png?lm=1462358637"},
    {"id": 82, "slug": "vfl-wolfsburg", "name": "VfL Wolfsburg", "wappen": "https://tmssl.akamaized.net/images/wappen/head/82.png?lm=1467356331"},
    {"id": 60, "slug": "sc-freiburg", "name": "SC Freiburg", "wappen": "https://tmssl.akamaized.net/images/wappen/head/60.png?lm=1517249279"},
    {"id": 86, "slug": "sv-werder-bremen", "name": "SV Werder Bremen", "wappen": "https://tmssl.akamaized.net/images/wappen/head/86.png?lm=1596112862"},
    {"id": 41, "slug": "hamburger-sv", "name": "Hamburger SV", "wappen": "https://tmssl.akamaized.net/images/wappen/head/41.png?lm=1702627785"},
    {"id": 167, "slug": "fc-augsburg", "name": "FC Augsburg", "wappen": "https://tmssl.akamaized.net/images/wappen/head/167.png?lm=1656073509"},
    {"id": 18, "slug": "borussia-monchengladbach", "name": "Borussia Mönchengladbach", "wappen": "https://tmssl.akamaized.net/images/wappen/head/18.png?lm=1656585791"},
    {"id": 39, "slug": "1-fsv-mainz-05", "name": "1. FSV Mainz 05", "wappen": "https://tmssl.akamaized.net/images/wappen/head/39.png?lm=1564476037"},
    {"id": 3, "slug": "1-fc-koln", "name": "1. FC Köln", "wappen": "https://tmssl.akamaized.net/images/wappen/head/3.png?lm=1656585763"},
    {"id": 89, "slug": "1-fc-union-berlin", "name": "1. FC Union Berlin", "wappen": "https://tmssl.akamaized.net/images/wappen/head/89.png?lm=1656585817"},
    {"id": 35, "slug": "fc-st-pauli", "name": "FC St. Pauli", "wappen": "https://tmssl.akamaized.net/images/wappen/head/35.png?lm=1698741498"},
    {"id": 2036, "slug": "1-fc-heidenheim-1846", "name": "1. FC Heidenheim 1846", "wappen": "https://tmssl.akamaized.net/images/wappen/head/2036.png?lm=1700207555"},
]

def fetch_url(url):
    """Fetch URL content with retries."""
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=ctx, timeout=15) as response:
                return response.read().decode('utf-8', errors='replace')
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return None

def parse_squad_page(html, club):
    """Parse player data from a Transfermarkt squad page."""
    players = []
    
    # Extract player entries from the HTML
    # Pattern: player profile links with IDs
    profile_pattern = re.compile(
        r'<a[^>]*href="/([^"]+)/profil/spieler/(\d+)"[^>]*>([^<]+)</a>',
        re.IGNORECASE
    )
    
    # Find all player profile links
    matches = profile_pattern.findall(html)
    
    # Market value pattern
    mv_pattern = re.compile(
        r'<a[^>]*href="/[^"]+/marktwertverlauf/spieler/(\d+)"[^>]*>\s*([^<]+)\s*</a>',
        re.IGNORECASE
    )
    mv_matches = {m[0]: m[1].strip() for m in mv_pattern.findall(html)}
    
    # Player image pattern
    img_pattern = re.compile(
        r'data-src="(https://img\.a\.transfermarkt\.technology/portrait/[^"]+)"',
        re.IGNORECASE
    )
    img_matches = img_pattern.findall(html)
    
    # Jersey number pattern - looking in table rows
    number_pattern = re.compile(
        r'<div class="tm-shirt-number"[^>]*>(\d+)</div>',
        re.IGNORECASE
    )
    number_matches = number_pattern.findall(html)
    
    # Position pattern
    pos_pattern = re.compile(
        r'<td class="posrela"[^>]*>.*?<tr>\s*<td[^>]*>([^<]+)</td>',
        re.IGNORECASE | re.DOTALL
    )
    
    seen_ids = set()
    player_names = []
    
    for slug, player_id, name in matches:
        name = name.strip()
        if player_id in seen_ids:
            continue
        if not name or name in ('News', 'Transfers', 'Profil', 'Leistungsdaten'):
            continue
        if len(name) < 3:
            continue
        seen_ids.add(player_id)
        player_names.append({
            'id': player_id,
            'name': name,
            'slug': slug,
            'marketValue': mv_matches.get(player_id, ''),
        })
    
    return player_names

def get_player_image_url(player_id):
    """Construct player image URL from ID."""
    return f"https://img.a.transfermarkt.technology/portrait/medium/{player_id}-1700000000.jpg?lm=1"

def scrape_club(club):
    """Scrape all players for a given club."""
    url = f"https://www.transfermarkt.de/{club['slug']}/kader/verein/{club['id']}/saison_id/2025"
    print(f"\nScraping {club['name']}...")
    print(f"  URL: {url}")
    
    html = fetch_url(url)
    if not html:
        print(f"  FAILED to fetch {club['name']}")
        return []
    
    players = parse_squad_page(html, club)
    print(f"  Found {len(players)} players")
    
    result = []
    for p in players:
        result.append({
            "Nummer": "",
            "Bild": get_player_image_url(p['id']),
            "Name": p['name'],
            "Position": "",
            "Geburtsdatum": "",
            "Marktwert": p['marketValue'],
            "Wappen": club['wappen'],
            "Verein": club['name'],
            "spielerId": p['id'],
        })
    
    return result

def main():
    all_players = []
    
    for club in CLUBS:
        players = scrape_club(club)
        all_players.extend(players)
        time.sleep(1)  # Be polite
    
    print(f"\n{'='*50}")
    print(f"Total players scraped: {len(all_players)}")
    print(f"Total clubs: {len(CLUBS)}")
    
    # Save to file
    output_path = "../src/jsonspieler.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_players, f, ensure_ascii=False, indent=2)
    
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
