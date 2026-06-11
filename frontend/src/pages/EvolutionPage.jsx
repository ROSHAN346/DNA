import React, { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { api } from '../api'

export default function EvolutionPage() {
  const [fitness, setFitness] = useState([])
  const [log, setLog] = useState([])
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState('')

  const loadFitness = () => api.getFitness().then(setFitness).finally(() => setLoading(false))
  useEffect(() => { loadFitness() }, [])

  const act = async (label, fn) => {
    setBusy(label)
    try {
      const r = await fn()
      setLog(l => [{ label, result: r }, ...l.slice(0, 9)])
      loadFitness()
    } catch (e) {
      setLog(l => [{ label, result: { error: e.message } }, ...l])
    } finally {
      setBusy('')
    }
  }

  const chartData = fitness
    .sort((a, b) => b.fitness - a.fitness)
    .slice(0, 15)
    .map(g => ({ name: g.knowledge.slice(0, 22), fitness: g.fitness, gen: g.generation }))

  if (loading) return <div className="spinner" />

  return (
    <div>
      <h2 style={{ fontSize: 20, marginBottom: 20 }}>🔬 Evolution Engine</h2>

      {/* Actions */}
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 20 }}>
        {[
          ['Mutate', 'mutation', () => api.mutate()],
          ['Crossover', 'crossover', () => api.crossover()],
          ['Prune (0.7)', 'prune', () => api.prune(0.7, 50)],
          ['Cleanup', 'cleanup', () => api.cleanup()],
        ].map(([label, key, fn]) => (
          <button
            key={key}
            className="btn-secondary"
            disabled={!!busy}
            onClick={() => act(label, fn)}
          >
            {busy === label ? <span className="spinner" /> : label}
          </button>
        ))}
      </div>

      {/* Fitness chart */}
      {chartData.length > 0 && (
        <div className="card" style={{ marginBottom: 20 }}>
          <div className="section-title">Fitness Scores (top 15 genes)</div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={chartData} margin={{ top: 4, right: 8, left: -20, bottom: 60 }}>
              <XAxis dataKey="name" tick={{ fontSize: 10, fill: '#64748b' }} angle={-35} textAnchor="end" />
              <YAxis tick={{ fontSize: 10, fill: '#64748b' }} />
              <Tooltip
                contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', fontSize: 12 }}
                labelStyle={{ color: 'var(--text)' }}
              />
              <Bar dataKey="fitness" radius={[3,3,0,0]}>
                {chartData.map((_, i) => (
                  <Cell key={i} fill={i === 0 ? 'var(--accent)' : '#334155'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Gene table */}
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="section-title">All Genes</div>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
            <thead>
              <tr style={{ color: 'var(--muted)', textAlign: 'left' }}>
                {['Knowledge', 'Chromosome', 'Fitness', 'Strength', 'Usage', 'Gen', 'Age'].map(h => (
                  <th key={h} style={{ padding: '6px 10px', borderBottom: '1px solid var(--border)' }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {fitness.sort((a,b) => b.fitness - a.fitness).map((g, i) => (
                <tr key={i} style={{ borderBottom: '1px solid var(--border)' }}>
                  <td style={{ padding: '6px 10px', maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{g.knowledge}</td>
                  <td style={{ padding: '6px 10px' }}><span className="tag">{g.chromosome}</span></td>
                  <td style={{ padding: '6px 10px', color: 'var(--accent)', fontFamily: 'monospace' }}>{g.fitness}</td>
                  <td style={{ padding: '6px 10px', fontFamily: 'monospace' }}>{(g.strength * 100).toFixed(0)}%</td>
                  <td style={{ padding: '6px 10px' }}>{g.usage_count}</td>
                  <td style={{ padding: '6px 10px' }}>{g.generation}</td>
                  <td style={{ padding: '6px 10px' }}>{g.age}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Operation log */}
      {log.length > 0 && (
        <div className="card">
          <div className="section-title">Operation Log</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {log.map((l, i) => (
              <div key={i} style={{ fontSize: 12, borderLeft: '2px solid var(--accent)', paddingLeft: 10 }}>
                <strong>{l.label}</strong>
                <pre style={{ color: 'var(--muted)', marginTop: 2, fontSize: 11, whiteSpace: 'pre-wrap' }}>
                  {JSON.stringify(l.result, null, 2)}
                </pre>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
