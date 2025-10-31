<template>
  <section class="space-y-4 p-4">
    <h2 class="text-xl font-semibold">Duty Statistics</h2>

    <div>
      <table class="min-w-full border divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-3 py-2 text-left text-sm font-semibold text-gray-700">Staff</th>
            <th class="px-3 py-2 text-right text-sm font-semibold text-gray-700">Duty Count</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="row in rows" :key="row.staff_id">
            <td class="px-3 py-2">{{ row.name }}</td>
            <td class="px-3 py-2 text-right">{{ row.count }}</td>
          </tr>
          <tr v-if="rows.length === 0">
            <td colspan="2" class="px-3 py-6 text-center text-gray-500">No data yet</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div>
      <canvas v-if="chartReady" ref="chartEl" height="120"></canvas>
      <p v-else class="text-gray-500 text-sm">Install chart.js to enable bar chart (npm i chart.js).</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import type { Staff } from '@/types/staff'
import { useDutyStore } from '@/stores/duty'
import { log } from '@/utils/logger'

const props = defineProps<{ staff: Staff[] }>()

const dutyStore = useDutyStore()

const rows = computed(() => {
  return dutyStore.stats
    .map((s) => ({
      staff_id: s.staff_id,
      count: s.count,
      name: props.staff.find((x) => x.id === s.staff_id)?.name || `#${s.staff_id}`,
    }))
    .sort((a, b) => b.count - a.count)
})

const chartEl = ref<HTMLCanvasElement | null>(null)
const chartReady = ref(false)
let destroyChart: (() => void) | null = null

async function drawChart() {
  try {
    const mod = await import('chart.js/auto')
    const Chart = mod.default
    if (destroyChart) {
      destroyChart()
      destroyChart = null
    }
    const ctx = chartEl.value!.getContext('2d')!
    // Build labels and data from rows
    const labels = rows.value.map((r) => r.name)
    const data = rows.value.map((r) => r.count)
    const inst = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Duties',
            data,
            backgroundColor: '#60a5fa',
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, precision: 0 },
        },
      },
    })
    destroyChart = () => inst.destroy()
    chartReady.value = true
  } catch (e) {
    chartReady.value = false
    log.warn('Chart unavailable (install chart.js to enable)', e)
  }
}

// Watch for changes in stats and redraw chart
watch(
  () => dutyStore.stats,
  () => {
    drawChart()
  },
  { immediate: true }
)
</script>
