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
      <div className="flex items-center justify-center py-24 text-primary">
        <Loader2 className="animate-spin mr-2" size={28} />
        <span>Cargando resultado…</span>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="max-w-lg mx-auto card border-l-4 border-accent flex items-start gap-3">
        <AlertCircle size={20} className="text-accent shrink-0" />
        <p className="text-sm">{(error as Error)?.message ?? 'No se encontró el análisis.'}</p>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto space-y-5">
      <div className="flex items-center justify-between">
        <Link to="/" className="flex items-center gap-1.5 text-sm text-primary hover:underline">
          <ArrowLeft size={16} /> Volver
        </Link>
        <a
          href={reportUrl(data.analysis_id)}
          target="_blank"
          rel="noreferrer"
          className="btn-primary flex items-center gap-2 text-sm py-2"
        >
          <Download size={16} /> Descargar PDF
        </a>
      </div>

      {data.thumbnail_b64 && (
        <div className="card p-4">
          <img
            src={`data:image/jpeg;base64,${data.thumbnail_b64}`}
            alt="Vehículo analizado"
            className="mx-auto max-h-52 rounded-lg object-contain"
          />
        </div>
      )}

      <ResultCard
        predictions={data.predictions}
        noVehicle={data.no_vehicle}
        suggestions={data.suggestions}
      />

      <DescriptionBox text={data.description_es} />

      {data.gradcam_url && <GradCamViewer analysisId={data.analysis_id} />}

      <p className="text-xs text-gray-400 text-center">
        ID del análisis: {data.analysis_id}  ·  {new Date(data.created_at).toLocaleString('es-CO')}
      </p>
    </div>
  )
}
