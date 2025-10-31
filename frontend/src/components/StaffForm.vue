<template>
  <form class="p-4 grid gap-3" @submit.prevent="onSubmit">
    <div class="grid gap-1">
      <label class="text-sm text-gray-700">Name</label>
      <input v-model="form.name" type="text" class="border rounded px-2 py-1" required />
    </div>
    <div class="grid gap-1">
      <label class="text-sm text-gray-700">Age</label>
      <input v-model.number="form.age" type="number" min="16" max="80" class="border rounded px-2 py-1" required />
    </div>
    <div class="grid gap-1">
      <label class="text-sm text-gray-700">Position</label>
      <input v-model="form.position" type="text" class="border rounded px-2 py-1" required />
    </div>
    <div>
      <button type="submit" class="bg-blue-600 text-white px-3 py-1 rounded">Add</button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import type { NewStaff } from '@/types/staff'

const emit = defineEmits<{ (e: 'submit', payload: NewStaff): void }>()

const form = reactive<NewStaff>({ name: '', age: 18, position: '' })

function onSubmit() {
  emit('submit', { name: form.name.trim(), age: Number(form.age), position: form.position.trim() })
  form.name = ''
  form.age = 18
  form.position = ''
}
</script>
