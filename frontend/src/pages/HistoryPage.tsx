import { History } from 'lucide-react'
import { useHistory } from '../hooks/useAnalyze'
import HistoryList from '../components/HistoryList'

export default function HistoryPage() {
  const { data, isLoading, error } = useHistory(10, 0)

  return (
    <div className="max-w-2xl mx-auto space-y-5">
      <div className="flex items-center gap-2">
        <History size={22} className="text-primary" />
        <h1 className="text-xl font-bold text-gray-800">Historial</h1>
        {data && (
          <span className="ml-auto text-xs text-gray-400">{data.total} análisis en total</span>
        )}
      </div>

      {isLoading && (
        <div className="text-center py-12 text-gray-400 text-sm">Cargando historial…</div>
      )}

      {error && (
        <div className="card border-l-4 border-accent text-accent text-sm p-4">
          {(error as Error).message}
        </div>
      )}

      {data && <HistoryList items={data.items} />}
    </div>
  )
}
