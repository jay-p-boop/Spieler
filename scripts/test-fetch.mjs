#!/usr/bin/env node
/**
 * Quick test: fetch ONE player profile page and extract the portrait URL.
 */

import https from 'node:https'

function fetchHTML(url) {
  return new Promise((resolve, reject) => {
    const req = https.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html',
        'Accept-Language': 'de-DE,de;q=0.9',
      },
    }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        console.log('Redirect →', res.headers.location)
        fetchHTML(res.headers.location).then(resolve).catch(reject)
        return
      }
      console.log('Status:', res.statusCode)
      let data = ''
      res.on('data', chunk => data += chunk)
      res.on('end', () => resolve(data))
    })
    req.on('error', reject)
    req.setTimeout(15000, () => { req.destroy(); reject(new Error('Timeout')) })
  })
}

async function main() {
  const url = 'https://www.transfermarkt.de/manuel-neuer/profil/spieler/17259'
  console.log('Fetching:', url)
  const html = await fetchHTML(url)
  console.log('HTML length:', html.length)
  
  // Extract ALL image URLs with "portrait" or "transfermarkt"
  const imgMatches = html.match(/(?:data-src|src)="(https:\/\/img\.a\.transfermarkt\.technology\/portrait\/[^"]+)"/gi) || []
  console.log('\nPortrait image URLs found:')
  imgMatches.forEach(m => console.log(' ', m))
  
  // Also look for og:image meta tags
  const ogMatch = html.match(/property="og:image"\s+content="([^"]+)"/i)
  if (ogMatch) console.log('\nog:image:', ogMatch[1])
  
  // Also check for any img.a.transfermarkt references
  const allTmImgs = html.match(/img\.a\.transfermarkt\.technology[^"'\s]*/g) || []
  console.log('\nAll transfermarkt image refs:')
  ;[...new Set(allTmImgs)].forEach(u => console.log(' ', u))
}

main().catch(console.error)
