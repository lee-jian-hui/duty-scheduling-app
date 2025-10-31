import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Schedule, NewSchedule } from '@/types/schedule'
import { listSchedule, createSchedule as apiCreateSchedule, deleteScheduleByDate as apiDeleteScheduleByDate, replaceScheduleByDate as apiReplaceScheduleByDate, generateIntelligentSchedule as apiGenerateIntelligentSchedule, wipeAllSchedules as apiWipeAllSchedules, fetchScheduleCsv } from '@/api/scheduleApi'
import { saveBlob } from '@/utils/download'
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

  async function generateIntelligentRange(start: string, end: string) {
    await apiGenerateIntelligentSchedule(start, end)
    // Reload full schedule to reflect changes across the range
    schedule.value = await listSchedule()
    const duty = useDutyStore()
    await duty.loadStats()
  }

  async function wipeAll() {
    await apiWipeAllSchedules()
    schedule.value = []
    const duty = useDutyStore()
    await duty.loadStats()
  }

  async function exportCsv(filename = 'schedule.csv') {
    const blob = await fetchScheduleCsv()
    saveBlob(blob, filename)
  }

  return { schedule, loadSchedule, createSchedule, deleteScheduleByDate, replaceScheduleByDate, generateIntelligentRange, wipeAll, exportCsv }
})
