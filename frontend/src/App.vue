<script setup lang="ts">
import { onMounted, ref } from 'vue'
import StaffForm from './components/StaffForm.vue'
import StaffTable from './components/StaffTable.vue'
import ScheduleForm from './components/ScheduleForm.vue'
import ScheduleTable from './components/ScheduleTable.vue'
import StatsPage from './pages/StatsPage.vue'
import type { NewStaff } from '@/types/staff'
import type { NewSchedule } from '@/types/schedule'
import { useDutyStore } from '@/stores/duty'
import { log, errorMessage } from '@/utils/logger'

const store = useDutyStore()
const loading = ref(false)
const error = ref('')

async function refresh() {
  loading.value = true
  error.value = ''
  try {
    await Promise.all([store.loadStaff(), store.loadSchedule(), store.loadStats()])
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
    await store.createStaff(payload)
  } catch (e) {
    const msg = errorMessage(e)
    log.error('Failed to create staff', e)
    error.value = `Failed to create staff: ${msg}`
  }
}

async function onDelete(id: number) {
  error.value = ''
  try {
    await store.deleteStaff(id)
  } catch (e) {
    const msg = errorMessage(e)
    log.error('Failed to delete staff', e)
    error.value = `Failed to delete staff: ${msg}`
  }
}

async function onAssign(payload: NewSchedule) {
  error.value = ''
  try {
    await store.createSchedule(payload)
  } catch (e) {
    const msg = errorMessage(e)
    log.error('Failed to assign duty', e)
    error.value = `Failed to assign duty: ${msg}`
  }
}

async function onUnassign(dateStr: string) {
  error.value = ''
  try {
    await store.deleteScheduleByDate(dateStr)
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
    <StaffTable :items="store.staff" @delete="onDelete" />

    <section class="space-y-3">
      <h2 class="text-xl font-semibold">Duty Scheduling</h2>
      <ScheduleForm :staff="store.staff" @submit="onAssign" />
      <ScheduleTable :items="store.schedule" :staff="store.staff" @delete="onUnassign" />
    </section>

    <section class="space-y-3">
      <StatsPage :staff="store.staff" :refresh-key="store.schedule.length" />
    </section>
  </main>
  
</template>
