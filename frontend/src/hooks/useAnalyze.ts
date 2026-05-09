import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  analyzeImage,
  analyzeVideo,
  deleteHistoryEntry,
  getHistory,
  getResult,
  getStats,
} from '../api/analyze'

export function useAnalyzeImage() {
  return useMutation({ mutationFn: analyzeImage })
}

export function useAnalyzeVideo() {
  return useMutation({ mutationFn: analyzeVideo })
}

export function useResult(id: string | undefined) {
  return useQuery({
    queryKey: ['result', id],
    queryFn: () => getResult(id!),
    enabled: !!id,
    staleTime: Infinity,
  })
}

export function useHistory(limit = 10, offset = 0) {
  return useQuery({
    queryKey: ['history', limit, offset],
    queryFn: () => getHistory(limit, offset),
  })
}

export function useDeleteHistory() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: deleteHistoryEntry,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['history'] }),
  })
}

export function useStats(adminKey: string) {
  return useQuery({
    queryKey: ['stats', adminKey],
    queryFn: () => getStats(adminKey),
    enabled: !!adminKey,
    retry: false,
  })
}
