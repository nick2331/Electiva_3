export interface PredictionItem {
  rank: number
  brand: string
  model: string
  confidence: number
}

export interface AnalysisResult {
  analysis_id: string
  input_type: 'image' | 'video'
  predictions: PredictionItem[]
  description_es: string
  no_vehicle: boolean
  suggestions: string[]
  gradcam_url: string | null
  report_url: string
  created_at: string
  thumbnail_b64: string | null
}

export interface HistoryItem {
  analysis_id: string
  input_type: 'image' | 'video'
  top_brand: string | null
  top_model: string | null
  top_confidence: number | null
  no_vehicle: boolean
  thumbnail_b64: string | null
  created_at: string
}

export interface HistoryListOut {
  items: HistoryItem[]
  total: number
}

export interface DailyCount {
  date: string
  count: number
}

export interface TopModel {
  brand: string
  model: string
  count: number
  percentage: number
}

export interface StatsOut {
  daily_counts: DailyCount[]
  top_models: TopModel[]
  total_analyses: number
  total_images: number
  total_videos: number
}
