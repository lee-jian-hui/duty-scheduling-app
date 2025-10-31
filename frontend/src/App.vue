<script setup lang="ts">
import { onMounted } from 'vue'
import StaffForm from './components/StaffForm.vue'
import StaffTable from './components/StaffTable.vue'
import ScheduleForm from './components/ScheduleForm.vue'
import ScheduleTable from './components/ScheduleTable.vue'
import StatsPage from './pages/StatsPage.vue'
import CalendarPage from './pages/CalendarPage.vue'

import type { NewStaff } from '@/types/staff'
import type { NewSchedule } from '@/types/schedule'

import { useDutyStore } from '@/stores/duty'
import { useStaffStore } from '@/stores/staff'
import { useScheduleStore } from '@/stores/schedule'
import { useAppInit } from '@/composables/useAppInit'
import { useAsyncAction } from '@/composables/useAsyncAction'
import { httpStatus, httpDetail } from '@/utils/http'
import { errorMessage } from '@/utils/logger'

const staffStore = useStaffStore()
const scheduleStore = useScheduleStore()
const dutyStore = useDutyStore()
const { init } = useAppInit()

const { loading, error, run } = useAsyncAction()

onMounted(() => run(init))

const onCreate = (payload: NewStaff) =>
  run(() => staffStore.createStaff(payload), {
    mapError: (e) => {
      const status = httpStatus(e)
      if (status === 409) return httpDetail(e) || 'Staff name already exists'
      return errorMessage(e)
    },
  })

const onDelete = (id: number) =>
  run(() => staffStore.deleteStaff(id))

const onAssign = (payload: NewSchedule) =>
  run(() => scheduleStore.createSchedule(payload), {
    mapError: (e) => {
      const status = httpStatus(e)
      if (status === 409) return httpDetail(e) || 'Staff already assigned for this date'
      return errorMessage(e)
    },
  })

const onUnassign = (date: string) =>
  run(() => scheduleStore.deleteScheduleByDate(date))
</script>

<template>
  <main class="max-w-3xl mx-auto p-4 space-y-6">
    <h1 class="text-2xl font-semibold">Staff Manager</h1>

    <p v-if="error" class="text-red-600">{{ error }}</p>
    <p v-if="loading" class="text-gray-600">Loading…</p>

    <!-- Staff -->
    <StaffForm @submit="onCreate" />
    <StaffTable :items="staffStore.staff" @delete="onDelete" />

    <!-- Schedule -->
    <!-- <section class="space-y-3">
      <h2 class="text-xl font-semibold">Duty Scheduling</h2>
      <ScheduleForm :staff="staffStore.staff" @submit="onAssign" />
      <ScheduleTable
        :items="scheduleStore.schedule"
        :staff="staffStore.staff"
        @delete="onUnassign"
      />
    </section> -->

    <!-- Calendar -->
    <CalendarPage :staff="staffStore.staff" :schedule="scheduleStore.schedule" @assign="onAssign" />
    <!-- Stats -->
    <StatsPage :staff="staffStore.staff" :refresh-key="scheduleStore.schedule.length" />

  </main>
</template>
