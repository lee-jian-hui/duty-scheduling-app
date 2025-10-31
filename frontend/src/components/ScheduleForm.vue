<template>
  <form class="p-4 grid gap-3" @submit.prevent="onSubmit">
    <div class="grid gap-1">
      <label class="text-sm text-gray-700">Date</label>
      <input v-model="date" type="date" class="border rounded px-2 py-1" required />
    </div>
    <div class="grid gap-1">
      <label class="text-sm text-gray-700">Staff</label>
      <select v-model.number="staffId" class="border rounded px-2 py-1" required>
        <option disabled value="">Select staff…</option>
        <option v-for="s in staff" :key="s.id" :value="s.id">{{ s.name }}</option>
      </select>
    </div>
    <div>
      <button type="submit" class="bg-blue-600 text-white px-3 py-1 rounded">Assign</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Staff } from '@/types/staff'
import type { NewSchedule } from '@/types/schedule'

const props = defineProps<{ staff: Staff[] }>()
const emit = defineEmits<{ (e: 'submit', payload: NewSchedule): void }>()

const date = ref<string>('')
const staffId = ref<number | ''>('')

function onSubmit() {
  if (!date.value || !staffId.value) return
  // Construct ISO datetime from YYYY-MM-DD at midnight UTC
  const iso = new Date(`${date.value}T00:00:00.000Z`).toISOString()
  emit('submit', { date: iso, staff_id: Number(staffId.value) })
  date.value = ''
  staffId.value = ''
}
</script>

