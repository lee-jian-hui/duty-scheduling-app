import { ref } from 'vue'
import { errorMessage } from '@/utils/logger'

export function useAsyncAction() {
  const loading = ref(false)
  const error = ref('')

  async function run(action: () => Promise<void>) {
    loading.value = true
    error.value = ''
    try {
      await action()
    } catch (e) {
      error.value = errorMessage(e)
    } finally {
      loading.value = false
    }
  }

  return { loading, error, run }
}

