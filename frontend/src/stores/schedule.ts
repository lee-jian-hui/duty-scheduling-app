import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Schedule, NewSchedule } from '@/types/schedule'
import { listSchedule, createSchedule as apiCreateSchedule, deleteScheduleByDate as apiDeleteScheduleByDate, replaceScheduleByDate as apiReplaceScheduleByDate } from '@/api/scheduleApi'
import { useDutyStore } from './duty'

export const useScheduleStore = defineStore('schedule', () => {
  const schedule = ref<Schedule[]>([])

  async function loadSchedule() {
    schedule.value = await listSchedule()
  }

  async function createSchedule(payload: NewSchedule) {
    const created = await apiCreateSchedule(payload)
    schedule.value = [...schedule.value, created]
    // refresh stats after mutation
    const duty = useDutyStore()
    await duty.loadStats()
  }

  async function deleteScheduleByDate(dateStr: string) {
    await apiDeleteScheduleByDate(dateStr)
    schedule.value = schedule.value.filter((x) => new Date(x.date).toISOString().slice(0, 10) !== dateStr)
    const duty = useDutyStore()
    await duty.loadStats()
  }

  async function replaceScheduleByDate(dateStr: string, staffId: number) {
    const updated = await apiReplaceScheduleByDate(dateStr, staffId)
    // Remove existing assignments for the date, then add the updated one
    const day = dateStr
    schedule.value = schedule.value.filter((x) => new Date(x.date).toISOString().slice(0, 10) !== day)
    schedule.value = [...schedule.value, updated]
    const duty = useDutyStore()
    await duty.loadStats()
  }

  return { schedule, loadSchedule, createSchedule, deleteScheduleByDate, replaceScheduleByDate }
})
