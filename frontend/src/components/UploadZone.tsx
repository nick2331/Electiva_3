import { useRef, useState, useCallback, DragEvent } from 'react'
import { UploadCloud, Camera, FileVideo, FileImage, X, Loader2, ScanLine } from 'lucide-react'

interface Props {
  onFile: (file: File) => void
  loading: boolean
}

const MAX_IMAGE_MB = 10
const ACCEPTED = '.jpg,.jpeg,.png,.mp4'

function fileMeta(file: File) {
  return { isVideo: file.type.startsWith('video/'), sizeMb: (file.size / 1024 / 1024).toFixed(1) }
}

function LoadingOverlay({ preview }: { preview: string | null }) {
  return (
    <div className="space-y-4">
      {preview ? (
        <div className="relative mx-auto max-h-48 rounded-xl overflow-hidden">
          <img src={preview} alt="Vista previa" className="mx-auto max-h-48 rounded-xl object-contain opacity-60" />
          {/* Scanner line */}
          <div className="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-primary to-transparent animate-scan pointer-events-none" />
          <div className="absolute inset-0 bg-gradient-to-b from-primary/5 to-primary/20 rounded-xl" />
        </div>
      ) : (
        <div className="flex justify-center">
          <FileVideo size={56} className="text-primary opacity-40" />
        </div>
      )}
      <div className="flex flex-col items-center gap-2">
        <div className="flex items-center gap-2 text-primary font-semibold text-sm">
          <Loader2 size={16} className="animate-spin" />
          Analizando con IA…
        </div>
        <div className="w-48 h-1.5 bg-gray-100 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-primary to-primary-light rounded-full animate-shimmer bg-[length:200%_100%]" />
        </div>
        <p className="text-xs text-gray-400">Puede tardar hasta 60 s en el primer uso</p>
      </div>
    </div>
  )
}

export default function UploadZone({ onFile, loading }: Props) {
  const inputRef  = useRef<HTMLInputElement>(null)
  const cameraRef = useRef<HTMLInputElement>(null)
  const [preview,  setPreview]  = useState<string | null>(null)
  const [dragging, setDragging] = useState(false)
  const [selected, setSelected] = useState<File | null>(null)
  const [error,    setError]    = useState<string | null>(null)

  const validate = (file: File): string | null => {
    const ok = ['image/jpeg', 'image/png', 'video/mp4', 'video/mpeg', 'video/quicktime']
    if (!ok.includes(file.type)) return 'Formato no soportado. Use JPG, PNG o MP4.'
    if (file.type.startsWith('image/') && file.size > MAX_IMAGE_MB * 1024 * 1024)
      return `Las imágenes no pueden superar ${MAX_IMAGE_MB} MB.`
    return null
  }

  const pick = useCallback((file: File) => {
    const err = validate(file)
    if (err) { setError(err); return }
    setError(null)
    setSelected(file)
    if (!file.type.startsWith('video/')) setPreview(URL.createObjectURL(file))
    else setPreview(null)
  }, [])

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault(); setDragging(false)
    const f = e.dataTransfer.files[0]; if (f) pick(f)
  }

  const clear = () => {
    setSelected(null); setPreview(null); setError(null)
    if (inputRef.current) inputRef.current.value = ''
  }

  return (
    <div className="w-full space-y-4">
      <div
        onDragOver={e => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => !selected && !loading && inputRef.current?.click()}
        className={[
          'relative border-2 rounded-2xl p-8 text-center transition-all duration-300',
          loading  ? 'border-primary bg-blue-50/60 cursor-wait animate-borderPulse'
          : dragging ? 'border-primary bg-blue-50 scale-[1.01] shadow-lg cursor-copy border-solid'
          : selected ? 'border-primary/40 bg-white cursor-default border-solid'
          : 'border-dashed border-gray-300 bg-white hover:border-primary hover:bg-blue-50/40 hover:shadow-md cursor-pointer',
        ].join(' ')}
      >
        {loading ? (
          <LoadingOverlay preview={preview} />
        ) : selected ? (
          <div className="space-y-3">
            {preview ? (
              <img src={preview} alt="Vista previa" className="mx-auto max-h-48 rounded-xl object-contain shadow-sm" />
            ) : (
              <div className="flex justify-center">
                <FileVideo size={56} className="text-primary opacity-60" />
              </div>
            )}
            <p className="text-sm font-medium text-gray-700">{selected.name}</p>
            <p className="text-xs text-gray-400">{fileMeta(selected).sizeMb} MB</p>
            <button
              onClick={e => { e.stopPropagation(); clear() }}
              className="absolute top-3 right-3 p-1.5 rounded-full bg-gray-100 hover:bg-red-100 text-gray-500 hover:text-accent transition-colors"
            >
              <X size={15} />
            </button>
          </div>
        ) : (
          <>
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-4 group-hover:bg-primary/20 transition-colors">
              <UploadCloud size={32} className="text-primary" />
            </div>
            <p className="text-gray-800 font-semibold text-base">Arrastra tu imagen aquí</p>
            <p className="text-gray-400 text-sm mt-1">o haz clic para seleccionar</p>
            <p className="text-gray-300 text-xs mt-3">JPG · PNG hasta {MAX_IMAGE_MB} MB · MP4</p>
          </>
        )}
      </div>

      {error && <p className="text-accent text-sm font-medium animate-fadeIn">{error}</p>}

      <div className="flex gap-3">
        <input ref={inputRef}  type="file" accept={ACCEPTED}   className="hidden" onChange={e => { const f = e.target.files?.[0]; if (f) pick(f) }} />
        <input ref={cameraRef} type="file" accept="image/*" capture="environment" className="hidden" onChange={e => { const f = e.target.files?.[0]; if (f) pick(f) }} />

        <button
          onClick={() => cameraRef.current?.click()}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-gray-200 bg-white text-gray-600 text-sm font-medium hover:border-primary hover:text-primary hover:bg-blue-50 transition-all duration-200 disabled:opacity-50"
          disabled={loading}
        >
          <Camera size={15} /> Cámara
        </button>

        <button
          onClick={() => inputRef.current?.click()}
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-gray-200 bg-white text-gray-600 text-sm font-medium hover:border-primary hover:text-primary hover:bg-blue-50 transition-all duration-200 disabled:opacity-50"
          disabled={loading}
        >
          <FileImage size={15} /> Examinar
        </button>

        <button
          onClick={() => { if (selected && !loading) onFile(selected) }}
          disabled={!selected || loading}
          className="flex-1 flex items-center justify-center gap-2 py-2.5 px-5 rounded-xl bg-gradient-to-r from-primary to-primary-light text-white font-semibold text-sm shadow-md hover:shadow-lg hover:from-primary-dark hover:to-primary transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none"
        >
          {loading ? <><Loader2 size={15} className="animate-spin" /> Analizando…</> : <><ScanLine size={15} /> Analizar</>}
        </button>
      </div>
    </div>
  )
}
