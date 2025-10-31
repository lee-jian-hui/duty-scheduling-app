import { api } from './client'
import type { DutyStat } from '@/types/stats'

export async function listDutyStats(): Promise<DutyStat[]> {
  const { data } = await api.get<DutyStat[]>('/api/statistics')
  return data
}

