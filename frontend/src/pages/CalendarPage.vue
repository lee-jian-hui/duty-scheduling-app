

<script setup lang="ts">
  import { computed, ref } from 'vue'
  import type { Staff } from '@/types/staff'
  import type { Schedule, NewSchedule } from '@/types/schedule'
  import { getMonthMatrix, formatISODate } from '@/utils/date'
  import ScheduleForm from '@/components/ScheduleForm.vue'

  const props = defineProps<{ staff: Staff[]; schedule: Schedule[] }>()
  const emit = defineEmits<{
    (e: 'assign', payload: { payload: NewSchedule; mode: 'create' | 'update' }): void
    (e: 'delete-date', date: string): void
  }>()

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
      const key = s.date.slice(0, 10)
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

    const list: { day: number; outside: boolean; names: string[]; iso: string }[] = []
    for (const row of matrix) {
      for (const d of row) {
        const outside = d.getUTCMonth() !== thisMonth
        const key = formatISODate(d)
        const names = scheduleMap.value.get(key) || []
        list.push({ day: d.getUTCDate(), outside, names, iso: key })
      }
    }
    return list
  })

  // Modal assign state
  const showAssign = ref(false)
  const selectedDate = ref<string>('')
  function openAssign(iso: string) {
    selectedDate.value = iso
    showAssign.value = true
  }
  function closeAssign() {
    showAssign.value = false
  }
  function onAssign(payload: NewSchedule) {
    // Always use update mode to replace the assignment for the day
    emit('assign', { payload, mode: 'update' })
    closeAssign()
  }

  const hasExistingForSelected = computed(() => {
    const arr = scheduleMap.value.get(selectedDate.value)
    return !!arr && arr.length > 0
  })

  function onDeleteDate() {
    emit('delete-date', selectedDate.value)
    closeAssign()
  }
</script>

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
        class="bg-white min-h-[96px] p-2 flex flex-col gap-1 cursor-pointer hover:bg-blue-50"
        :class="{ 'opacity-50': cell.outside }"
        @click="openAssign(cell.iso)"
      >
        <div class="text-xs text-gray-500">{{ cell.day }}</div>
        <div class="space-y-1">
          <div v-for="(name, i) in cell.names" :key="i" class="text-xs truncate">
            • {{ name }}
          </div>
        </div>
      </div>
    </div>

    <!-- Assign modal -->
    <div v-if="showAssign" class="fixed inset-0 bg-black/40 grid place-items-center p-4" @click.self="closeAssign">
      <div class="bg-white rounded shadow w-full max-w-md">
        <div class="flex items-center justify-between px-4 py-2 border-b">
          <div class="font-medium">Assign duty for {{ selectedDate }}</div>
          <button class="text-sm" @click="closeAssign">✕</button>
        </div>
        <ScheduleForm
          class="pt-2"
          :staff="props.staff"
          :default-date="selectedDate"
          :lock-date="true"
          @submit="onAssign"
        />
        <div v-if="hasExistingForSelected" class="px-4 pb-4">
          <button
            class="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700"
            @click="onDeleteDate"
          >
            Delete assignments for this date
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
