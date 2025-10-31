<template>
  <section class="p-4">
    <table class="min-w-full border divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-3 py-2 text-left text-sm font-semibold text-gray-700">Name</th>
          <th class="px-3 py-2 text-left text-sm font-semibold text-gray-700">Age</th>
          <th class="px-3 py-2 text-left text-sm font-semibold text-gray-700">Position</th>
          <th class="px-3 py-2 text-right text-sm font-semibold text-gray-700">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-gray-200">
        <tr v-for="it in items" :key="it.id">
          <td class="px-3 py-2">{{ it.name }}</td>
          <td class="px-3 py-2">{{ it.age }}</td>
          <td class="px-3 py-2">{{ it.position }}</td>
          <td class="px-3 py-2 text-right">
            <button class="text-red-600 hover:underline" @click="$emit('delete', it.id)">Delete</button>
          </td>
        </tr>
        <tr v-if="!items || items.length === 0">
          <td colspan="4" class="px-3 py-6 text-center text-gray-500">No staff yet</td>
        </tr>
      </tbody>
    </table>
  </section>
  
</template>

<script setup lang="ts">
import type { Staff } from '@/types/staff'

defineProps<{ items: Staff[] }>()
defineEmits<{ (e: 'delete', id: number): void }>()
</script>
