import React, { useEffect, useState } from 'react'
import { api } from '../api'

const COLORS = ['#00d4aa','#7c3aed','#f59e0b','#3b82f6','#ef4444','#34d399','#f472b6','#a78bfa']

export default function ConceptsPage() {
  const [concepts, setConcepts] = useState([])
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState('')
  const [clusters, setClusters] = useState(3)

  const load = () => api.getConcepts().then(setConcepts).finally(() => setLoading(false))
  useEffect(() => { load() }, [])

  const act = async (fn, label) => {
    setBusy(label)
    await fn().catch(() => {})
    await load()
    setBusy('')
  }

  if (loading) return <div className="spinner" />

  return (
    <div>
      <h2 style={{ fontSize: 20, marginBottom: 20 }}>💡 Concept Clusters</h2>

      <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 20, flexWrap: 'wrap' }}>
        <button className="btn-secondary" onClick={() => act(api.buildConcepts, 'build')} disabled={!!busy}>
          {busy === 'build' ? <span className="spinner" /> : 'Build Concept Associations'}
        </button>
        <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
          <input
            type="number" min={2} max={10}
            value={clusters}
            onChange={e => setClusters(Number(e.target.value))}
            style={{ width: 60 }}
          />
          <button className="btn-purple" onClick={() => act(() => api.discoverConcepts(clusters), 'discover')} disabled={!!busy}>
            {busy === 'discover' ? <span className="spinner" /> : `K-Means (k=${clusters})`}
          </button>
        </div>
      </div>

      {concepts.length === 0
        ? <div style={{ color: 'var(--muted)' }}>No concepts yet. Run discovery first.</div>
        : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(280px,1fr))', gap: 14 }}>
            {concepts.map((c, i) => (
              <div key={i} className="card" style={{ borderTop: `3px solid ${COLORS[i % COLORS.length]}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span style={{ fontWeight: 600, color: COLORS[i % COLORS.length] }}>
                    {c.concept || c.cluster || `Cluster ${i}`}
                  </span>
                  <span className="badge">{c.size || c.members?.length} members</span>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                  {(c.members || []).map((m, j) => (
                    <div key={j} style={{ fontSize: 12, color: 'var(--muted)', paddingLeft: 8,
                      borderLeft: `2px solid ${COLORS[i % COLORS.length]}40` }}>
                      {m}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )
      }
    </div>
  )
}
