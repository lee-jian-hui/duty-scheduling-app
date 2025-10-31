import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Schedule, NewSchedule } from '@/types/schedule'
import { listSchedule, createSchedule as apiCreateSchedule, deleteScheduleByDate as apiDeleteScheduleByDate, replaceScheduleByDate as apiReplaceScheduleByDate } from '@/api/scheduleApi'
import { useDutyStore } from './duty'
import { dateKeyFromISO } from '@/utils/date'

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
    schedule.value = schedule.value.filter((x) => dateKeyFromISO(x.date) !== dateStr)
    const duty = useDutyStore()
    await duty.loadStats()
  }

  async function replaceScheduleByDate(dateStr: string, staffId: number) {
    const updated = await apiReplaceScheduleByDate(dateStr, staffId)

    // Remove all existing assignments for this date
    schedule.value = schedule.value.filter((x) => dateKeyFromISO(x.date) !== dateStr)

    // Add the new assignment
    schedule.value = [...schedule.value, updated]

    const duty = useDutyStore()
    await duty.loadStats()
  }

  return { schedule, loadSchedule, createSchedule, deleteScheduleByDate, replaceScheduleByDate }
})
