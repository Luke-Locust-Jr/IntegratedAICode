import React, { useState } from 'react'
import { logPositronMeta, attachEncodedToLatestMeta } from '../lib/IntegratedLKLJrDatabase'

// Mirror Python: format(ord(i), '08b')
const charToBinary = (char) =>
  char.charCodeAt(0).toString(2).padStart(8, '0')

// Mirror Python: convert_to_inverted_math(binary)
const toInvertedMath = (binary) =>
  binary.split('').map(b => b === '1' ? 'i' : 'π').join('')

// Mirror Python: convert_to_binary(inverted_math)
const toBinary = (inverted) =>
  inverted.split('').map(c => c === 'i' ? '1' : '0').join('')

// Mirror Python: chr(int(binary_back[i:i+8], 2))
const binaryToText = (binary) => {
  const chars = []
  for (let i = 0; i < binary.length; i += 8) {
    chars.push(String.fromCharCode(parseInt(binary.slice(i, i + 8), 2)))
  }
  return chars.join('')
}

const encode = (sentence) => {
  const binary      = sentence.split('').map(charToBinary).join('')
  const inverted    = toInvertedMath(binary)
  const binaryBack  = toBinary(inverted)
  const output      = binaryToText(binaryBack)
  return { binary, inverted, binaryBack, output }
}

const InvertedMathEncoder = () => {
  const [input,  setInput]  = useState('')
  const [result, setResult] = useState(null)

  const handleEncode = async () => {
    if (!input.trim()) return
    const r = encode(input)
    setResult(r)

    // Log to the positron imaging metadata store and attach to latest seam-carve meta when present
    const entry = {
      source: 'InvertedMathEncoder',
      author: 'lukelocustjr',
      original: input,
      encoded: r.inverted,
      binary: r.binary,
      timestamp: new Date().toISOString(),
    }
    try {
      await logPositronMeta(entry)
    } catch (err) {
      console.warn('Failed to append to meta log', err)
    }
    try {
      await attachEncodedToLatestMeta(entry)
    } catch (err) {
      // non-fatal
    }
  }

  return (
    <div style={s.container}>
      <div style={s.header}>
        <span style={s.badge}>lukelocustjr</span>
        <span style={s.title}>Inverted Math Encoder</span>
      </div>

      <div style={s.inputRow}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleEncode()}
          placeholder="Enter a sentence..."
          style={s.input}
        />
        <button onClick={handleEncode} style={s.btn}>Encode</button>
      </div>

      {result && (
        <div style={s.results}>
          <div style={s.row}>
            <span style={s.label}>Binary</span>
            <code style={s.code}>{result.binary}</code>
          </div>
          <div style={s.row}>
            <span style={s.label}>Inverted math</span>
            <code style={{...s.code, color: '#553c9a', letterSpacing: '0.05em'}}>
              {result.inverted}
            </code>
          </div>
          <div style={s.row}>
            <span style={s.label}>Binary back</span>
            <code style={s.code}>{result.binaryBack}</code>
          </div>
          <div style={s.row}>
            <span style={s.label}>Output</span>
            <code style={{...s.code, color: '#1D9E75', fontWeight: '600'}}>
              {result.output}
            </code>
          </div>
        </div>
      )}

    </div>
  )
}

const s = {
  container: { maxWidth: '600px', margin: '20px auto', fontFamily: 'system-ui, sans-serif', border: '1px solid #e2e8f0', borderRadius: '8px', overflow: 'hidden' },
  header:    { background: '#f7fafc', padding: '10px 16px', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', gap: '10px' },
  badge:     { fontSize: '0.72rem', fontWeight: '600', color: '#1D9E75', background: '#e1f5ee', padding: '3px 8px', borderRadius: '4px' },
  title:     { fontSize: '0.9rem', fontWeight: '600', color: '#2d3748' },
  inputRow:  { display: 'flex', gap: '8px', padding: '16px' },
  input:     { flex: 1, padding: '8px 12px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '0.9rem' },
  btn:       { padding: '8px 16px', background: '#2d3748', color: '#fff', border: 'none', borderRadius: '6px', fontWeight: '600', cursor: 'pointer', fontSize: '0.85rem' },
  results:   { padding: '0 16px 16px' },
  row:       { marginBottom: '10px' },
  label:     { display: 'block', fontSize: '0.7rem', fontWeight: '600', color: '#718096', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: '3px' },
  code:      { display: 'block', fontSize: '0.72rem', color: '#2d3748', wordBreak: 'break-all', background: '#f7fafc', padding: '6px 8px', borderRadius: '4px', border: '1px solid #e2e8f0' },
}

export default InvertedMathEncoder
