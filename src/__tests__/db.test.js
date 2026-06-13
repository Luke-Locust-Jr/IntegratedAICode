import '../setupTests'
import { describe, it, expect, beforeEach } from 'vitest'
import { logPositronMeta, getPositronMetaLogs, attachEncodedToLatestMeta } from '../lib/IntegratedLKLJrDatabase'

beforeEach(() => {
  localStorage.clear()
})

describe('IntegratedLKLJrDatabase', () => {
  it('logs and retrieves meta entries', async () => {
    await logPositronMeta({ source: 'test', value: 1 })
    const logs = getPositronMetaLogs()
    expect(Array.isArray(logs)).toBe(true)
    expect(logs.length).toBe(1)
    expect(logs[0].source).toBe('test')
  })

  it('attaches encoded entry to latest meta', async () => {
    const meta = { author: 'x', algorithm: 'y' }
    localStorage.setItem('positron_imaging_meta', JSON.stringify(meta))
    const entry = { source: 'InvertedMathEncoder', encoded: 'πi' }
    await attachEncodedToLatestMeta(entry)
    const updated = JSON.parse(localStorage.getItem('positron_imaging_meta'))
    expect(updated.encodedEntries).toBeDefined()
    expect(updated.encodedEntries.length).toBe(1)
    expect(updated.encodedEntries[0].encoded).toBe('πi')
  })
})
