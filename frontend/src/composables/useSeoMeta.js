import { onMounted, onBeforeUnmount } from 'vue'

function setOrCreateMeta(selector, attrs) {
  let el = document.head.querySelector(selector)
  if (!el) {
    el = document.createElement(attrs.tag || 'meta')
    for (const [key, value] of Object.entries(attrs)) {
      if (key === 'tag') continue
      el.setAttribute(key, value)
    }
    document.head.appendChild(el)
    return el
  }
  for (const [key, value] of Object.entries(attrs)) {
    if (key === 'tag') continue
    el.setAttribute(key, value)
  }
  return el
}

export function useSeoMeta({ title, description, canonical, jsonLd } = {}) {
  const previous = { title: '', description: '', canonical: '', ogUrl: '', ogTitle: '', ogDescription: '' }
  let jsonLdEl = null

  onMounted(() => {
    if (title) {
      previous.title = document.title
      document.title = title
      previous.ogTitle = document.head.querySelector('meta[property="og:title"]')?.getAttribute('content') || ''
      setOrCreateMeta('meta[property="og:title"]', { property: 'og:title', content: title })
    }

    if (description) {
      const descEl = document.head.querySelector('meta[name="description"]')
      previous.description = descEl?.getAttribute('content') || ''
      setOrCreateMeta('meta[name="description"]', { name: 'description', content: description })

      previous.ogDescription = document.head.querySelector('meta[property="og:description"]')?.getAttribute('content') || ''
      setOrCreateMeta('meta[property="og:description"]', { property: 'og:description', content: description })
    }

    if (canonical) {
      const linkEl = document.head.querySelector('link[rel="canonical"]')
      previous.canonical = linkEl?.getAttribute('href') || ''
      if (linkEl) {
        linkEl.setAttribute('href', canonical)
      } else {
        const l = document.createElement('link')
        l.setAttribute('rel', 'canonical')
        l.setAttribute('href', canonical)
        document.head.appendChild(l)
      }

      previous.ogUrl = document.head.querySelector('meta[property="og:url"]')?.getAttribute('content') || ''
      setOrCreateMeta('meta[property="og:url"]', { property: 'og:url', content: canonical })
    }

    if (jsonLd) {
      jsonLdEl = document.createElement('script')
      jsonLdEl.type = 'application/ld+json'
      jsonLdEl.setAttribute('data-seo-route', 'true')
      jsonLdEl.textContent = JSON.stringify(jsonLd)
      document.head.appendChild(jsonLdEl)
    }
  })

  onBeforeUnmount(() => {
    if (previous.title) document.title = previous.title
    if (previous.description) {
      document.head.querySelector('meta[name="description"]')?.setAttribute('content', previous.description)
    }
    if (previous.ogTitle) {
      document.head.querySelector('meta[property="og:title"]')?.setAttribute('content', previous.ogTitle)
    }
    if (previous.ogDescription) {
      document.head.querySelector('meta[property="og:description"]')?.setAttribute('content', previous.ogDescription)
    }
    if (previous.canonical) {
      document.head.querySelector('link[rel="canonical"]')?.setAttribute('href', previous.canonical)
    }
    if (previous.ogUrl) {
      document.head.querySelector('meta[property="og:url"]')?.setAttribute('content', previous.ogUrl)
    }
    if (jsonLdEl?.parentNode) jsonLdEl.parentNode.removeChild(jsonLdEl)
  })
}
