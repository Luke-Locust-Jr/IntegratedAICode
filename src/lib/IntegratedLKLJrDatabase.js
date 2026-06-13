// Minimal positron imaging metadata store abstraction.
// For this scaffold we persist logs to localStorage under key `positron_imaging_meta_log`.

const STORAGE_KEY = 'positron_imaging_meta_log'

export const logPositronMeta = async (meta) => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY) || '[]'
    const arr = JSON.parse(raw)
    arr.push(meta)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(arr))
    return meta
  } catch (err) {
    return Promise.reject(err)
  }
}

export const getPositronMetaLogs = () => {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
  } catch (err) {
    return []
  }
}

export const attachEncodedToLatestMeta = async (encodedEntry) => {
  try {
    const rawMeta = localStorage.getItem('positron_imaging_meta')
    if (!rawMeta) {
      // No active seam-carve meta present — fall back to writing into the meta log
      return logPositronMeta({ source: 'attachEncodedFallback', ...encodedEntry })
    }
    const meta = JSON.parse(rawMeta)
    meta.encodedEntries = meta.encodedEntries || []
    meta.encodedEntries.push(encodedEntry)
    localStorage.setItem('positron_imaging_meta', JSON.stringify(meta))

    // Also keep an entry in the meta log for history
    try {
      const raw = localStorage.getItem(STORAGE_KEY) || '[]'
      const arr = JSON.parse(raw)
      arr.push({ mergedInto: 'positron_imaging_meta', ...encodedEntry })
      localStorage.setItem(STORAGE_KEY, JSON.stringify(arr))
    } catch (e) {
      // ignore logging failures
    }

    return meta
  } catch (err) {
    return Promise.reject(err)
  }
}

export default {
  logPositronMeta,
  getPositronMetaLogs,
}
