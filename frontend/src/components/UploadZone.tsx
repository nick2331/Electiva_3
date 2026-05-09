import { useRef, useState, useCallback, DragEvent, ChangeEvent } from 'react'
import { UploadCloud, Camera, FileVideo, FileImage, X } from 'lucide-react'

interface Props {
  onFile: (file: File) => void
  loading: boolean
}

const MAX_IMAGE_MB = 10
const MAX_VIDEO_S_LABEL = '30 s'
const ACCEPTED = '.jpg,.jpeg,.png,.mp4'

function fileMeta(file: File) {
  const isVideo = file.type.startsWith('video/')
  const sizeMb = (file.size / 1024 / 1024).toFixed(1)
  return { isVideo, sizeMb }
}

export default function UploadZone({ onFile, loading }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const cameraRef = useRef<HTMLInputElement>(null)
  const [preview, setPreview] = useState<string | null>(null)
  const [dragging, setDragging] = useState(false)
  const [selected, setSelected] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)

  const validate = (file: File): string | null => {
    const allowed = ['image/jpeg', 'image/png', 'video/mp4', 'video/mpeg', 'video/quicktime']
    if (!allowed.includes(file.type)) return 'Formato no soportado. Use JPG, PNG o MP4.'
    if (file.type.startsWith('image/') && file.size > MAX_IMAGE_MB * 1024 * 1024)
      return `Las imágenes no pueden superar ${MAX_IMAGE_MB} MB.`
    return null
  }

  const pick = useCallback((file: File) => {
    const err = validate(file)
    if (err) { setError(err); return }
    setError(null)
    setSelected(file)
    const { isVideo } = fileMeta(file)
    if (!isVideo) setPreview(URL.createObjectURL(file))
    else setPreview(null)
  }, [])

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files[0]
    if (f) pick(f)
  }

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (f) pick(f)
  }

  const clear = () => {
    setSelected(null)
    setPreview(null)
    setError(null)
    if (inputRef.current) inputRef.current.value = ''
  }

  const submit = () => { if (selected && !loading) onFile(selected) }

  return (
    <div className="w-full space-y-4">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => !selected && inputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-10 text-center transition-colors cursor-pointer
          ${dragging ? 'border-primary bg-blue-50' : 'border-gray-300 bg-white hover:border-primary hover:bg-blue-50/40'}
          ${selected ? 'cursor-default' : ''}`}
      >
        {selected ? (
          <div className="space-y-3">
            {preview ? (
              <img src={preview} alt="Vista previa" className="mx-auto max-h-48 rounded-lg object-contain" />
            ) : (
              <div className="flex justify-center">
                <FileVideo size={56} className="text-primary opacity-60" />
              </div>
            )}
            <p className="text-sm font-medium text-gray-700">{selected.name}</p>
            <p className="text-xs text-gray-400">{fileMeta(selected).sizeMb} MB</p>
            <button
              onClick={(e) => { e.stopPropagation(); clear() }}
              className="absolute top-3 right-3 p-1 rounded-full bg-gray-100 hover:bg-red-100 text-gray-500 hover:text-accent transition-colors"
            >
              <X size={16} />
            </button>
          </div>
        ) : (
          <>
            <UploadCloud size={48} className="mx-auto text-gray-400 mb-3" />
            <p className="text-gray-700 font-medium">Arrastra tu imagen o video aquí</p>
            <p className="text-gray-400 text-sm mt-1">o haz clic para seleccionar</p>
            <p className="text-gray-400 text-xs mt-3">
              JPG · PNG hasta {MAX_IMAGE_MB} MB  ·  MP4 hasta {MAX_VIDEO_S_LABEL}
            </p>
          </>
        )}
      </div>

      {error && <p className="text-accent text-sm font-medium">{error}</p>}

      <div className="flex gap-3">
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED}
          className="hidden"
          onChange={handleChange}
        />
        <input
          ref={cameraRef}
          type="file"
          accept="image/*"
          capture="environment"
          className="hidden"
          onChange={handleChange}
        />

        <button
          onClick={() => cameraRef.current?.click()}
          className="btn-ghost flex items-center gap-2"
          disabled={loading}
        >
          <Camera size={16} /> Usar cámara
        </button>

        <button
          onClick={() => inputRef.current?.click()}
          className="btn-ghost flex items-center gap-2"
          disabled={loading}
        >
          <FileImage size={16} /> Examinar
        </button>

        <button
          onClick={submit}
          disabled={!selected || loading}
          className="btn-primary flex-1 flex items-center justify-center gap-2"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
              </svg>
              Analizando…
            </span>
          ) : (
            'Analizar'
          )}
        </button>
      </div>
    </div>
  )
}
