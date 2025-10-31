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

function toIsoDateTime(v: string | Date): string {
  if (v instanceof Date) return v.toISOString()
  // if YYYY-MM-DD, set to midnight UTC
  if (/^\d{4}-\d{2}-\d{2}$/.test(v)) return `${v}T00:00:00.000Z`
  return v
}

export async function generateIntelligentSchedule(
  start: string | Date,
  end: string | Date,
): Promise<Schedule[]> {
  const payload = { start_date: toIsoDateTime(start), end_date: toIsoDateTime(end) }
  const { data } = await api.post<Schedule[]>('/api/schedule/intelligent-schedule', payload)
  console.log("generating intelligent schedule")
  return data
}

export async function wipeAllSchedules(): Promise<{ deleted: boolean }> {
  const { data } = await api.delete<{ deleted: boolean }>('/api/schedule')
  return data
}
