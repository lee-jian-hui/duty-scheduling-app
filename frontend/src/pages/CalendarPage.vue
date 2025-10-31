<template>
  <section class="space-y-3 p-2">
    <div class="flex items-center justify-between">
      <h2 class="text-xl font-semibold">Duty Calendar</h2>
      <div class="flex items-center gap-2">
        <button class="px-2 py-1 border rounded" @click="prevMonth">Prev</button>
        <div class="min-w-[10rem] text-center font-medium">{{ monthLabel }}</div>
        <button class="px-2 py-1 border rounded" @click="nextMonth">Next</button>
      </div>
    </div>

    <div class="grid grid-cols-7 text-sm font-semibold text-gray-600">
      <div class="p-2 text-center">Sun</div>
      <div class="p-2 text-center">Mon</div>
      <div class="p-2 text-center">Tue</div>
      <div class="p-2 text-center">Wed</div>
      <div class="p-2 text-center">Thu</div>
      <div class="p-2 text-center">Fri</div>
      <div class="p-2 text-center">Sat</div>
    </div>

    <div class="grid grid-cols-7 gap-px bg-gray-200">
      <div
        v-for="(cell, idx) in cells"
        :key="idx"
        class="bg-white min-h-[96px] p-2 flex flex-col gap-1"
        :class="{ 'opacity-50': cell.outside }"
      >
        <div class="text-xs text-gray-500">{{ cell.day }}</div>
        <div class="space-y-1">
          <div v-for="(name, i) in cell.names" :key="i" class="text-xs truncate">
            • {{ name }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Staff } from '@/types/staff'
import type { Schedule } from '@/types/schedule'
import { getMonthMatrix, formatISODate } from '@/utils/date'

const props = defineProps<{ staff: Staff[]; schedule: Schedule[] }>()

const today = new Date()
const year = ref(today.getUTCFullYear())
const month = ref(today.getUTCMonth()) // 0-based

function nextMonth() {
  const d = new Date(Date.UTC(year.value, month.value + 1, 1))
  year.value = d.getUTCFullYear()
  month.value = d.getUTCMonth()
}
function prevMonth() {
  const d = new Date(Date.UTC(year.value, month.value - 1, 1))
  year.value = d.getUTCFullYear()
  month.value = d.getUTCMonth()
}

const monthLabel = computed(() => {
  return new Date(Date.UTC(year.value, month.value, 1)).toLocaleString(undefined, {
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  })
})

const scheduleMap = computed(() => {
  // Map YYYY-MM-DD -> array of staff names
  const map = new Map<string, string[]>()
  for (const s of props.schedule) {
    const key = formatISODate(new Date(s.date))
    const staff = props.staff.find((x) => x.id === s.staff_id)
    const name = staff ? staff.name : `#${s.staff_id}`
    const arr = map.get(key) || []
    arr.push(name)
    map.set(key, arr)
  }
  return map
})

const cells = computed(() => {
  const matrix = getMonthMatrix(year.value, month.value)
  const firstOfMonth = new Date(Date.UTC(year.value, month.value, 1))
  const thisMonth = firstOfMonth.getUTCMonth()

  const list: { day: number; outside: boolean; names: string[] }[] = []
  for (const row of matrix) {
    for (const d of row) {
      const outside = d.getUTCMonth() !== thisMonth
      const key = formatISODate(d)
      const names = scheduleMap.value.get(key) || []
      list.push({ day: d.getUTCDate(), outside, names })
    }
  }
  return list
})
</script>

