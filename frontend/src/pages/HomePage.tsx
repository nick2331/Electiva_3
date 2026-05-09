import { useNavigate } from 'react-router-dom'
import { useAnalyzeImage, useAnalyzeVideo } from '../hooks/useAnalyze'
import UploadZone from '../components/UploadZone'
import { AlertCircle } from 'lucide-react'

export default function HomePage() {
  const navigate = useNavigate()
  const imgMutation  = useAnalyzeImage()
  const vidMutation  = useAnalyzeVideo()
  const loading = imgMutation.isPending || vidMutation.isPending
  const error   = imgMutation.error ?? vidMutation.error

  const handleFile = async (file: File) => {
    const isVideo = file.type.startsWith('video/')
    try {
      const result = isVideo
        ? await vidMutation.mutateAsync(file)
        : await imgMutation.mutateAsync(file)
      navigate(`/resultado/${result.analysis_id}`)
    } catch {
      // El error ya está en mutation.error
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-primary">Identifica tu vehículo</h1>
        <p className="text-gray-500 text-sm">
          Sube una foto o video corto y el sistema identificará la marca y modelo automáticamente.
        </p>
      </div>

      <UploadZone onFile={handleFile} loading={loading} />

      {error && (
        <div className="flex items-start gap-3 bg-red-50 border border-red-200 rounded-xl p-4 text-accent">
          <AlertCircle size={18} className="shrink-0 mt-0.5" />
          <p className="text-sm">{(error as Error).message}</p>
        </div>
      )}
    </div>
  )
}
