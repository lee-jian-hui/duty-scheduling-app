<template>
  <div v-if="open" class="fixed inset-0 z-50 grid place-items-center bg-black/40 p-4" @click.self="close">
    <div class="bg-white rounded shadow w-full max-w-md overflow-hidden">
      <div class="px-4 py-2 border-b flex items-center justify-between">
        <h3 class="font-medium">Something went wrong</h3>
        <button class="text-sm" @click="close">✕</button>
      </div>
      <div class="p-4 text-sm text-red-700">
        {{ message }}
      </div>
      <div class="px-4 py-3 border-t flex justify-end">
        <button class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700" @click="close">OK</button>
      </div>
    </div>
  </div>
  
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useUiStore } from '@/stores/ui'

const ui = useUiStore()
const { errorOpen: open, errorMessage: message } = storeToRefs(ui)

function close() {
  ui.closeError()
}
</script>

