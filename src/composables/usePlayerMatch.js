/**
 * usePlayerMatch — Intelligent Fuzzy Player Matching
 * Combines Levenshtein distance + phonetic matching
 * Handles umlauts, accents, partial names
 */
import levenshtein from 'fast-levenshtein'

/**
 * Normalize text for comparison
 * - lowercase, trim, remove accents/umlauts, strip punctuation
 */
function normalize(text) {
  return text
    .toLowerCase()
    .trim()
    .replace(/ä/g, 'ae').replace(/ö/g, 'oe').replace(/ü/g, 'ue')
    .replace(/ß/g, 'ss')
    .replace(/é|è|ê|ë/g, 'e')
    .replace(/á|à|â/g, 'a')
    .replace(/í|ì|î/g, 'i')
    .replace(/ó|ò|ô/g, 'o')
    .replace(/ú|ù|û/g, 'u')
    .replace(/ç/g, 'c')
    .replace(/ñ/g, 'n')
    .replace(/[^a-z0-9\s]/g, '')
    .replace(/\s+/g, ' ')
}

/**
 * Simple consonant-based phonetic code (German-optimized)
 */
function phoneticCode(str) {
  const n = normalize(str)
  return n
    .replace(/[aeiou]/g, '')     // strip vowels
    .replace(/(.)\1+/g, '$1')    // deduplicate consonants
    .slice(0, 8)                 // take first 8 consonant chars
}

/**
 * Calculate match confidence (0-100) between spoken word and player name
 */
function matchConfidence(spoken, playerName) {
  const s = normalize(spoken)
  const p = normalize(playerName)

  // Exact match
  if (s === p) return 100

  // Check each part of the player name (first/last)
  const parts = p.split(' ')
  const lastName = parts[parts.length - 1]
  const firstName = parts[0]

  // Exact last name match
  if (s === lastName) return 95

  // Levenshtein on full name
  const fullDist = levenshtein.get(s, p)
  const maxLen = Math.max(s.length, p.length)
  const fullScore = Math.max(0, 100 - (fullDist / maxLen) * 100)

  // Levenshtein on last name only
  const lastDist = levenshtein.get(s, lastName)
  const lastMaxLen = Math.max(s.length, lastName.length)
  const lastScore = Math.max(0, 100 - (lastDist / lastMaxLen) * 100)

  // Levenshtein on first name
  const firstDist = levenshtein.get(s, firstName)
  const firstMaxLen = Math.max(s.length, firstName.length)
  const firstScore = Math.max(0, 100 - (firstDist / firstMaxLen) * 100)

  // Phonetic similarity
  const spokenPhonetic = phoneticCode(spoken)
  const namePhonetic = phoneticCode(playerName)
  const lastPhonetic = phoneticCode(lastName)
  const phoneticScore = spokenPhonetic === namePhonetic ? 20 :
                        spokenPhonetic === lastPhonetic ? 15 : 0

  // Starts-with bonus
  const startsBonus = p.startsWith(s) || lastName.startsWith(s) ? 15 : 0

  // Contains bonus (for partial matches)
  const containsBonus = p.includes(s) && s.length >= 3 ? 10 : 0

  // Weighted combination
  const best = Math.max(fullScore, lastScore * 0.95, firstScore * 0.8)
  return Math.min(100, best + phoneticScore + startsBonus + containsBonus)
}

export function usePlayerMatch(players) {

  /**
   * Find the best matching player for a spoken word
   * Returns { player, confidence } or null
   */
  function findPlayer(spoken) {
    if (!spoken || spoken.length < 2) return null

    let bestPlayer = null
    let bestConfidence = 0

    for (const player of players) {
      const conf = matchConfidence(spoken, player.Name)
      if (conf > bestConfidence) {
        bestConfidence = conf
        bestPlayer = player
      }
    }

    if (bestConfidence < 40) return null

    return {
      player: bestPlayer,
      confidence: Math.round(bestConfidence),
    }
  }

  /**
   * Find best matching club
   */
  function findClub(spoken) {
    if (!spoken || spoken.length < 2) return null

    let bestClub = null
    let bestConfidence = 0

    const clubs = [...new Set(players.map(p => p.Verein))]

    for (const club of clubs) {
      const conf = matchConfidence(spoken, club)
      if (conf > bestConfidence) {
        bestConfidence = conf
        bestClub = club
      }
    }

    if (bestConfidence < 35) return null

    return {
      club: bestClub,
      confidence: Math.round(bestConfidence),
    }
  }

  /**
   * Check if spoken word matches a specific player (threshold-based)
   */
  function isMatch(spoken, playerName, threshold = 65) {
    return matchConfidence(spoken, playerName) >= threshold
  }

  return { findPlayer, findClub, isMatch, matchConfidence }
}
