import type { PredictionItem } from '../types/api'
import { AlertTriangle } from 'lucide-react'

interface Props {
  predictions: PredictionItem[]
  noVehicle: boolean
  suggestions: string[]
}

function ConfBar({ value }: { value: number }) {
  const pct = Math.round(value * 100)
  const color = pct >= 70 ? 'bg-primary' : pct >= 40 ? 'bg-yellow-400' : 'bg-red-400'
  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 bg-gray-100 rounded-full h-2.5 overflow-hidden">
        <div
          className={`${color} h-2.5 rounded-full transition-all duration-700`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-sm font-semibold w-12 text-right text-gray-700">{pct} %</span>
    </div>
  )
}

export default function ResultCard({ predictions, noVehicle, suggestions }: Props) {
  if (noVehicle || predictions.length === 0) {
    return (
      <div className="card border-l-4 border-accent space-y-3">
        <div className="flex items-center gap-2 text-accent font-semibold">
          <AlertTriangle size={20} />
          No se detectó un vehículo identificable
        </div>
        {suggestions.length > 0 && (
          <ul className="text-sm text-gray-600 space-y-1 list-disc list-inside">
            {suggestions.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        )}
      </div>
    )
  }

  return (
    <div className="card space-y-4">
      <h2 className="font-semibold text-gray-800 text-lg">Resultados del análisis</h2>
      <ul className="space-y-4">
        {predictions.map((p) => (
          <li key={p.rank} className={`space-y-1 ${p.rank === 1 ? '' : 'opacity-70'}`}>
            <div className="flex items-center gap-2">
              {p.rank === 1 && (
                <span className="bg-primary text-white text-xs font-bold px-2 py-0.5 rounded-full">
                  Principal
                </span>
              )}
              <span className={`font-medium ${p.rank === 1 ? 'text-gray-900 text-base' : 'text-gray-600 text-sm'}`}>
                {p.brand} {p.model}
              </span>
            </div>
            <ConfBar value={p.confidence} />
          </li>
        ))}
      </ul>
    </div>
  )
}
