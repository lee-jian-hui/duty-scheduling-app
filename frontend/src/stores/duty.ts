import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Staff, NewStaff } from '@/types/staff'
import type { Schedule, NewSchedule } from '@/types/schedule'
import type { DutyStat } from '@/types/stats'
import { listStaff, createStaff as apiCreateStaff, deleteStaff as apiDeleteStaff } from '@/api/staffApi'
import { listSchedule, createSchedule as apiCreateSchedule, deleteScheduleByDate as apiDeleteScheduleByDate } from '@/api/scheduleApi'
import { listDutyStats } from '@/api/statsApi'
import { log, errorMessage } from '@/utils/logger'

export const useDutyStoreuseDutyStore = defineStore('duty', () => {
  const staff = ref<Staff[]>([])
  const schedule = ref<Schedule[]>([])
  const stats = ref<DutyStat[]>([])

  async function loadStaff() {
    staff.value = await listStaff()
  }

  async function createStaff(payload: NewStaff) {
    const created = await apiCreateStaff(payload)
    staff.value = [...staff.value, created]
  }

  async function deleteStaff(id: number) {
    await apiDeleteStaff(id)
    staff.value = staff.value.filter((s) => s.id !== id)
  }

  async function loadSchedule() {
    schedule.value = await listSchedule()
  }

  async function createSchedule(payload: NewSchedule) {
    const created = await apiCreateSchedule(payload)
    schedule.value = [...schedule.value, created]
    // keep stats in sync
    await loadStats()
  }

  async function deleteScheduleByDate(dateStr: string) {
    await apiDeleteScheduleByDate(dateStr)
    schedule.value = schedule.value.filter((x) => new Date(x.date).toISOString().slice(0, 10) !== dateStr)
    // keep stats in sync
    await loadStats()
  }

  async function loadStats() {
    try {
      stats.value = await listDutyStats()
    } catch (e) {
      log.error('Failed to load stats', errorMessage(e))
      throw e
    }
  }

  return {
    staff,
    schedule,
    stats,
    loadStaff,
    createStaff,
    deleteStaff,
    loadSchedule,
    createSchedule,
    deleteScheduleByDate,
    loadStats,
  }
})

