<script setup lang="ts">
import { ref, onMounted } from 'vue'
import StaffForm from './components/StaffForm.vue'
import StaffTable from './components/StaffTable.vue'
import ScheduleForm from './components/ScheduleForm.vue'
import ScheduleTable from './components/ScheduleTable.vue'
import StatsPage from './pages/StatsPage.vue'
import { listStaff, createStaff, deleteStaff } from './api/staffApi'
import { listSchedule, createSchedule, deleteScheduleByDate } from './api/scheduleApi'
import type { Staff, NewStaff } from '@/types/staff'
import type { Schedule, NewSchedule } from '@/types/schedule'
import { log, errorMessage } from '@/utils/logger'

const items = ref<Staff[]>([])
const loading = ref(false)
const error = ref('')
const schedule = ref<Schedule[]>([])

async function refresh() {
  loading.value = true
  error.value = ''
  try {
    const [staffList, scheduleList] = await Promise.all([
      listStaff(),
      listSchedule(),
    ])
    items.value = staffList
    schedule.value = scheduleList
  } catch (e) {
    const msg = errorMessage(e)
    log.error('Failed to load staff', e)
    error.value = `Failed to load staff: ${msg}`
  } finally {
    loading.value = false
  }
}

async function onCreate(payload: NewStaff) {
  error.value = ''
  try {
    const created = await createStaff(payload)
    items.value = [...items.value, created]
  } catch (e) {
    const msg = errorMessage(e)
    log.error('Failed to create staff', e)
    error.value = `Failed to create staff: ${msg}`
  }
}

async function onDelete(id: number) {
  error.value = ''
  try {
    await deleteStaff(id)
    items.value = items.value.filter((x) => x.id !== id)
  } catch (e) {
    const msg = errorMessage(e)
    log.error('Failed to delete staff', e)
    error.value = `Failed to delete staff: ${msg}`
  }
}

async function onAssign(payload: NewSchedule) {
  error.value = ''
  try {
    const created = await createSchedule(payload)
    schedule.value = [...schedule.value, created]
  } catch (e) {
    const msg = errorMessage(e)
    log.error('Failed to assign duty', e)
    error.value = `Failed to assign duty: ${msg}`
  }
}

async function onUnassign(dateStr: string) {
  error.value = ''
  try {
    await deleteScheduleByDate(dateStr)
    schedule.value = schedule.value.filter((x) => new Date(x.date).toISOString().slice(0, 10) !== dateStr)
  } catch (e) {
    const msg = errorMessage(e)
    log.error('Failed to remove duty', e)
    error.value = `Failed to remove duty: ${msg}`
  }
}

onMounted(refresh)
</script>

<template>
  <main class="max-w-3xl mx-auto p-4 space-y-6">
    <h1 class="text-2xl font-semibold">Staff Manager</h1>
    <p v-if="error" class="text-red-600">{{ error }}</p>
    <p v-if="loading" class="text-gray-600">Loading…</p>
    <StaffForm @submit="onCreate" />
    <StaffTable :items="items" @delete="onDelete" />

    <section class="space-y-3">
      <h2 class="text-xl font-semibold">Duty Scheduling</h2>
      <ScheduleForm :staff="items" @submit="onAssign" />
      <ScheduleTable :items="schedule" :staff="items" @delete="onUnassign" />
    </section>

    <section class="space-y-3">
      <StatsPage :staff="items" />
    </section>
  </main>
  
</template>
