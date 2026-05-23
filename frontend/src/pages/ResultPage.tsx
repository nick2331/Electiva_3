import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Download, Loader2, AlertCircle } from 'lucide-react'
import { useResult } from '../hooks/useAnalyze'
import { reportUrl } from '../api/analyze'
import ResultCard from '../components/ResultCard'
import DescriptionBox from '../components/DescriptionBox'
import GradCamViewer from '../components/GradCamViewer'

export default function ResultPage() {
  const { id } = useParams<{ id: string }>()
  const { data, isLoading, error } = useResult(id)

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-24 gap-3 text-primary animate-fadeIn">
        <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center">
          <Loader2 className="animate-spin text-primary" size={32} />
        </div>
        <span className="text-sm font-medium text-gray-600">Cargando resultado…</span>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="max-w-lg mx-auto bg-white rounded-2xl border border-red-100 shadow-sm p-5 flex items-start gap-3 animate-scaleIn">
        <AlertCircle size={20} className="text-accent shrink-0 mt-0.5" />
        <p className="text-sm text-gray-700">{(error as Error)?.message ?? 'No se encontró el análisis.'}</p>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto space-y-4">
      {/* Top bar */}
      <div className="flex items-center justify-between animate-slideIn">
        <Link to="/" className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-primary font-medium transition-colors group">
          <ArrowLeft size={15} className="group-hover:-translate-x-0.5 transition-transform" /> Volver
        </Link>
        <a
          href={reportUrl(data.analysis_id)}
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-2 text-sm py-2 px-4 rounded-xl bg-gradient-to-r from-primary to-primary-light text-white font-semibold shadow hover:shadow-md transition-all duration-200"
        >
          <Download size={15} /> Descargar PDF
        </a>
      </div>

      {/* Image preview */}
      {data.thumbnail_b64 && (
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-4 animate-scaleIn">
          <img
            src={`data:image/jpeg;base64,${data.thumbnail_b64}`}
            alt="Vehículo analizado"
            className="mx-auto max-h-56 rounded-xl object-contain"
          />
        </div>
      )}

      <ResultCard predictions={data.predictions} noVehicle={data.no_vehicle} suggestions={data.suggestions} />
      <DescriptionBox text={data.description_es} />
      {data.gradcam_url && <GradCamViewer analysisId={data.analysis_id} />}

      <p className="text-xs text-gray-400 text-center pb-4 animate-fadeIn">
        ID: {data.analysis_id} · {new Date(data.created_at).toLocaleString('es-CO')}
      </p>
    </div>
  )
}
