import { ref } from 'vue'
import { errorMessage } from '@/utils/logger'

export function useAsyncAction() {
  const loading = ref(false)
  const error = ref('')

  async function run(action: () => Promise<void>, opts?: { mapError?: (e: unknown) => string }) {
    loading.value = true
    error.value = ''
    try {
      await action()
    } catch (e) {
      error.value = opts?.mapError ? opts.mapError(e) : errorMessage(e)
    } finally {
      loading.value = false
    }
  }

  return { loading, error, run }
}
