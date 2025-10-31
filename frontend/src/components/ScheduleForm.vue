<template>
  <form class="p-4 grid gap-3" @submit.prevent="onSubmit">
    <div class="grid gap-1">
      <label class="text-sm text-gray-700">Date</label>
      <input v-model="date" type="date" class="border rounded px-2 py-1" :disabled="lockDate" required />
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
import { ref, watch, toRef } from 'vue'
import type { Staff } from '@/types/staff'
import type { NewSchedule } from '@/types/schedule'

const props = defineProps<{ staff: Staff[]; defaultDate?: string; lockDate?: boolean }>()
const emit = defineEmits<{ (e: 'submit', payload: NewSchedule): void }>()

const lockDate = toRef(props, 'lockDate')
const date = ref<string>(props.defaultDate ?? '')
const staffId = ref<number | ''>('')

watch(
  () => props.defaultDate,
  (val) => {
    if (val) date.value = val
  }
)

function onSubmit() {
  if (!date.value || !staffId.value) return
  // Construct ISO datetime from YYYY-MM-DD at midnight UTC
  const iso = new Date(`${date.value}T00:00:00.000Z`).toISOString()
  emit('submit', { date: iso, staff_id: Number(staffId.value) })
  date.value = ''
  staffId.value = ''
}
</script>
