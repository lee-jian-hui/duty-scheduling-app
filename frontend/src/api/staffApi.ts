import { api } from './client'
import type { Staff, NewStaff } from '@/types/staff'

export async function listStaff(): Promise<Staff[]> {
  const { data } = await api.get<Staff[]>('/api/staff')
  return data
}

export async function createStaff(payload: NewStaff): Promise<Staff> {
  const { data } = await api.post<Staff>('/api/staff', payload)
  return data
}

export async function deleteStaff(staffId: number): Promise<{ deleted: boolean }> {
  const { data } = await api.delete<{ deleted: boolean }>(`/api/staff/${staffId}`)
  return data
}

