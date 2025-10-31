import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Staff, NewStaff } from '@/types/staff'
import { listStaff, createStaff as apiCreateStaff, deleteStaff as apiDeleteStaff } from '@/api/staffApi'

export const useStaffStore = defineStore('staff', () => {
  const staff = ref<Staff[]>([])

  async function loadStaff() {
    staff.value = await listStaff()
  }

  async function createStaff(payload: NewStaff) {
    const created = await apiCreateStaff(payload)
    staff.value = [...staff.value, created]
  }

  async function deleteStaff(id: number, opts?: { force?: boolean }) {
    await apiDeleteStaff(id, opts?.force ?? false)
    staff.value = staff.value.filter((s) => s.id !== id)
  }

  return { staff, loadStaff, createStaff, deleteStaff }
})
