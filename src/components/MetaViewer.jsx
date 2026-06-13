import React, { useEffect, useState } from 'react'
import { getPositronMetaLogs } from '../lib/IntegratedLKLJrDatabase'

export default function MetaViewer() {
  const [logs, setLogs] = useState([])
  const [active, setActive] = useState(null)

  const refresh = () => {
    setLogs(getPositronMetaLogs())
    try {
      const a = JSON.parse(localStorage.getItem('positron_imaging_meta') || 'null')
      setActive(a)
    } catch (e) {
      setActive(null)
    }
  }

  useEffect(() => {
    refresh()
  }, [])

  const clearMetaLog = () => {
    localStorage.removeItem('positron_imaging_meta_log')
    localStorage.removeItem('positron_imaging_meta')
    refresh()
  }

  const exportMetaLog = () => {
    const payload = {
      active: active || null,
      log: logs || [],
      exportedAt: new Date().toISOString(),
    }
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `positron_meta_${Date.now()}.json`
    document.body.appendChild(a)
    a.click()
    a.remove()
    URL.revokeObjectURL(url)
  }

  return (
    <div style={{ border: '1px solid #e2e8f0', padding: 12, borderRadius: 8 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
        <div style={{ fontWeight: 600 }}>Positron Imaging Metadata</div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button onClick={exportMetaLog} style={{ padding: '6px 10px' }}>Export</button>
          <button onClick={clearMetaLog} style={{ padding: '6px 10px', background: '#e53e3e', color: '#fff', border: 'none', borderRadius: 6 }}>Clear</button>
        </div>
      </div>

      <div style={{ marginBottom: 8 }}>
        <strong>Active meta:</strong>
        <pre style={{ background: '#f7fafc', padding: 8, borderRadius: 6 }}>{active ? JSON.stringify(active, null, 2) : 'none'}</pre>
      </div>
      <div>
        <strong>Meta log ({logs.length})</strong>
        <pre style={{ background: '#f7fafc', padding: 8, borderRadius: 6, maxHeight: 220, overflow: 'auto' }}>{JSON.stringify(logs, null, 2)}</pre>
      </div>
    </div>
  )
}
