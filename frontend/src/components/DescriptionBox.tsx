import { FileText } from 'lucide-react'

interface Props {
  text: string
}

export default function DescriptionBox({ text }: Props) {
  return (
    <div className="card space-y-2">
      <div className="flex items-center gap-2 text-primary font-semibold">
        <FileText size={18} />
        Descripción automática
      </div>
      <p className="text-gray-700 leading-relaxed text-sm">{text}</p>
    </div>
  )
}
