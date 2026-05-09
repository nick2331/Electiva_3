import { useState } from 'react'
import {
  LayoutDashboard, Lock, ExternalLink, RefreshCw,
  Database, Cpu, HardDrive, Activity, Server, Zap,
  CheckCircle, AlertTriangle, XCircle, Terminal, Play,
} from 'lucide-react'
import { useStats } from '../hooks/useAnalyze'
import StatsChart from '../components/StatsChart'
import client from '../api/client'

// ─── Types ───────────────────────────────────────────────────────────────────

interface ServiceStatus { status: 'ok' | 'warning' | 'error'; message: string }
interface HealthData {
  uptime_seconds: number
  database: ServiceStatus
  model: ServiceStatus
  memory: ServiceStatus
  memory_used_mb: number
  memory_total_mb: number
  memory_percent: number
  cpu_percent: number
  disk_used_mb: number
  disk_total_mb: number
  disk_percent: number
}
interface QueryResult { columns: string[]; rows: unknown[][]; row_count: number; message: string }

// ─── Helpers ─────────────────────────────────────────────────────────────────

function fmtUptime(s: number) {
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = s % 60
  return `${h}h ${m}m ${sec}s`
}

function StatusIcon({ status }: { status: 'ok' | 'warning' | 'error' }) {
  if (status === 'ok')      return <CheckCircle size={16} className="text-green-500 shrink-0" />
  if (status === 'warning') return <AlertTriangle size={16} className="text-yellow-500 shrink-0" />
  return <XCircle size={16} className="text-red-500 shrink-0" />
}

function GaugeBar({ value, color }: { value: number; color: string }) {
  return (
    <div className="w-full bg-gray-100 rounded-full h-2 mt-1">
      <div className={`${color} h-2 rounded-full transition-all`} style={{ width: `${Math.min(value, 100)}%` }} />
    </div>
  )
}

const QUICK_QUERIES = [
  { label: 'Últimos 10 análisis', sql: 'SELECT id, input_type, no_vehicle, created_at FROM analyses ORDER BY created_at DESC LIMIT 10' },
  { label: 'Total por tipo',      sql: 'SELECT input_type, COUNT(*) as total FROM analyses GROUP BY input_type' },
  { label: 'Modelos top 5',       sql: "SELECT predictions->0->>'brand' AS brand, predictions->0->>'model' AS model, COUNT(*) AS total FROM analyses WHERE no_vehicle = false GROUP BY 1,2 ORDER BY 3 DESC LIMIT 5" },
  { label: 'Todas las tablas',    sql: "SELECT name FROM sqlite_master WHERE type='table'" },
]

// ─── Component ───────────────────────────────────────────────────────────────

