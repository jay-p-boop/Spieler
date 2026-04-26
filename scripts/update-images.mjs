#!/usr/bin/env node
/**
 * Fetch actual player portrait image URLs from Transfermarkt profile pages.
 * 
 * For each player in players.json, visits their Transfermarkt profile to extract
 * the correct image URL (with timestamp), then writes the updated JSON back.
 *
 * Usage: node scripts/update-images.mjs
 */

import { readFile, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import https from 'node:https'

const __dirname = dirname(fileURLToPath(import.meta.url))
const PLAYERS_PATH = join(__dirname, '..', 'src', 'data', 'players.json')

// Rate limiting: wait between requests to not hammer TM
const DELAY_MS = 800

function sleep(ms) { return new Promise(r => setTimeout(r, ms)) }

/**
 * Fetch a URL and return the raw HTML body.
 */
function fetchHTML(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'de-DE,de;q=0.9,en;q=0.8',
        'Referer': 'https://www.transfermarkt.de/',
      },
    }, (res) => {
      // Follow redirects
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        fetchHTML(res.headers.location).then(resolve).catch(reject)
        return
      }
      let data = ''
      res.on('data', chunk => data += chunk)
      res.on('end', () => resolve(data))
    })
    req.on('error', reject)
    req.setTimeout(10000, () => { req.destroy(); reject(new Error('Timeout')) })
  })
}

/**
 * Extract the player portrait URL from a Transfermarkt profile page HTML.
 * Looks for <img> tags with data-src or src attributes containing "portrait".
 */
function extractPortraitUrl(html) {
  // Pattern 1: data-src attribute (lazy loaded images)
  const dataSrcMatch = html.match(/data-src="(https:\/\/img\.a\.transfermarkt\.technology\/portrait\/[^"]+)"/i)
  if (dataSrcMatch) return dataSrcMatch[1]

  // Pattern 2: regular src attribute
  const srcMatch = html.match(/src="(https:\/\/img\.a\.transfermarkt\.technology\/portrait\/[^"]+)"/i)
  if (srcMatch) return srcMatch[1]

  // Pattern 3: look in JSON-LD or meta tags
  const ogMatch = html.match(/content="(https:\/\/img\.a\.transfermarkt\.technology\/portrait\/[^"]+)"/i)
  if (ogMatch) return ogMatch[1]

  return null
}

/**
 * Build Transfermarkt profile URL from player ID.
 */
function profileUrl(playerId) {
  return `https://www.transfermarkt.de/x/profil/spieler/${playerId}`
}

/**
 * Extract player ID from current Bild URL.
 */
function extractPlayerId(bildUrl) {
  // Match patterns like /header/17259.jpg or /medium/17259-123456.jpg
  const m = bildUrl.match(/\/(\d+)(?:-\d+)?\.jpg/)
  return m ? m[1] : null
}

async function main() {
  console.log('📂 Loading players.json...')
  const raw = await readFile(PLAYERS_PATH, 'utf-8')
  const players = JSON.parse(raw)
  console.log(`   Found ${players.length} players\n`)

  let updated = 0
  let failed = 0
  let skipped = 0

  for (let i = 0; i < players.length; i++) {
    const p = players[i]
    const pid = extractPlayerId(p.Bild)
    
    if (!pid) {
      console.log(`⏭️  [${i + 1}/${players.length}] ${p.Name}: Could not extract player ID from ${p.Bild}`)
      skipped++
      continue
    }

    const url = profileUrl(pid)
    process.stdout.write(`🔍 [${i + 1}/${players.length}] ${p.Name} (${pid})... `)
    
    try {
      const html = await fetchHTML(url)
      const imgUrl = extractPortraitUrl(html)
      
      if (imgUrl) {
        if (imgUrl !== p.Bild) {
          p.Bild = imgUrl
          console.log(`✅ Updated → ${imgUrl.substring(0, 80)}...`)
          updated++
        } else {
          console.log('✅ Already correct')
          skipped++
        }
      } else {
        console.log('⚠️  No portrait URL found in HTML')
        failed++
      }
    } catch (err) {
      console.log(`❌ ${err.message}`)
      failed++
    }

    await sleep(DELAY_MS)
  }

  console.log(`\n📊 Results: ${updated} updated, ${failed} failed, ${skipped} skipped`)
  
  // Save updated JSON
  await writeFile(PLAYERS_PATH, JSON.stringify(players, null, 2) + '\n', 'utf-8')
  console.log(`💾 Saved → ${PLAYERS_PATH}`)
}

main().catch(err => {
  console.error('Fatal error:', err)
  process.exit(1)
})
