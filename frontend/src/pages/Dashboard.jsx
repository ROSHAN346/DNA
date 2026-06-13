import React, { useEffect, useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
} from 'recharts'
import {
  Dna, Brain, Share2, Lightbulb, GitBranch, Zap,
  PlusCircle, RefreshCw, Activity, TrendingUp, Trash2,
} from 'lucide-react'
import { api } from '../api'

const STAT_CONFIG = [
  { key: 'genes',          label: 'DNA Genes',       Icon: Dna,       color: '#00d4aa', bg: 'rgba(0,212,170,.1)'  },
  { key: 'neural_memories',label: 'Neural Memories', Icon: Brain,     color: '#3b82f6', bg: 'rgba(59,130,246,.1)' },
  { key: 'graph_nodes',    label: 'Graph Nodes',     Icon: Share2,    color: '#f59e0b', bg: 'rgba(245,158,11,.1)' },
  { key: 'experiences',    label: 'Experiences',     Icon: Activity,  color: '#a78bfa', bg: 'rgba(167,139,250,.1)' },
  { key: 'concepts',       label: 'Concepts',        Icon: Lightbulb, color: '#34d399', bg: 'rgba(52,211,153,.1)'  },
  { key: 'inferences',     label: 'Inferences',      Icon: GitBranch, color: '#f472b6', bg: 'rgba(244,114,182,.1)' },
]

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: '#1a2235', border: '1px solid #1f2d3d',
      borderRadius: 8, padding: '8px 12px', fontSize: 12,
    }}>
      <div style={{ color: '#94a3b8', marginBottom: 2 }}>{label}</div>
      <div style={{ color: '#00d4aa', fontWeight: 700 }}>{payload[0].value} genes</div>
    </div>
  )
}

function StatCard({ label, value, Icon, color, bg }) {
  return (
    <div className="stat-card" style={{ '--card-accent': color }}>
      <div className="stat-icon" style={{ background: bg, color }}>
        <Icon size={18} />
      </div>
      <div className="stat-body">
        <div className="stat-value" style={{ color }}>{value ?? '—'}</div>
        <div className="stat-label">{label}</div>
      </div>
    </div>
  )
}

