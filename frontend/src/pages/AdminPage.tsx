import { useState } from 'react'
import { LayoutDashboard, Lock, ExternalLink } from 'lucide-react'
import { useStats } from '../hooks/useAnalyze'
import StatsChart from '../components/StatsChart'

export default function AdminPage() {
  const [key, setKey] = useState('')
  const [submitted, setSubmitted] = useState('')
  const { data, isLoading, error } = useStats(submitted)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitted(key)
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center gap-2">
        <LayoutDashboard size={22} className="text-primary" />
        <h1 className="text-xl font-bold text-gray-800">Panel administrativo</h1>
      </div>

      {!submitted && (
        <div className="card max-w-sm">
          <div className="flex items-center gap-2 text-gray-700 font-semibold mb-4">
            <Lock size={16} /> Acceso restringido
          </div>
          <form onSubmit={handleSubmit} className="space-y-3">
            <input
              type="password"
              value={key}
              onChange={(e) => setKey(e.target.value)}
              placeholder="X-Admin-Key"
              className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
            />
            <button type="submit" className="btn-primary w-full text-sm">
              Ingresar
            </button>
          </form>
        </div>
      )}

      {submitted && isLoading && (
        <p className="text-gray-400 text-sm">Cargando estadísticas…</p>
      )}

      {error && (
        <div className="card border-l-4 border-accent text-accent text-sm p-4">
          {(error as Error).message}
          <button
            onClick={() => setSubmitted('')}
            className="ml-4 underline text-xs"
          >
            Reintentar
          </button>
        </div>
      )}

      {data && (
        <>
          <StatsChart stats={data} />
          <div className="card flex items-center justify-between py-3">
            <span className="text-sm text-gray-600">Reporte de métricas del modelo (Grad-CAM, F1, matriz)</span>
            <a
              href="/api/v1/admin/metrics"
              target="_blank"
              rel="noreferrer"
              className="btn-ghost text-sm py-1.5 flex items-center gap-1.5"
            >
              <ExternalLink size={14} /> Descargar
            </a>
          </div>
        </>
      )}
    </div>
  )
}