export default function AdminPage() {
  const [key, setKey]           = useState('')
  const [adminKey, setAdminKey] = useState('')
  const [health, setHealth]     = useState<HealthData | null>(null)
  const [healthErr, setHealthErr] = useState('')
  const [healthLoading, setHealthLoading] = useState(false)
  const [sql, setSql]           = useState('')
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null)
  const [queryErr, setQueryErr] = useState('')
  const [queryLoading, setQueryLoading] = useState(false)

  const { data: stats, isLoading: statsLoading, error: statsErr, refetch } = useStats(adminKey)

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    setAdminKey(key)
  }

  const loadHealth = async () => {
    setHealthLoading(true)
    setHealthErr('')
    try {
      const { data } = await client.get<HealthData>('/admin/health', {
        headers: { 'X-Admin-Key': adminKey },
      })
      setHealth(data)
    } catch (err) {
      setHealthErr((err as Error).message)
    } finally {
      setHealthLoading(false)
    }
  }

  const runQuery = async () => {
    if (!sql.trim()) return
    setQueryLoading(true)
    setQueryErr('')
    setQueryResult(null)
    try {
      const { data } = await client.post<QueryResult>('/admin/db/query', { sql }, {
        headers: { 'X-Admin-Key': adminKey },
      })
      setQueryResult(data)
    } catch (err) {
      setQueryErr((err as Error).message)
    } finally {
      setQueryLoading(false)
    }
  }

  // ── Login ──
  if (!adminKey) {
    return (
      <div className="max-w-sm mx-auto mt-16 card">
        <div className="flex items-center gap-2 font-semibold text-gray-800 mb-5">
          <Lock size={18} className="text-primary" /> Acceso restringido
        </div>
        <form onSubmit={handleLogin} className="space-y-3">
          <input
            type="password"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            placeholder="X-Admin-Key"
            className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/40"
          />
          <button type="submit" className="btn-primary w-full">Ingresar</button>
        </form>
      </div>
    )
  }

  // ── Dashboard ──
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <LayoutDashboard size={22} className="text-primary" />
          <h1 className="text-xl font-bold text-gray-800">Panel administrativo</h1>
        </div>
        <button onClick={() => refetch()} className="btn-ghost text-sm py-1.5 flex items-center gap-1.5">
          <RefreshCw size={14} /> Actualizar stats
        </button>
      </div>

      {/* ── Estadísticas de uso ── */}
      {statsLoading && <p className="text-sm text-gray-400">Cargando estadísticas…</p>}
      {statsErr && <div className="card border-l-4 border-accent text-accent text-sm p-3">{(statsErr as Error).message}</div>}
      {stats && <StatsChart stats={stats} />}

      {/* ── Estado del sistema ── */}
      <div className="card space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="font-semibold text-gray-800 flex items-center gap-2">
            <Activity size={18} className="text-primary" /> Estado del sistema
          </h2>
          <button
            onClick={loadHealth}
            disabled={healthLoading}
            className="btn-ghost text-sm py-1.5 flex items-center gap-1.5"
          >
            <RefreshCw size={14} className={healthLoading ? 'animate-spin' : ''} />
            {health ? 'Actualizar' : 'Verificar'}
          </button>
        </div>

        {healthErr && <p className="text-accent text-sm">{healthErr}</p>}

        {health && (
          <div className="space-y-4">
            {/* Uptime */}
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Zap size={14} className="text-primary" />
              <span>Uptime del servidor:</span>
              <span className="font-medium text-gray-900">{fmtUptime(health.uptime_seconds)}</span>
            </div>

            {/* Cards de servicios */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {/* DB */}
              <div className="bg-gray-50 rounded-lg p-3 space-y-1">
                <div className="flex items-center gap-2 font-medium text-sm">
                  <Database size={15} className="text-primary" /> Base de datos
                  <StatusIcon status={health.database.status} />
                </div>
                <p className="text-xs text-gray-500">{health.database.message}</p>
              </div>

              {/* Modelo */}
              <div className="bg-gray-50 rounded-lg p-3 space-y-1">
                <div className="flex items-center gap-2 font-medium text-sm">
                  <Server size={15} className="text-primary" /> Modelo IA
                  <StatusIcon status={health.model.status} />
                </div>
                <p className="text-xs text-gray-500">{health.model.message}</p>
              </div>
            </div>

            {/* Métricas de recursos */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {/* RAM */}
              <div className="bg-gray-50 rounded-lg p-3">
                <div className="flex items-center justify-between text-sm font-medium mb-1">
                  <span className="flex items-center gap-1"><Cpu size={13} /> RAM</span>
                  <StatusIcon status={health.memory.status} />
                </div>
                <p className="text-xs text-gray-500">
                  {health.memory_used_mb.toFixed(0)} / {health.memory_total_mb.toFixed(0)} MB
                </p>
                <GaugeBar
                  value={health.memory_percent}
                  color={health.memory_percent > 90 ? 'bg-red-400' : health.memory_percent > 75 ? 'bg-yellow-400' : 'bg-primary'}
                />
                <p className="text-xs text-gray-400 mt-1">{health.memory_percent} %</p>
              </div>

              {/* CPU */}
              <div className="bg-gray-50 rounded-lg p-3">
                <div className="flex items-center justify-between text-sm font-medium mb-1">
                  <span className="flex items-center gap-1"><Activity size={13} /> CPU</span>
                </div>
                <p className="text-xs text-gray-500">Uso actual</p>
                <GaugeBar
                  value={health.cpu_percent}
                  color={health.cpu_percent > 80 ? 'bg-red-400' : 'bg-primary'}
                />
                <p className="text-xs text-gray-400 mt-1">{health.cpu_percent} %</p>
              </div>

              {/* Disco */}
              <div className="bg-gray-50 rounded-lg p-3">
                <div className="flex items-center justify-between text-sm font-medium mb-1">
                  <span className="flex items-center gap-1"><HardDrive size={13} /> Disco</span>
                </div>
                <p className="text-xs text-gray-500">
                  {health.disk_used_mb.toFixed(0)} / {health.disk_total_mb.toFixed(0)} MB
                </p>
                <GaugeBar
                  value={health.disk_percent}
                  color={health.disk_percent > 90 ? 'bg-red-400' : 'bg-primary'}
                />
                <p className="text-xs text-gray-400 mt-1">{health.disk_percent} %</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* ── Consola SQL ── */}
      <div className="card space-y-3">
        <h2 className="font-semibold text-gray-800 flex items-center gap-2">
          <Terminal size={18} className="text-primary" /> Consola de base de datos
        </h2>
        <p className="text-xs text-gray-400">Solo se permiten consultas SELECT / PRAGMA / EXPLAIN. Máximo 200 filas.</p>

        {/* Queries rápidas */}
        <div className="flex flex-wrap gap-2">
          {QUICK_QUERIES.map((q) => (
            <button
              key={q.label}
              onClick={() => setSql(q.sql)}
              className="text-xs px-2.5 py-1 bg-gray-100 hover:bg-primary hover:text-white rounded-full transition-colors"
            >
              {q.label}
            </button>
          ))}
        </div>

        <textarea
          value={sql}
          onChange={(e) => setSql(e.target.value)}
          rows={4}
          placeholder="SELECT * FROM analyses LIMIT 10;"
          className="w-full font-mono text-sm border border-gray-200 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-primary/40 resize-y bg-gray-50"
          onKeyDown={(e) => { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) runQuery() }}
        />

        <button
          onClick={runQuery}
          disabled={queryLoading || !sql.trim()}
          className="btn-primary flex items-center gap-2 text-sm"
        >
          <Play size={14} />
          {queryLoading ? 'Ejecutando…' : 'Ejecutar  (Ctrl+Enter)'}
        </button>

        {queryErr && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-accent text-sm">
            {queryErr}
          </div>
        )}

        {queryResult && (
          <div className="space-y-2">
            <p className="text-xs text-gray-500">{queryResult.message}</p>
            <div className="overflow-x-auto rounded-lg border border-gray-100">
              <table className="w-full text-xs">
                <thead>
                  <tr className="bg-primary text-white">
                    {queryResult.columns.map((c) => (
                      <th key={c} className="px-3 py-2 text-left font-medium whitespace-nowrap">{c}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {queryResult.rows.map((row, i) => (
                    <tr key={i} className={i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                      {row.map((cell, j) => (
                        <td key={j} className="px-3 py-1.5 text-gray-700 whitespace-nowrap max-w-xs truncate">
                          {cell === null ? <span className="text-gray-300 italic">null</span> : String(cell)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* ── API docs + métricas ── */}
      <div className="card flex flex-wrap gap-3 items-center justify-between py-3">
        <span className="text-sm text-gray-600 font-medium">Recursos del sistema</span>
        <div className="flex gap-2 flex-wrap">
          <a
            href="https://vehicleye-api.onrender.com/docs"
            target="_blank"
            rel="noreferrer"
            className="btn-ghost text-sm py-1.5 flex items-center gap-1.5"
          >
            <ExternalLink size={14} /> Documentación API
          </a>
          <a
            href="https://vehicleye-api.onrender.com/health"
            target="_blank"
            rel="noreferrer"
            className="btn-ghost text-sm py-1.5 flex items-center gap-1.5"
          >
            <Activity size={14} /> Health check
          </a>
          <a
            href="/api/v1/admin/metrics"
            target="_blank"
            rel="noreferrer"
            className="btn-primary text-sm py-1.5 flex items-center gap-1.5"
          >
            <ExternalLink size={14} /> Métricas del modelo
          </a>
        </div>
      </div>
    </div>
  )
}
