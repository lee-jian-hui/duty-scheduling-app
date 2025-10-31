<template>
  <section class="p-4">
    <table class="min-w-full border divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-3 py-2 text-left text-sm font-semibold text-gray-700">Date</th>
          <th class="px-3 py-2 text-left text-sm font-semibold text-gray-700">Staff</th>
          <th class="px-3 py-2 text-right text-sm font-semibold text-gray-700">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-200">
        <tr v-for="it in items" :key="it.date">
          <td class="px-3 py-2">{{ formatDate(it.date) }}</td>
          <td class="px-3 py-2">{{ staffName(it.staff_id) }}</td>
          <td class="px-3 py-2 text-right">
            <button class="text-red-600 hover:underline" @click="$emit('delete', formatDate(it.date))">Remove</button>
          </td>
        </tr>
        <tr v-if="!items || items.length === 0">
          <td colspan="3" class="px-3 py-6 text-center text-gray-500">No assignments yet</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup lang="ts">
import type { Schedule } from '@/types/schedule'
import type { Staff } from '@/types/staff'

const props = defineProps<{ items: Schedule[]; staff: Staff[] }>()
defineEmits<{ (e: 'delete', dateStr: string): void }>()

function staffName(id: number): string {
  const s = props.staff.find((x) => x.id === id)
  return s ? s.name : `#${id}`
}

function formatDate(iso: string): string {
  // Display as YYYY-MM-DD
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toISOString().slice(0, 10)
}
</script>
