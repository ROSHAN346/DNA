import React, { useEffect, useState } from 'react'
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer, Tooltip } from 'recharts'
import { api } from '../api'

export default function AttentionPage() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.getAttention().then(setData).finally(() => setLoading(false))
  }, [])

  const max = Math.max(...data.map(d => d.weight), 1)

  if (loading) return <div className="spinner" />

  return (
    <div>
      <h2 style={{ fontSize: 20, marginBottom: 20 }}>⚡ Dynamic Attention</h2>
      <p style={{ color: 'var(--muted)', fontSize: 12, marginBottom: 20 }}>
        Tracks which chromosome domains have been most recently activated. Weights decay 5% per cycle.
      </p>

      {data.length === 0
        ? <div style={{ color: 'var(--muted)' }}>No attention data yet. Run a search to activate chromosomes.</div>
        : (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
            {/* Radar chart */}
            <div className="card">
              <div className="section-title">Activation Radar</div>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={data}>
                  <PolarGrid stroke="var(--border)" />
                  <PolarAngleAxis dataKey="chromosome" tick={{ fontSize: 11, fill: 'var(--muted)' }} />
                  <Radar dataKey="weight" stroke="var(--accent)" fill="var(--accent)" fillOpacity={0.25} />
                  <Tooltip contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', fontSize: 12 }} />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            {/* Weight bars */}
            <div className="card">
              <div className="section-title">Chromosome Weights</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                {[...data].sort((a,b) => b.weight - a.weight).map((d, i) => (
                  <div key={i}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginBottom: 3 }}>
                      <span>{d.chromosome}</span>
                      <span style={{ fontFamily: 'monospace', color: 'var(--accent)' }}>{d.weight.toFixed(3)}</span>
                    </div>
                    <div style={{ background: 'var(--border)', borderRadius: 4, height: 6 }}>
                      <div style={{
                        background: 'var(--accent)',
                        width: `${(d.weight / max) * 100}%`,
                        height: '100%',
                        borderRadius: 4,
                        transition: 'width .4s',
                      }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )
      }
    </div>
  )
}
