import { useState } from 'react'
import { Eye, EyeOff, Loader2 } from 'lucide-react'
import { gradcamUrl } from '../api/analyze'

interface Props {
  analysisId: string
}

export default function GradCamViewer({ analysisId }: Props) {
  const [show, setShow] = useState(false)
  const [loaded, setLoaded] = useState(false)

  return (
    <div className="card space-y-3">
      <div className="flex items-center justify-between">
        <span className="font-semibold text-gray-800 flex items-center gap-2">
          <Eye size={18} className="text-primary" />
          Mapa de activación (Grad-CAM)
        </span>
        <button
          onClick={() => setShow((v) => !v)}
          className="text-primary text-sm font-medium flex items-center gap-1 hover:underline"
        >
          {show ? <><EyeOff size={14} /> Ocultar</> : <><Eye size={14} /> Ver qué miró el modelo</>}
        </button>
      </div>

      {show && (
        <div className="relative">
          {!loaded && (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-50 rounded-lg">
              <Loader2 className="animate-spin text-primary" size={28} />
            </div>
          )}
          <img
            src={gradcamUrl(analysisId)}
            alt="Mapa Grad-CAM"
            className="w-full rounded-lg object-contain max-h-64"
            onLoad={() => setLoaded(true)}
            onError={() => setLoaded(true)}
          />
          <p className="text-xs text-gray-400 mt-2">
            Las zonas cálidas (rojo/amarillo) indican las regiones en las que el modelo basó su decisión.
          </p>
        </div>
      )}
    </div>
  )
}