function ActivityItem({ icon, text, time, type = 'info' }) {
  const colors = { info: '#00d4aa', success: '#34d399', warn: '#f59e0b', error: '#ef4444' }
  return (
    <div style={{ display: 'flex', gap: 10, alignItems: 'flex-start', padding: '8px 0', borderBottom: '1px solid #1a2235' }}>
      <div style={{ color: colors[type], marginTop: 1, flexShrink: 0 }}>{icon}</div>
      <div style={{ flex: 1, fontSize: 12, color: '#cbd5e1' }}>{text}</div>
      {time && <div style={{ fontSize: 11, color: '#475569', flexShrink: 0 }}>{time}</div>}
    </div>
  )
}

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [text, setText] = useState('')
  const [msg, setMsg] = useState(null)   // { text, type }
  const [activity, setActivity] = useState([])
  const [refreshing, setRefreshing] = useState(false)

  const pushActivity = (text, type = 'info') => {
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    setActivity(prev => [{ text, type, time }, ...prev].slice(0, 8))
  }

  const load = async (showRefresh = false) => {
    if (showRefresh) setRefreshing(true)
    try {
      const s = await api.stats()
      setStats(s)
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  useEffect(() => { load() }, [])

  const addMemory = async () => {
    if (!text.trim()) return
    setMsg(null)
    await api.addMemory(text.trim())
    pushActivity(`Memory stored: "${text.slice(0, 60)}${text.length > 60 ? '…' : ''}"`, 'success')
    setText('')
    setMsg({ text: '✓ Stored in neural buffer', type: 'success' })
    load()
  }

  const consolidate = async () => {
    setMsg({ text: 'Consolidating…', type: 'info' })
    const r = await api.consolidate()
    const msg = `Consolidation done — ${r.genes} genes in DNA`
    setMsg({ text: '✓ ' + msg, type: 'success' })
    pushActivity(msg, 'success')
    load()
  }

  const clearAllData = async () => {
    if (!window.confirm("Are you sure you want to clear all DNA and memory data? This will completely reset the brain state and cannot be undone.")) {
      return
    }
    setMsg({ text: 'Clearing memory…', type: 'info' })
    try {
      await api.clearMemory()
      setMsg({ text: '✓ Brain data completely cleared', type: 'success' })
      pushActivity("Brain and DNA memory cleared completely", "warn")
      load()
    } catch (err) {
      setMsg({ text: 'Error: ' + err.message, type: 'error' })
    }
  }

  // Build chromosome bar chart data
  const chromoData = stats?.chromosome_counts
    ? Object.entries(stats.chromosome_counts)
        .map(([name, count]) => ({ name: name.slice(0, 12), count }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 10)
    : stats?.chromosomes?.map(c => ({ name: c.slice(0, 12), count: 1 })) ?? []

  // Radar data for system health
  const radarData = stats ? [
    { subject: 'Genes',      A: Math.min(100, (stats.genes || 0) * 2) },
    { subject: 'Neural',     A: Math.min(100, (stats.neural_memories || 0) * 5) },
    { subject: 'Graph',      A: Math.min(100, (stats.graph_nodes || 0) * 3) },
    { subject: 'Concepts',   A: Math.min(100, (stats.concepts || 0) * 10) },
    { subject: 'Experience', A: Math.min(100, (stats.experiences || 0) * 4) },
    { subject: 'Inference',  A: Math.min(100, (stats.inferences || 0) * 8) },
  ] : []

  if (loading) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
      <div style={{ textAlign: 'center' }}>
        <div className="spinner" style={{ width: 32, height: 32, margin: '0 auto 12px' }} />
        <div style={{ color: 'var(--muted)', fontSize: 13 }}>Loading brain state…</div>
      </div>
    </div>
  )

  return (
    <div style={{ maxWidth: 1100, margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 24 }}>
        <div>
          <h2 style={{ fontSize: 22, fontWeight: 700, letterSpacing: '-.01em' }}>Brain Overview</h2>
          <p style={{ color: 'var(--muted)', fontSize: 12, marginTop: 2 }}>
            Real-time state of the DNA Mimic cognitive framework
          </p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <button
            className="btn-secondary"
            onClick={() => load(true)}
            style={{ display: 'flex', alignItems: 'center', gap: 6 }}
            disabled={refreshing}
          >
            <RefreshCw size={13} style={{ animation: refreshing ? 'spin .7s linear infinite' : 'none' }} />
            Refresh
          </button>
          <button
            className="btn-danger"
            onClick={clearAllData}
            style={{ display: 'flex', alignItems: 'center', gap: 6 }}
          >
            <Trash2 size={13} />
            Clear All Data
          </button>
        </div>
      </div>

      {/* Stat cards */}
      <div className="stat-grid" style={{ marginBottom: 24 }}>
        {STAT_CONFIG.map(c => (
          <StatCard key={c.key} value={stats?.[c.key]} {...c} />
        ))}
      </div>

      {/* Charts row */}
      <div style={{ display: 'grid', gridTemplateColumns: chromoData.length ? '1fr 280px' : '1fr', gap: 16, marginBottom: 20 }}>

        {/* Chromosome bar chart */}
        {chromoData.length > 0 && (
          <div className="card glow-border">
            <div className="section-title" style={{ marginBottom: 14 }}>
              <TrendingUp size={12} style={{ marginRight: 6, display: 'inline', verticalAlign: 'middle' }} />
              Chromosome Gene Distribution
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={chromoData} barSize={18} margin={{ top: 4, right: 4, left: -20, bottom: 0 }}>
                <XAxis dataKey="name" tick={{ fontSize: 10, fill: '#64748b' }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fontSize: 10, fill: '#64748b' }} axisLine={false} tickLine={false} />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,.04)' }} />
                <Bar dataKey="count" fill="#00d4aa" radius={[4, 4, 0, 0]}
                  background={{ fill: 'rgba(255,255,255,.02)', radius: [4, 4, 0, 0] }} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Radar system health */}
        {radarData.length > 0 && (
          <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div className="section-title" style={{ marginBottom: 6, alignSelf: 'flex-start' }}>
              System Health
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <RadarChart data={radarData} margin={{ top: 10, right: 20, bottom: 10, left: 20 }}>
                <PolarGrid stroke="#1f2d3d" />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 10, fill: '#64748b' }} />
                <Radar dataKey="A" stroke="#00d4aa" fill="#00d4aa" fillOpacity={0.15} strokeWidth={1.5} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Bottom row: Add Memory + Activity */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: 16 }}>

        {/* Add Memory */}
        <div className="card gradient-card">
          <div className="section-title" style={{ marginBottom: 12 }}>
            <PlusCircle size={12} style={{ marginRight: 6, display: 'inline', verticalAlign: 'middle' }} />
            Add Memory
          </div>
          <textarea
            rows={3}
            placeholder="Enter knowledge text to store in neural buffer…"
            value={text}
            onChange={e => setText(e.target.value)}
            style={{ marginBottom: 10, resize: 'vertical', minHeight: 80 }}
          />
          <div style={{ display: 'flex', gap: 8 }}>
            <button
              className="btn-primary"
              onClick={addMemory}
              style={{ display: 'flex', alignItems: 'center', gap: 6 }}
              disabled={!text.trim()}
            >
              <Brain size={13} /> Store Memory
            </button>
            <button
              className="btn-secondary"
              onClick={consolidate}
              style={{ display: 'flex', alignItems: 'center', gap: 6 }}
            >
              <Dna size={13} /> Consolidate → DNA
            </button>
          </div>
          {msg && (
            <div style={{
              marginTop: 10, fontSize: 12, padding: '6px 10px', borderRadius: 6,
              background: msg.type === 'success' ? 'rgba(52,211,153,.1)' : 'rgba(0,212,170,.08)',
              color: msg.type === 'success' ? '#34d399' : 'var(--accent)',
              border: `1px solid ${msg.type === 'success' ? 'rgba(52,211,153,.2)' : 'rgba(0,212,170,.15)'}`,
            }}>
              {msg.text}
            </div>
          )}
        </div>

        {/* Activity log */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column' }}>
          <div className="section-title" style={{ marginBottom: 8 }}>
            <Zap size={12} style={{ marginRight: 6, display: 'inline', verticalAlign: 'middle' }} />
            Activity Log
          </div>
          <div style={{ flex: 1 }}>
            {activity.length === 0 ? (
              <div style={{ color: 'var(--muted)', fontSize: 12, padding: '8px 0' }}>
                No activity yet — add a memory to get started.
              </div>
            ) : (
              activity.map((a, i) => (
                <ActivityItem key={i} icon={<Zap size={12} />} text={a.text} time={a.time} type={a.type} />
              ))
            )}
          </div>

          {/* Chromosomes as tags below */}
          {stats?.chromosomes?.length > 0 && (
            <div style={{ marginTop: 14, paddingTop: 14, borderTop: '1px solid var(--border)' }}>
              <div style={{ fontSize: 11, color: 'var(--muted)', marginBottom: 6, fontWeight: 600, letterSpacing: '.05em', textTransform: 'uppercase' }}>Active Chromosomes</div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                {stats.chromosomes.map(c => <span key={c} className="tag">{c}</span>)}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
