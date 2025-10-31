import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { DutyStat } from '@/types/stats'
import { listDutyStats } from '@/api/statsApi'
import { log, errorMessage } from '@/utils/logger'

export const useDutyStore = defineStore('duty', () => {
  const stats = ref<DutyStat[]>([])

  async function loadStats() {
    try {
      stats.value = await listDutyStats()
    } catch (e) {
      log.error('Failed to load stats', errorMessage(e))
      throw e
    }
  }

  return {
    stats,
    loadStats,
  }
})
