const BASE = import.meta.env.VITE_API_URL || '/api'

async function req(method, path, body) {
  const res = await fetch(BASE + path, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export const api = {
  stats: () => req('GET', '/stats'),
  // memory
  addMemory: (text) => req('POST', '/memory/add', { text }),
  getNeuralMemory: () => req('GET', '/memory/neural'),
  getDNAMemory: () => req('GET', '/memory/dna'),
  consolidate: () => req('POST', '/memory/consolidate'),
  // search
  search: (query) => req('POST', '/search', { query }),
  // evolution
  getFitness: () => req('GET', '/evolution/fitness'),
  getSelected: () => req('GET', '/evolution/selected'),
  mutate: () => req('POST', '/evolution/mutate'),
  crossover: () => req('POST', '/evolution/crossover'),
  prune: (threshold, max_population) =>
    req('POST', '/evolution/prune', { threshold, max_population }),
  cleanup: () => req('POST', '/evolution/cleanup'),
  // attention
  getAttention: () => req('GET', '/attention'),
  // graph
  getGraph: () => req('GET', '/graph'),
  graphSearch: (node, depth) => req('POST', '/graph/search', { node, depth }),
  runInference: () => req('POST', '/graph/infer'),
  getInferences: () => req('GET', '/graph/inferences'),
  // concepts
  buildConcepts: () => req('POST', '/concepts/build'),
  discoverConcepts: (n) => req('POST', `/concepts/discover?n_clusters=${n}`),
  getConcepts: () => req('GET', '/concepts'),
  // learning
  getExperiences: () => req('GET', '/learning/experiences'),
  getLearningSummary: () => req('GET', '/learning/summary'),
  getPolicy: () => req('GET', '/learning/policy'),
}
