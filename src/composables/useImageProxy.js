/**
 * Rewrites external Transfermarkt image URLs through the wsrv.nl
 * image proxy to bypass hotlink protection (Referer/CORS blocking).
 *
 * wsrv.nl is a free, open-source, Cloudflare-backed image proxy
 * that strips the Referer header when fetching from origin servers.
 *
 * @see https://github.com/weserv/images
 */

const WSRV_BASE = 'https://wsrv.nl'

/**
 * Proxy any image URL through wsrv.nl.
 * If the URL is already local or proxied, returns it unchanged.
 *
 * @param {string} url - Original image URL
 * @returns {string} Proxied URL via wsrv.nl
 */
export function proxyImage(url) {
  if (!url || typeof url !== 'string') return ''

  // Skip already-proxied, local, or data URLs
  if (
    url.startsWith(WSRV_BASE) ||
    url.startsWith('/') ||
    url.startsWith('data:')
  ) {
    return url
  }

  // Route external URLs through wsrv.nl proxy
  return `${WSRV_BASE}/?url=${encodeURIComponent(url)}&default=placeholder`
}
