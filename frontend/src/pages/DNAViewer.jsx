import React, { useEffect, useState } from 'react'
import { Trash2 } from 'lucide-react'
import { api } from '../api'

function GenomeBar({ genome = '' }) {
  // show first 80 chars
  const slice = genome.slice(0, 80)
  return (
    <div style={{ fontFamily: 'monospace', fontSize: 11, letterSpacing: 1, lineHeight: 1.8 }}>
      {slice.split('').map((c, i) => (
        <span key={i} className={`dna-${c}`}>{c}</span>
      ))}
      {genome.length > 80 && <span style={{ color: 'var(--muted)' }}>…</span>}
    </div>
  )
}

function StrengthBar({ value }) {
  return (
    <div style={{ background: 'var(--border)', borderRadius: 4, height: 5, width: '100%', marginTop: 4 }}>
      <div style={{
        background: `hsl(${Math.round(value * 120)},70%,45%)`,
        width: `${Math.min(value * 100, 100)}%`,
        height: '100%',
        borderRadius: 4,
        transition: 'width .4s',
      }} />
    </div>
  )
}

export default function DNAViewer() {
  const [genes, setGenes] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('')

  useEffect(() => {
    api.getDNAMemory().then(setGenes).finally(() => setLoading(false))
  }, [])

  const clearAllData = async () => {
    if (!window.confirm("Are you sure you want to clear all DNA and memory data? This will completely reset the brain state and cannot be undone.")) {
      return
    }
    setLoading(true)
    try {
      await api.clearMemory()
      setGenes([])
    } catch (err) {
      alert("Error: " + err.message)
    } finally {
      setLoading(false)
    }
  }

  const shown = genes.filter(g =>
    !filter || g.knowledge?.toLowerCase().includes(filter.toLowerCase()) ||
    g.chromosome?.toLowerCase().includes(filter.toLowerCase())
  )

  if (loading) return <div className="spinner" />

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <h2 style={{ fontSize: 20 }}>🧬 DNA Viewer</h2>
          <span className="badge">{genes.length} genes</span>
        </div>
        <button
          className="btn-danger"
          onClick={clearAllData}
          style={{ display: 'flex', alignItems: 'center', gap: 6 }}
        >
          <Trash2 size={13} />
          Clear DNA Data
        </button>
      </div>

      <input
        placeholder="Filter by knowledge or chromosome…"
        value={filter}
        onChange={e => setFilter(e.target.value)}
        style={{ maxWidth: 360, marginBottom: 16 }}
      />

      {/* Legend */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 16, fontSize: 12 }}>
        {['A','T','C','G'].map(c => (
          <span key={c} className={`dna-${c}`} style={{ fontFamily: 'monospace', fontWeight: 700 }}>
            {c} ■
          </span>
        ))}
        <span style={{ color: 'var(--muted)' }}>— ATCG nucleotide encoding</span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
        {shown.length === 0 && <div style={{ color: 'var(--muted)' }}>No genes. Add memories and consolidate first.</div>}
        {shown.map((g, i) => (
          <div key={i} className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 6 }}>
              <div style={{ flex: 1, paddingRight: 12 }}>
                <span style={{ fontWeight: 600, fontSize: 13 }}>{g.knowledge}</span>
              </div>
              <div style={{ display: 'flex', gap: 6, flexShrink: 0 }}>
                <span className="badge badge-blue">{g.chromosome}</span>
                <span className="badge">gen {g.generation}</span>
                <span className="badge">×{g.usage_count}</span>
              </div>
            </div>
            <GenomeBar genome={g.genome} />
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 6 }}>
              <span style={{ fontSize: 11, color: 'var(--muted)', width: 60 }}>
                strength {(g.strength * 100).toFixed(0)}%
              </span>
              <div style={{ flex: 1 }}><StrengthBar value={g.strength} /></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
