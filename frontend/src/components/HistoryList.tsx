import { Link } from 'react-router-dom'
import { Trash2, ChevronRight, FileVideo, FileImage, AlertCircle } from 'lucide-react'
import type { HistoryItem } from '../types/api'
import { useDeleteHistory } from '../hooks/useAnalyze'

interface Props {
  items: HistoryItem[]
}

function fmtDate(iso: string) {
  return new Date(iso).toLocaleString('es-CO', {
    dateStyle: 'short',
    timeStyle: 'short',
  })
}

function Thumbnail({ b64 }: { b64: string | null }) {
  if (!b64) return <div className="w-14 h-10 bg-gray-100 rounded flex items-center justify-center text-gray-400"><FileImage size={20} /></div>
  return <img src={`data:image/jpeg;base64,${b64}`} className="w-14 h-10 object-cover rounded" alt="miniatura" />
}

export default function HistoryList({ items }: Props) {
  const { mutate: del, isPending } = useDeleteHistory()

  if (items.length === 0) {
    return (
      <div className="card text-center text-gray-500 py-12">
        <AlertCircle size={32} className="mx-auto mb-2 text-gray-300" />
        No hay análisis en el historial todavía.
      </div>
    )
  }

  return (
    <ul className="space-y-2">
      {items.map((item) => (
        <li key={item.analysis_id} className="card flex items-center gap-4 py-3 px-4 hover:shadow-md transition-shadow">
          <Thumbnail b64={item.thumbnail_b64} />

          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              {item.input_type === 'video'
                ? <FileVideo size={14} className="text-gray-400 shrink-0" />
                : <FileImage size={14} className="text-gray-400 shrink-0" />}
              <span className="font-medium text-gray-800 truncate">
                {item.no_vehicle
                  ? 'Sin vehículo identificado'
                  : `${item.top_brand ?? ''} ${item.top_model ?? ''}`}
              </span>
              {!item.no_vehicle && item.top_confidence && (
                <span className="text-xs text-gray-400 shrink-0">
                  {Math.round(item.top_confidence * 100)} %
                </span>
              )}
            </div>
            <p className="text-xs text-gray-400 mt-0.5">{fmtDate(item.created_at)}</p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <Link
              to={`/resultado/${item.analysis_id}`}
              className="p-2 rounded-lg hover:bg-gray-100 text-primary transition-colors"
              title="Ver detalle"
            >
              <ChevronRight size={18} />
            </Link>
            <button
              onClick={() => del(item.analysis_id)}
              disabled={isPending}
              className="p-2 rounded-lg hover:bg-red-50 text-gray-400 hover:text-accent transition-colors disabled:opacity-40"
              title="Eliminar"
            >
              <Trash2 size={16} />
            </button>
          </div>
        </li>
      ))}
    </ul>
  )
}
