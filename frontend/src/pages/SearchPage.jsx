import React, { useState } from 'react'
import { api } from '../api'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [expandedGene, setExpandedGene] = useState(null)

  const search = async () => {
    if (!query.trim()) return
    setLoading(true)
    setResult(null)
    setExpandedGene(null)
    try {
      const r = await api.search(query.trim())
      setResult(r)
    } finally {
      setLoading(false)
    }
  }

  const sourceColor = (src) => src === 'DNA' ? 'badge-green' : 'badge-blue'

  // Extract connection data for visualization
  const activeDnaResults = result?.results.filter(r => r.source === 'DNA') || []
  const topDnaResult = activeDnaResults[0]

  return (
    <div style={{ maxWidth: 800, paddingBottom: 40 }}>
      <h2 style={{ fontSize: 24, fontWeight: 700, marginBottom: 6, display: 'flex', alignItems: 'center', gap: 8 }}>
        🧬 Regulatory Hybrid Search
      </h2>
      <p style={{ color: 'var(--muted)', fontSize: 13, marginBottom: 24 }}>
        Stimulates genes based on query semantics and simulates promoter/repressor signal cascade.
      </p>

      {/* Input panel */}
      <div style={{ display: 'flex', gap: 10, marginBottom: 24 }}>
        <input
          style={{ height: 42, fontSize: 14 }}
          placeholder="Query the knowledge network (e.g., 'GPUs compute deep learning models')…"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && search()}
        />
        <button className="btn-primary" style={{ padding: '0 24px', height: 42, fontSize: 14, display: 'flex', alignItems: 'center', gap: 6 }} onClick={search} disabled={loading}>
          {loading ? <span className="spinner" style={{ width: 16, height: 16 }} /> : 'Stimulate'}
        </button>
      </div>

      {result && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 20 }}>
          
          {/* Signal flow schematic map */}
          {topDnaResult && (
            <div className="card gradient-card glow-border" style={{ padding: 18 }}>
              <div className="section-title" style={{ color: 'var(--accent)', fontSize: 11 }}>⚡ Regulatory Signal Flow Map</div>
              <p style={{ fontSize: 12, color: 'var(--muted)', marginBottom: 16 }}>
                Simulated path for top activated node:
              </p>
              
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 12 }}>
                {/* Step 1: Query Input */}
                <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', padding: '6px 14px', borderRadius: 20, fontSize: 12, color: 'var(--muted)' }}>
                  🔍 Input Query
                </div>
                
                {/* Down Arrow */}
                <div style={{ fontSize: 16, color: 'var(--accent)' }}>↓</div>
                
                {/* Step 2: Top Activated Gene */}
                <div style={{ background: 'rgba(0, 212, 170, 0.15)', border: '1px solid var(--accent)', padding: '10px 16px', borderRadius: 8, textAlign: 'center', width: '100%', maxWidth: 450 }}>
                  <span style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', color: 'var(--accent)', display: 'block', marginBottom: 2 }}>
                    Primary Expression Hub ({(topDnaResult.score * 100).toFixed(1)}%)
                  </span>
                  <span style={{ fontSize: 13, fontWeight: 500 }}>{topDnaResult.text}</span>
                </div>

                {/* Step 3: Connections flow */}
                {(Object.keys(topDnaResult.details?.promoters || {}).length > 0 || Object.keys(topDnaResult.details?.repressors || {}).length > 0) ? (
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, width: '100%', maxWidth: 600, marginTop: 8 }}>
                    
                    {/* Promoter Pathway */}
                    <div>
                      <div style={{ textAlign: 'center', color: 'var(--dna-a)', fontSize: 11, fontWeight: 700, marginBottom: 8 }}>
                        🟩 Promoter Pathways (Up-regulation)
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                        {Object.entries(topDnaResult.details?.promoters || {}).slice(0, 3).map(([target, weight]) => (
                          <div key={target} style={{ background: 'rgba(34, 197, 94, 0.08)', border: '1px solid rgba(34, 197, 94, 0.2)', padding: 8, borderRadius: 6, fontSize: 11 }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--dna-a)', marginBottom: 2 }}>
                              <span>Promotes:</span>
                              <strong>+{weight}</strong>
                            </div>
                            <div style={{ color: 'var(--text)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{target}</div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Repressor Pathway */}
                    <div>
                      <div style={{ textAlign: 'center', color: 'var(--dna-g)', fontSize: 11, fontWeight: 700, marginBottom: 8 }}>
                        🟥 Repressor Pathways (Suppression)
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                        {Object.entries(topDnaResult.details?.repressors || {}).slice(0, 3).map(([target, weight]) => (
                          <div key={target} style={{ background: 'rgba(239, 68, 68, 0.08)', border: '1px solid rgba(239, 68, 68, 0.2)', padding: 8, borderRadius: 6, fontSize: 11 }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--dna-g)', marginBottom: 2 }}>
                              <span>Represses:</span>
                              <strong>-{weight}</strong>
                            </div>
                            <div style={{ color: 'var(--text)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{target}</div>
                          </div>
                        ))}
                      </div>
                    </div>

                  </div>
                ) : (
                  <p style={{ fontSize: 11, color: 'var(--muted)', fontStyle: 'italic', marginTop: 4 }}>
                    No feedback loops established yet. Reinforce search or evolve network to generate pathways.
                  </p>
                )}
              </div>
            </div>
          )}

          {/* Results List */}
          <div>
            <div style={{ marginBottom: 14, fontSize: 12, color: 'var(--muted)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                Chromosome activated: <span className="tag" style={{ background: 'rgba(124, 58, 237, 0.2)', color: '#c4b5fd', border: '1px solid rgba(124, 58, 237, 0.4)' }}>{result.chromosome}</span>
              </div>
              <div>{result.results.length} active genes retrieved</div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {result.results.map((r, i) => {
                const isDna = r.source === 'DNA'
                const expr = isDna ? (r.details?.expression || 0) : 0
                const scorePercent = (r.score * 100).toFixed(1)
                const isExpanded = expandedGene === i

                return (
                  <div key={i} className="card" style={{
                    borderLeft: `3px solid ${i === 0 ? 'var(--accent)' : 'var(--border)'}`,
                    transition: 'transform 0.2s',
                  }}>
                    {/* Header */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <span className={`badge ${sourceColor(r.source)}`}>{r.source}</span>
                        {isDna && (
                          <span style={{ fontSize: 11, color: 'var(--muted)' }}>
                            Gen {r.details?.generation || 0}
                          </span>
                        )}
                      </div>
                      <span style={{ fontFamily: 'monospace', fontSize: 13, fontWeight: 700, color: 'var(--accent)' }}>
                        {scorePercent}% Activation
                      </span>
                    </div>

                    {/* Text */}
                    <div style={{ fontSize: 14, fontWeight: 500, marginBottom: 12, color: 'var(--text)' }}>
                      {r.text}
                    </div>

                    {/* Dynamic Expression / Importance Slider meter */}
                    {isDna ? (
                      <div style={{ marginBottom: 12 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--muted)', marginBottom: 4 }}>
                          <span>Dynamic Expression Level</span>
                          <strong>{(expr * 100).toFixed(1)}%</strong>
                        </div>
                        <div style={{ height: 6, background: 'var(--border)', borderRadius: 3, overflow: 'hidden', display: 'flex' }}>
                          <div style={{
                            width: `${expr * 100}%`,
                            background: expr > 0.6 ? 'var(--dna-a)' : expr > 0.3 ? 'var(--dna-c)' : 'var(--muted)',
                            transition: 'width 0.4s'
                          }} />
                        </div>
                      </div>
                    ) : (
                      <div style={{ marginBottom: 12 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: 'var(--muted)', marginBottom: 4 }}>
                          <span>Neural Importance</span>
                          <strong>{((r.details?.importance || 0.5) * 100).toFixed(1)}%</strong>
                        </div>
                        <div style={{ height: 6, background: 'var(--border)', borderRadius: 3, overflow: 'hidden' }}>
                          <div style={{ width: `${(r.details?.importance || 0.5) * 100}%`, background: 'var(--dna-t)', height: '100%' }} />
                        </div>
                      </div>
                    )}

                    {/* Dynamic DNA connectivity Details Accordion */}
                    {isDna && (
                      <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: 11, color: 'var(--muted)', borderTop: '1px solid var(--border)', paddingTop: 10 }}>
                          <span>Base Expression: {r.details?.base_expression || 0.1} | Total Usage: {r.details?.usage_count || 0}</span>
                          <button 
                            className="btn-secondary" 
                            style={{ padding: '3px 8px', fontSize: 10 }}
                            onClick={() => setExpandedGene(isExpanded ? null : i)}
                          >
                            {isExpanded ? 'Hide Network Connections' : 'View Network Connections'}
                          </button>
                        </div>

                        {isExpanded && (
                          <div style={{ marginTop: 12, padding: 10, background: 'var(--bg)', borderRadius: 6, border: '1px solid var(--border)' }}>
                            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                              {/* Promoters */}
                              <div>
                                <div style={{ fontSize: 10, fontWeight: 700, color: 'var(--dna-a)', marginBottom: 4 }}>🟩 Promoted By:</div>
                                {Object.keys(r.details?.promoters || {}).length > 0 ? (
                                  Object.entries(r.details?.promoters || {}).map(([target, weight]) => (
                                    <div key={target} style={{ fontSize: 11, margin: '2px 0', display: 'flex', justifyContent: 'space-between' }}>
                                      <span style={{ color: 'var(--muted)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: 130 }} title={target}>
                                        {target}
                                      </span>
                                      <span style={{ color: 'var(--dna-a)', fontWeight: 'bold' }}>+{weight}</span>
                                    </div>
                                  ))
                                ) : (
                                  <span style={{ fontSize: 10, color: 'var(--muted)', fontStyle: 'italic' }}>No promoters</span>
                                )}
                              </div>

                              {/* Repressors */}
                              <div>
                                <div style={{ fontSize: 10, fontWeight: 700, color: 'var(--dna-g)', marginBottom: 4 }}>🟥 Repressed By:</div>
                                {Object.keys(r.details?.repressors || {}).length > 0 ? (
                                  Object.entries(r.details?.repressors || {}).map(([target, weight]) => (
                                    <div key={target} style={{ fontSize: 11, margin: '2px 0', display: 'flex', justifyContent: 'space-between' }}>
                                      <span style={{ color: 'var(--muted)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: 130 }} title={target}>
                                        {target}
                                      </span>
                                      <span style={{ color: 'var(--dna-g)', fontWeight: 'bold' }}>-{weight}</span>
                                    </div>
                                  ))
                                ) : (
                                  <span style={{ fontSize: 10, color: 'var(--muted)', fontStyle: 'italic' }}>No repressors</span>
                                )}
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {i === 0 && (
                      <div style={{ fontSize: 11, color: 'var(--accent)', marginTop: 8, borderTop: isDna ? 'none' : '1px solid var(--border)', paddingTop: isDna ? 0 : 8 }}>
                        ⚡ Top Expressed Node — Reinforced & connection pathways updated
                      </div>
                    )}
                  </div>
                )
              })}

              {result.results.length === 0 && (
                <div style={{ color: 'var(--muted)', textAlign: 'center', padding: '40px 0' }}>
                  No active genes stimulated. Add and consolidate memories first.
                </div>
              )}
            </div>
          </div>

        </div>
      )}
    </div>
  )
}

