import { useState } from 'react'
import { Eye, EyeOff, Loader2, Flame } from 'lucide-react'
import { gradcamUrl } from '../api/analyze'

interface Props { analysisId: string }

export default function GradCamViewer({ analysisId }: Props) {
  const [show, setShow] = useState(false)
  const [loaded, setLoaded] = useState(false)

  return (
    <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden animate-slideUp-400">
      <div className="flex items-center justify-between px-5 py-3 border-b border-gray-50">
        <span className="font-semibold text-gray-800 flex items-center gap-2 text-sm">
          <Flame size={16} className="text-orange-500" />
          Mapa de activación (Grad-CAM)
        </span>
        <button
          onClick={() => setShow(v => !v)}
          className="flex items-center gap-1.5 text-xs font-medium text-primary hover:text-primary-dark transition-colors px-3 py-1.5 rounded-lg hover:bg-blue-50"
        >
          {show ? <><EyeOff size={13} /> Ocultar</> : <><Eye size={13} /> Ver qué miró el modelo</>}
        </button>
      </div>

      {show && (
        <div className="p-4 animate-fadeIn">
          <div className="relative rounded-xl overflow-hidden bg-gray-900">
            {!loaded && (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-900/80 z-10">
                <Loader2 className="animate-spin text-white" size={28} />
              </div>
            )}
            <img
              src={gradcamUrl(analysisId)}
              alt="Mapa Grad-CAM"
              className="w-full object-contain max-h-72"
              onLoad={() => setLoaded(true)}
              onError={() => setLoaded(true)}
            />
          </div>
          <p className="text-xs text-gray-400 mt-2 text-center">
            Las zonas cálidas (rojo/amarillo) muestran las regiones clave para la decisión del modelo.
          </p>
        </div>
      )}
    </div>
  )
}
