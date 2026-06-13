import React, { useState } from 'react'
import InvertedMathEncoder from './components/InvertedMathEncoder'
import SeamCarveProcessor from './SeamCarveProcessor'
import MetaViewer from './components/MetaViewer'

const panels = [
  { key: 'home', label: 'Home' },
  { key: 'seam', label: 'Seam Carve' },
  { key: 'encoder', label: 'Inverted math' },
  { key: 'meta', label: 'Meta' },
]

export default function PiLogicDashboard() {
  const [activePanel, setActivePanel] = useState('home')

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: 20 }}>
      <header style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 12 }}>
        <h3 style={{ margin: 0 }}>PiLogic Dashboard</h3>
        <nav style={{ display: 'flex', gap: 8 }}>
          {panels.map(p => (
            <button
              key={p.key}
              onClick={() => setActivePanel(p.key)}
              style={{
                padding: '6px 10px',
                background: activePanel === p.key ? '#2d3748' : '#edf2f7',
                color: activePanel === p.key ? '#fff' : '#2d3748',
                border: 'none',
                borderRadius: 6,
                cursor: 'pointer'
              }}
            >
              {p.label}
            </button>
          ))}
        </nav>
      </header>

      <main>
        {activePanel === 'home' && <div>Welcome — select a panel.</div>}
        {activePanel === 'seam' && <SeamCarveProcessor />}
        {activePanel === 'encoder' && <InvertedMathEncoder />}
        {activePanel === 'meta' && <MetaViewer />}
      </main>
    </div>
  )
}
