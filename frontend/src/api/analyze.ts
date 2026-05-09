import client from './client'
import type { AnalysisResult, HistoryListOut, StatsOut } from '../types/api'

export async function analyzeImage(file: File): Promise<AnalysisResult> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await client.post<AnalysisResult>('/analyze/image', form)
  return data
}

export async function analyzeVideo(file: File): Promise<AnalysisResult> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await client.post<AnalysisResult>('/analyze/video', form)
  return data
}

export async function getResult(id: string): Promise<AnalysisResult> {
  const { data } = await client.get<AnalysisResult>(`/results/${id}`)
  return data
}

export async function getHistory(limit = 10, offset = 0): Promise<HistoryListOut> {
  const { data } = await client.get<HistoryListOut>('/history', { params: { limit, offset } })
  return data
}

export async function deleteHistoryEntry(id: string): Promise<void> {
  await client.delete(`/history/${id}`)
}

export async function getStats(adminKey: string): Promise<StatsOut> {
  const { data } = await client.get<StatsOut>('/admin/stats', {
    headers: { 'X-Admin-Key': adminKey },
  })
  return data
}

export function reportUrl(analysisId: string): string {
  return `/api/v1/results/${analysisId}/report`
}

export function gradcamUrl(analysisId: string): string {
  return `/api/v1/results/${analysisId}/gradcam`
}
