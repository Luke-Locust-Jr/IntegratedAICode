import React, { useRef, useState } from 'react'
import { getPositronMetaLogs, attachEncodedToLatestMeta } from './lib/IntegratedLKLJrDatabase'

export default function SeamCarveProcessor() {
  const [running, setRunning] = useState(false)
  const [lastMeta, setLastMeta] = useState(null)
  const fileRef = useRef(null)

  const simulateRun = async () => {
    const file = fileRef.current?.files?.[0]
    if (!file) return alert('Choose an image file to simulate seam carve')
    setRunning(true)

    // Simulate work
    await new Promise(r => setTimeout(r, 600))

    const meta = {
      author: 'lukelocustjr',
      algorithm: 'Pi Logic Inverse Mirror Seam Carve',
      originalFilename: file.name,
      originalDimensions: { w: 800, h: 600 },
      outputDimensions: { w: 760, h: 600 },
      seamsRemoved: 40,
      avgEnergyPerSeam: [0.123456],
      omegaConstant: Math.PI,
      timestamp: new Date().toISOString(),
    }

    // store active seam-carve meta
    localStorage.setItem('positron_imaging_meta', JSON.stringify(meta))

    // Merge any pending encoder entries from the meta log into this meta
    try {
      const logs = getPositronMetaLogs()
      const pending = logs.filter(l => l.source === 'InvertedMathEncoder' && !l.mergedInto)
      for (const p of pending) {
        await attachEncodedToLatestMeta(p)
      }
    } catch (err) {
      console.warn('Failed to merge encoder entries', err)
    }

    setLastMeta(JSON.parse(localStorage.getItem('positron_imaging_meta')))
    setRunning(false)
  }

  return (
    <div style={{ border: '1px solid #e2e8f0', padding: 12, borderRadius: 8 }}>
      <div style={{ marginBottom: 8 }}>Seam Carve (simulated)</div>
      <input ref={fileRef} type="file" accept="image/*" />
      <div style={{ marginTop: 8 }}>
        <button onClick={simulateRun} disabled={running} style={{ padding: '6px 10px' }}>
          {running ? 'Running…' : 'Run Seam Carve'}
        </button>
      </div>

      {lastMeta && (
        <pre style={{ marginTop: 12, background: '#f7fafc', padding: 8, borderRadius: 6 }}>
          {JSON.stringify(lastMeta, null, 2)}
        </pre>
      )}
    </div>
  )
}
