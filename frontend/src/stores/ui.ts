import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  const errorOpen = ref(false)
  const errorMessage = ref('')

  function showError(message: string) {
    errorMessage.value = message
    errorOpen.value = true
  }

  function closeError() {
    errorOpen.value = false
    errorMessage.value = ''
  }

  return { errorOpen, errorMessage, showError, closeError }
})

