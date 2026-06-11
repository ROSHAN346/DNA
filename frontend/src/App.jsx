import React, { useState } from 'react'
import Dashboard from './pages/Dashboard'
import DNAViewer from './pages/DNAViewer'
import SearchPage from './pages/SearchPage'
import EvolutionPage from './pages/EvolutionPage'
import GraphPage from './pages/GraphPage'
import AttentionPage from './pages/AttentionPage'
import ConceptsPage from './pages/ConceptsPage'
import LearningPage from './pages/LearningPage'

const NAV = [
  { id: 'dashboard',  label: 'Dashboard',   icon: '⬡' },
  { id: 'dna',        label: 'DNA Viewer',   icon: '🧬' },
  { id: 'search',     label: 'Search',       icon: '🔍' },
  { id: 'evolution',  label: 'Evolution',    icon: '🔬' },
  { id: 'graph',      label: 'Graph',        icon: '🕸' },
  { id: 'attention',  label: 'Attention',    icon: '⚡' },
  { id: 'concepts',   label: 'Concepts',     icon: '💡' },
  { id: 'learning',   label: 'Learning',     icon: '📚' },
]

const PAGES = {
  dashboard: Dashboard,
  dna: DNAViewer,
  search: SearchPage,
  evolution: EvolutionPage,
  graph: GraphPage,
  attention: AttentionPage,
  concepts: ConceptsPage,
  learning: LearningPage,
}

export default function App() {
  const [page, setPage] = useState('dashboard')
  const Page = PAGES[page]

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      {/* Sidebar */}
      <aside style={{
        width: 210, flexShrink: 0,
        background: 'var(--surface)',
        borderRight: '1px solid var(--border)',
        display: 'flex', flexDirection: 'column',
      }}>
        {/* Logo */}
        <div style={{
          padding: '18px 16px 16px',
          borderBottom: '1px solid var(--border)',
          display: 'flex', alignItems: 'center', gap: 10,
        }}>
          <div style={{
            width: 32, height: 32, borderRadius: 8,
            background: 'linear-gradient(135deg, #00d4aa 0%, #7c3aed 100%)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 16, flexShrink: 0,
          }}>🧬</div>
          <div>
            <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--accent)', letterSpacing: '.05em', lineHeight: 1.2 }}>
              DNA MIMIC
            </div>
            <div style={{ fontSize: 10, color: 'var(--muted)', marginTop: 1 }}>
              Cognitive AI Framework
            </div>
          </div>
        </div>

        {/* Nav */}
        <nav style={{ flex: 1, padding: '10px 8px', display: 'flex', flexDirection: 'column', gap: 1, overflowY: 'auto' }}>
          {NAV.map(n => {
            const active = page === n.id
            return (
              <button
                key={n.id}
                onClick={() => setPage(n.id)}
                style={{
                  textAlign: 'left',
                  background: active ? 'rgba(0,212,170,.1)' : 'transparent',
                  color: active ? 'var(--accent)' : 'var(--text)',
                  border: 'none',
                  borderRadius: 6,
                  padding: '8px 10px',
                  fontSize: 13,
                  fontWeight: active ? 600 : 400,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  position: 'relative',
                  transition: 'background .15s, color .15s',
                }}
              >
                {active && (
                  <span style={{
                    position: 'absolute', left: 0, top: '20%', bottom: '20%',
                    width: 3, borderRadius: 2,
                    background: 'var(--accent)',
                  }} />
                )}
                <span style={{ fontSize: 14, lineHeight: 1 }}>{n.icon}</span>
                <span>{n.label}</span>
              </button>
            )
          })}
        </nav>

        <div style={{
          padding: '10px 16px',
          borderTop: '1px solid var(--border)',
          fontSize: 10, color: 'var(--muted)',
        }}>
          v1.0
        </div>
      </aside>

      {/* Main */}
      <main style={{ flex: 1, overflow: 'auto', padding: 28, background: 'var(--bg)' }}>
        <Page />
      </main>
    </div>
  )
}
