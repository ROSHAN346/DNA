import React, { useEffect, useState, useCallback } from 'react'
import ReactFlow, { Background, Controls, MiniMap, useNodesState, useEdgesState } from 'reactflow'
import 'reactflow/dist/style.css'
import { api } from '../api'

function buildFlow(graphData) {
  const nodes = []
  const edges = []
  const seen = new Set()

  const addNode = (id) => {
    if (seen.has(id)) return
    seen.add(id)
    nodes.push({
      id,
      data: { label: id },
      position: {
        x: Math.random() * 600,
        y: Math.random() * 400,
      },
      style: {
        background: '#1f2d3d',
        color: '#e2e8f0',
        border: '1px solid #00d4aa',
        borderRadius: 8,
        fontSize: 11,
        padding: '4px 10px',
      },
    })
  }

  Object.entries(graphData).forEach(([source, rels]) => {
    addNode(source)
    rels.forEach(({ target, relation }, i) => {
      addNode(target)
      edges.push({
        id: `${source}-${target}-${i}`,
        source,
        target,
        label: relation,
        style: { stroke: '#334155' },
        labelStyle: { fontSize: 9, fill: '#94a3b8' },
        labelBgStyle: { fill: '#111827' },
      })
    })
  })

  return { nodes, edges }
}

export default function GraphPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [inferences, setInferences] = useState([])
  const [searchNode, setSearchNode] = useState('')
  const [searchResult, setSearchResult] = useState([])
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState('')

  const loadGraph = useCallback(() => {
    api.getGraph().then(data => {
      const { nodes: n, edges: e } = buildFlow(data)
      setNodes(n)
      setEdges(e)
    }).finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    loadGraph()
    api.getInferences().then(setInferences)
  }, [])

  const runInfer = async () => {
    setBusy('infer')
    const r = await api.runInference()
    setInferences(r)
    setBusy('')
  }

  const graphSearch = async () => {
    if (!searchNode.trim()) return
    setBusy('search')
    const r = await api.graphSearch(searchNode.trim(), 3)
    setSearchResult(r)
    setBusy('')
  }

  if (loading) return <div className="spinner" />

  return (
    <div>
      <h2 style={{ fontSize: 20, marginBottom: 20 }}>🕸 Knowledge Graph</h2>

      {/* ReactFlow canvas */}
      <div style={{ height: 380, borderRadius: 10, overflow: 'hidden', border: '1px solid var(--border)', marginBottom: 20 }}>
        {nodes.length === 0
          ? <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--muted)' }}>
              No graph nodes yet. Add memories and consolidate.
            </div>
          : <ReactFlow
              nodes={nodes} edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              fitView
            >
              <Background color="#1f2d3d" gap={16} />
              <Controls style={{ background: 'var(--surface)', border: '1px solid var(--border)' }} />
              <MiniMap style={{ background: 'var(--surface)' }} nodeColor="#00d4aa" />
            </ReactFlow>
        }
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
        {/* Graph search */}
        <div className="card">
          <div className="section-title">Traverse from Node</div>
          <div style={{ display: 'flex', gap: 8, marginBottom: 10 }}>
            <input placeholder="Node name…" value={searchNode} onChange={e => setSearchNode(e.target.value)} />
            <button className="btn-secondary" onClick={graphSearch} disabled={!!busy}>Go</button>
          </div>
          <div style={{ maxHeight: 160, overflowY: 'auto', fontSize: 12 }}>
            {searchResult.map((r, i) => (
              <div key={i} style={{ borderBottom: '1px solid var(--border)', padding: '4px 0', color: 'var(--muted)' }}>
                <span style={{ color: 'var(--text)' }}>{r.source}</span>
                <span style={{ color: 'var(--accent)', margin: '0 6px' }}>—{r.relation}→</span>
                <span style={{ color: 'var(--text)' }}>{r.target}</span>
                <span style={{ marginLeft: 6 }}>(depth {r.depth})</span>
              </div>
            ))}
          </div>
        </div>

        {/* Inferences */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <div className="section-title" style={{ marginBottom: 0 }}>Transitive Inferences</div>
            <button className="btn-secondary" onClick={runInfer} disabled={!!busy} style={{ fontSize: 11, padding: '4px 10px' }}>
              Run
            </button>
          </div>
          <div style={{ maxHeight: 160, overflowY: 'auto', fontSize: 12 }}>
            {inferences.slice(0, 30).map((inf, i) => (
              <div key={i} style={{ borderBottom: '1px solid var(--border)', padding: '4px 0', color: 'var(--muted)' }}>
                <span style={{ color: 'var(--text)' }}>{inf.from}</span>
                <span style={{ color: '#a78bfa', margin: '0 4px' }}>→{inf.through}→</span>
                <span style={{ color: 'var(--text)' }}>{inf.to}</span>
              </div>
            ))}
            {inferences.length === 0 && <span style={{ color: 'var(--muted)' }}>No inferences yet.</span>}
          </div>
        </div>
      </div>
    </div>
  )
}
