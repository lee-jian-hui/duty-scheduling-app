import { api } from './client'
import type { Schedule, NewSchedule } from '@/types/schedule'

export async function listSchedule(): Promise<Schedule[]> {
  const { data } = await api.get<Schedule[]>('/api/schedule')
  return data
}

export async function createSchedule(payload: NewSchedule): Promise<Schedule> {
  const { data } = await api.post<Schedule>('/api/schedule', payload)
  return data
}

export async function deleteScheduleByDate(dateStr: string): Promise<{ deleted: boolean }> {
  const { data } = await api.delete<{ deleted: boolean }>(`/api/schedule/${encodeURIComponent(dateStr)}`)
  return data
}

export async function replaceScheduleByDate(dateStr: string, staffId: number): Promise<Schedule> {
  const { data } = await api.put<Schedule>(`/api/schedule/${encodeURIComponent(dateStr)}`, { staff_id: staffId })
  return data
}
