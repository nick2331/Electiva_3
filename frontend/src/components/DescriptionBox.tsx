import { FileText, Sparkles } from 'lucide-react'

interface Props { text: string }

export default function DescriptionBox({ text }: Props) {
  return (
    <div className="bg-white rounded-2xl border border-blue-100 shadow-sm overflow-hidden animate-slideUp-200">
      <div className="flex items-center gap-2 px-5 py-3 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-blue-100">
        <FileText size={16} className="text-primary" />
        <span className="font-semibold text-primary text-sm">Descripción automática</span>
        <Sparkles size={13} className="text-blue-300 ml-auto" />
      </div>
      <p className="px-5 py-4 text-gray-700 leading-relaxed text-sm">{text}</p>
    </div>
  )
}
