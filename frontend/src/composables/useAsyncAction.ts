import { ref } from 'vue'
import { errorMessage } from '@/utils/logger'
import { useUiStore } from '@/stores/ui'

export function useAsyncAction() {
  const loading = ref(false)
  const error = ref('')
  const ui = useUiStore()

  async function run(action: () => Promise<void>, opts?: { mapError?: (e: unknown) => string }) {
    loading.value = true
    error.value = ''
    try {
      await action()
    } catch (e) {
      const msg = opts?.mapError ? opts.mapError(e) : errorMessage(e)
      error.value = msg
      // Also display a global modal
      ui.showError(msg)
    } finally {
      loading.value = false
    }
  }

  return { loading, error, run }
}
