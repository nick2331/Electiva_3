import { useNavigate } from 'react-router-dom'
import { useAnalyzeImage, useAnalyzeVideo } from '../hooks/useAnalyze'
import UploadZone from '../components/UploadZone'
import { AlertCircle, Zap, Shield, BarChart3 } from 'lucide-react'

const features = [
  { icon: Zap, label: 'Análisis en segundos', desc: 'IA con visión por computador' },
  { icon: Shield, label: '20 modelos colombianos', desc: 'Mercado automotor local' },
  { icon: BarChart3, label: 'Top-3 con confianza', desc: 'Resultados explicados' },
]

export default function HomePage() {
  const navigate = useNavigate()
  const imgMutation = useAnalyzeImage()
  const vidMutation = useAnalyzeVideo()
  const loading = imgMutation.isPending || vidMutation.isPending
  const error   = imgMutation.error ?? vidMutation.error

  const handleFile = async (file: File) => {
    const isVideo = file.type.startsWith('video/')
    try {
      const result = isVideo
        ? await vidMutation.mutateAsync(file)
        : await imgMutation.mutateAsync(file)
      navigate(`/resultado/${result.analysis_id}`)
    } catch { /* error ya en mutation.error */ }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      {/* Hero */}
      <div className="text-center space-y-3 animate-slideUp">
        <div className="inline-flex items-center gap-2 bg-primary/10 text-primary text-xs font-semibold px-3 py-1.5 rounded-full border border-primary/20">
          <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
          Sistema IA activo
        </div>
        <h1 className="text-4xl font-extrabold text-gray-900 leading-tight">
          Identifica tu{' '}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-primary-light">
            vehículo
          </span>
        </h1>
        <p className="text-gray-500 text-base max-w-md mx-auto">
          Sube una foto y la IA identificará la marca y modelo en segundos.
        </p>
      </div>

      {/* Upload */}
      <div className="animate-slideUp" style={{ animationDelay: '0.1s' }}>
        <UploadZone onFile={handleFile} loading={loading} />
      </div>

      {error && (
        <div className="flex items-start gap-3 bg-red-50 border border-red-200 rounded-xl p-4 text-accent animate-fadeIn">
          <AlertCircle size={18} className="shrink-0 mt-0.5" />
          <p className="text-sm">{(error as Error).message}</p>
        </div>
      )}

      {/* Features */}
      <div className="grid grid-cols-3 gap-3 animate-slideUp" style={{ animationDelay: '0.25s' }}>
        {features.map(({ icon: Icon, label, desc }) => (
          <div key={label} className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm text-center hover:shadow-md hover:-translate-y-0.5 transition-all duration-200">
            <div className="w-9 h-9 rounded-lg bg-primary/10 flex items-center justify-center mx-auto mb-2">
              <Icon size={18} className="text-primary" />
            </div>
            <p className="text-xs font-semibold text-gray-800">{label}</p>
            <p className="text-xs text-gray-400 mt-0.5">{desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
