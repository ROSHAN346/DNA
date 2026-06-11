import React, { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import { api } from '../api'

export default function LearningPage() {
  const [summary, setSummary] = useState([])
  const [experiences, setExperiences] = useState([])
  const [policy, setPolicy] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.getLearningSummary().then(setSummary),
      api.getExperiences().then(setExperiences),
      api.getPolicy().then(setPolicy),
    ]).finally(() => setLoading(false))
  }, [])

  const topGenes = Object.entries(policy.genes || {})
    .sort((a, b) => b[1] - a[1]).slice(0, 8)
    .map(([k, v]) => ({ name: k.slice(0, 24), reward: v }))

  const topChrom = Object.entries(policy.chromosomes || {})
    .sort((a, b) => b[1] - a[1])
    .map(([k, v]) => ({ name: k, reward: v }))

  if (loading) return <div className="spinner" />

  return (
    <div>
      <h2 style={{ fontSize: 20, marginBottom: 20 }}>📚 Learning & Policy</h2>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 20 }}>
        {/* Gene rewards */}
        <div className="card">
          <div className="section-title">Top Rewarded Genes</div>
          {topGenes.length > 0
            ? <ResponsiveContainer width="100%" height={200}>
                <BarChart data={topGenes} layout="vertical" margin={{ left: 10, right: 16 }}>
                  <XAxis type="number" tick={{ fontSize: 10, fill: '#64748b' }} />
                  <YAxis type="category" dataKey="name" width={130} tick={{ fontSize: 10, fill: '#94a3b8' }} />
                  <Tooltip contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', fontSize: 11 }} />
                  <Bar dataKey="reward" fill="var(--accent)" radius={[0,3,3,0]} />
                </BarChart>
              </ResponsiveContainer>
            : <div style={{ color: 'var(--muted)', fontSize: 12 }}>No policy data yet.</div>
          }
        </div>

        {/* Chromosome rewards */}
        <div className="card">
          <div className="section-title">Chromosome Rewards</div>
          {topChrom.length > 0
            ? <ResponsiveContainer width="100%" height={200}>
                <BarChart data={topChrom} layout="vertical" margin={{ left: 10, right: 16 }}>
                  <XAxis type="number" tick={{ fontSize: 10, fill: '#64748b' }} />
                  <YAxis type="category" dataKey="name" width={100} tick={{ fontSize: 10, fill: '#94a3b8' }} />
                  <Tooltip contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', fontSize: 11 }} />
                  <Bar dataKey="reward" fill="#7c3aed" radius={[0,3,3,0]} />
                </BarChart>
              </ResponsiveContainer>
            : <div style={{ color: 'var(--muted)', fontSize: 12 }}>No policy data yet.</div>
          }
        </div>
      </div>

      {/* Knowledge usage summary */}
      {summary.length > 0 && (
        <div className="card" style={{ marginBottom: 16 }}>
          <div className="section-title">Most Retrieved Knowledge</div>
          {summary.slice(0, 10).map((s, i) => (
            <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '5px 0',
              borderBottom: '1px solid var(--border)', fontSize: 12 }}>
              <span style={{ color: 'var(--text)', flex: 1 }}>{s.knowledge}</span>
              <span className="badge badge-green">{s.count}×</span>
            </div>
          ))}
        </div>
      )}

      {/* Experience log */}
      <div className="card">
        <div className="section-title">Recent Experiences ({experiences.length})</div>
        <div style={{ maxHeight: 260, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 8 }}>
          {experiences.slice(-20).reverse().map((e, i) => (
            <div key={i} style={{ borderLeft: '2px solid var(--border)', paddingLeft: 10, fontSize: 12 }}>
              <div style={{ color: 'var(--muted)' }}>Q: <span style={{ color: 'var(--text)' }}>{e.query}</span></div>
              <div style={{ color: 'var(--muted)' }}>A: <span style={{ color: 'var(--accent)' }}>{e.result}</span>
                <span className={`badge ${e.source === 'DNA' ? 'badge-green' : 'badge-blue'}`} style={{ marginLeft: 6 }}>{e.source}</span>
                <span style={{ marginLeft: 6, fontFamily: 'monospace' }}>{(e.score * 100).toFixed(1)}%</span>
              </div>
            </div>
          ))}
          {experiences.length === 0 && <div style={{ color: 'var(--muted)' }}>No experiences yet. Run a search.</div>}
        </div>
      </div>
    </div>
  )
}
