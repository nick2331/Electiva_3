import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  Cell,
} from 'recharts'
import type { StatsOut } from '../types/api'

interface Props {
  stats: StatsOut
}

const PRIMARY = '#0B3D91'
const LIGHT   = '#93b4e8'

function shortDate(iso: string) {
  const d = new Date(iso)
  return `${d.getDate()}/${d.getMonth() + 1}`
}

export default function StatsChart({ stats }: Props) {
  const daily = stats.daily_counts.map((d) => ({ ...d, date: shortDate(d.date) }))
  const top = stats.top_models.slice(0, 8)

  return (
    <div className="space-y-6">
      {/* Totales */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { label: 'Total análisis', value: stats.total_analyses },
          { label: 'Imágenes', value: stats.total_images },
          { label: 'Videos', value: stats.total_videos },
        ].map(({ label, value }) => (
          <div key={label} className="card text-center">
            <p className="text-3xl font-bold text-primary">{value}</p>
            <p className="text-sm text-gray-500 mt-1">{label}</p>
          </div>
        ))}
      </div>

      {/* Análisis por día */}
      <div className="card">
        <h3 className="font-semibold text-gray-800 mb-4">Análisis por día (últimos 30 días)</h3>
        <ResponsiveContainer width="100%" height={180}>
          <AreaChart data={daily} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} interval={4} />
            <YAxis tick={{ fontSize: 11 }} allowDecimals={false} />
            <Tooltip />
            <Area type="monotone" dataKey="count" stroke={PRIMARY} fill={LIGHT} strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Modelos más consultados */}
      <div className="card">
        <h3 className="font-semibold text-gray-800 mb-4">Modelos más consultados</h3>
        {top.length === 0 ? (
          <p className="text-gray-400 text-sm">Sin datos suficientes todavía.</p>
        ) : (
          <ResponsiveContainer width="100%" height={top.length * 36 + 20}>
            <BarChart layout="vertical" data={top} margin={{ top: 0, right: 48, left: 80, bottom: 0 }}>
              <XAxis type="number" hide />
              <YAxis
                type="category"
                dataKey={(d) => `${d.brand} ${d.model}`}
                tick={{ fontSize: 12 }}
                width={80}
              />
              <Tooltip formatter={(v) => [`${v} análisis`, '']} />
              <Bar dataKey="count" radius={[0, 4, 4, 0]}>
                {top.map((_, i) => (
                  <Cell key={i} fill={i === 0 ? PRIMARY : LIGHT} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}
