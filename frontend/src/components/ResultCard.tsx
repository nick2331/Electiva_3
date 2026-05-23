import { useState, useEffect } from 'react'
import type { PredictionItem } from '../types/api'
import { AlertTriangle, Trophy, Medal, Award } from 'lucide-react'

interface Props {
  predictions: PredictionItem[]
  noVehicle: boolean
  suggestions: string[]
}

const RANK_ICONS = [Trophy, Medal, Award]
const RANK_COLORS = ['text-yellow-500', 'text-gray-400', 'text-orange-400']
const RANK_BG = ['bg-yellow-50 border-yellow-200', 'bg-gray-50 border-gray-200', 'bg-orange-50 border-orange-200']

function ConfBar({ value, delay = 0 }: { value: number; delay?: number }) {
  const [width, setWidth] = useState(0)
  const pct = Math.round(value * 100)
  const color = pct >= 70 ? 'bg-gradient-to-r from-primary to-primary-light'
               : pct >= 40 ? 'bg-gradient-to-r from-yellow-400 to-orange-400'
               :             'bg-gradient-to-r from-red-400 to-red-500'

  useEffect(() => {
    const t = setTimeout(() => setWidth(pct), delay + 100)
    return () => clearTimeout(t)
  }, [pct, delay])

  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 bg-gray-100 rounded-full h-2.5 overflow-hidden">
        <div
          className={`${color} h-2.5 rounded-full`}
          style={{ width: `${width}%`, transition: 'width 0.8s cubic-bezier(0.34,1.56,0.64,1)' }}
        />
      </div>
      <span className="text-sm font-bold w-12 text-right text-gray-700">{pct} %</span>
    </div>
  )
}

export default function ResultCard({ predictions, noVehicle, suggestions }: Props) {
  if (noVehicle || predictions.length === 0) {
    return (
      <div className="bg-white rounded-2xl border border-red-100 shadow-sm p-5 space-y-3 animate-scaleIn">
        <div className="flex items-center gap-2 text-accent font-semibold">
          <AlertTriangle size={20} />
          No se detectó un vehículo identificable
        </div>
        {suggestions.length > 0 && (
          <ul className="text-sm text-gray-600 space-y-1.5">
            {suggestions.map((s, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-gray-400 mt-1.5 shrink-0" />
                {s}
              </li>
            ))}
          </ul>
        )}
      </div>
    )
  }

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden animate-scaleIn">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-dark to-primary px-5 py-3">
        <h2 className="font-semibold text-white text-base">Resultados del análisis</h2>
      </div>

      <ul className="divide-y divide-gray-50 px-5 py-2">
        {predictions.map((p, i) => {
          const Icon = RANK_ICONS[i] ?? Award
          const iconColor = RANK_COLORS[i] ?? 'text-gray-400'
          const bg = RANK_BG[i] ?? ''
          return (
            <li
              key={p.rank}
              className={`py-3.5 space-y-2 ${i > 0 ? 'opacity-80' : ''}`}
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <div className="flex items-center gap-2.5">
                <div className={`flex items-center justify-center w-7 h-7 rounded-lg border ${bg}`}>
                  <Icon size={15} className={iconColor} />
                </div>
                {i === 0 && (
                  <span className="bg-primary text-white text-xs font-bold px-2 py-0.5 rounded-full">
                    Principal
                  </span>
                )}
                <span className={`font-semibold ${i === 0 ? 'text-gray-900 text-base' : 'text-gray-600 text-sm'}`}>
                  {p.brand} {p.model}
                </span>
              </div>
              <ConfBar value={p.confidence} delay={i * 150} />
            </li>
          )
        })}
      </ul>
    </div>
  )
}
