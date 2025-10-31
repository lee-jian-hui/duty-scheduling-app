import { useStaffStore } from '@/stores/staff'
import { useScheduleStore } from '@/stores/schedule'
import { useDutyStore } from '@/stores/duty'

export function useAppInit() {
  const staffStore = useStaffStore()
  const scheduleStore = useScheduleStore()
  const dutyStore = useDutyStore()

  async function init() {
    await Promise.all([
      staffStore.loadStaff(),
      scheduleStore.loadSchedule(),
      dutyStore.loadStats(),
    ])
  }

  return { init }
}

