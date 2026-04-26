#!/usr/bin/env python3
"""
Fetch correct player portrait image URLs from the Transfermarkt API
and update players.json with the working URLs.

Usage: python3 scripts/fix_images.py
"""
import json
import re
import time
import urllib.request
import urllib.error
import os

PLAYERS_PATH = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'players.json')
API_BASE = 'https://transfermarkt-api.fly.dev'
DELAY = 0.5  # seconds between API requests

def fetch_json(url):
    """Fetch a URL and return parsed JSON."""
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json',
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f'  HTTP {e.code}')
        return None
    except Exception as e:
        print(f'  Error: {e}')
        return None

def extract_player_id(bild_url):
    """Extract numeric player ID from the Bild URL."""
    m = re.search(r'/(\d+)(?:-\d+)?\.jpg', bild_url)
    return m.group(1) if m else None

def main():
    print('📂 Loading players.json...')
    with open(PLAYERS_PATH, 'r', encoding='utf-8') as f:
        players = json.load(f)
    print(f'   Found {len(players)} players\n')

    # Deduplicate: group by player ID to avoid redundant API calls
    id_to_indices = {}
    for i, p in enumerate(players):
        pid = extract_player_id(p['Bild'])
        if pid:
            id_to_indices.setdefault(pid, []).append(i)

    unique_ids = list(id_to_indices.keys())
    print(f'🔑 Unique player IDs: {len(unique_ids)}\n')

    updated = 0
    failed = 0
    already_ok = 0

    for idx, pid in enumerate(unique_ids):
        # Check if already has timestamp in URL
        sample_url = players[id_to_indices[pid][0]]['Bild']
        if re.search(r'/\d+-\d+\.jpg', sample_url):
            already_ok += 1
            continue

        print(f'[{idx+1}/{len(unique_ids)}] Player ID {pid}... ', end='', flush=True)

        data = fetch_json(f'{API_BASE}/players/{pid}/profile')
        if data and 'imageUrl' in data:
            new_url = data['imageUrl']
            name = data.get('name', '?')
            print(f'✅ {name} → {new_url[-40:]}')

            # Update all players with this ID
            for i in id_to_indices[pid]:
                players[i]['Bild'] = new_url
            updated += 1
        else:
            print('⚠️  No imageUrl found')
            failed += 1

        time.sleep(DELAY)

    print(f'\n📊 Results:')
    print(f'   ✅ Updated: {updated}')
    print(f'   ✅ Already OK: {already_ok}')
    print(f'   ⚠️  Failed: {failed}')

    # Save
    with open(PLAYERS_PATH, 'w', encoding='utf-8') as f:
        json.dump(players, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f'\n💾 Saved → {PLAYERS_PATH}')

if __name__ == '__main__':
    main()
