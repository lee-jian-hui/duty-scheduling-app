<script setup lang="ts">
import { ref, onMounted } from 'vue'
import StaffForm from './components/StaffForm.vue'
import StaffTable from './components/StaffTable.vue'
import { listStaff, createStaff, deleteStaff } from './api/staffApi'
import type { Staff, NewStaff } from '@/types/staff'
import { log, errorMessage } from '@/utils/logger'

const items = ref<Staff[]>([])
const loading = ref(false)
const error = ref('')

async function refresh() {
  loading.value = true
  error.value = ''
  try {
    items.value = await listStaff()
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

onMounted(refresh)
</script>

<template>
  <main class="max-w-3xl mx-auto p-4 space-y-4">
    <h1 class="text-2xl font-semibold">Staff Manager</h1>
    <p v-if="error" class="text-red-600">{{ error }}</p>
    <p v-if="loading" class="text-gray-600">Loading…</p>
    <StaffForm @submit="onCreate" />
    <StaffTable :items="items" @delete="onDelete" />
  </main>
  
</template>
