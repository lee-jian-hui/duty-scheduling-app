<script setup lang="ts">
import { onMounted } from 'vue'
import StaffForm from './components/StaffForm.vue'
import StaffTable from './components/StaffTable.vue'
import ScheduleForm from './components/ScheduleForm.vue'
import ScheduleTable from './components/ScheduleTable.vue'
import StatsPage from './pages/StatsPage.vue'
import CalendarPage from './pages/CalendarPage.vue'
import ErrorModal from './components/ErrorModal.vue'

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
  run(async () => {
    try {
      await staffStore.deleteStaff(id)
    } catch (e: any) {
      // If staff has duties, ask for confirmation to cascade delete
      const status = (e?.response?.status as number | undefined)
      if (status === 409) {
        const confirmed = window.confirm('This staff still has scheduled duties. Delete staff and remove those duties?')
        if (confirmed) {
          await staffStore.deleteStaff(id, { force: true })
          // After cascading on backend, refresh schedule and stats to drop placeholders like #id
          await Promise.all([scheduleStore.loadSchedule(), dutyStore.loadStats()])
        } else {
          // User canceled: swallow the original 409 so no global error modal pops
          return
        }
      } else {
        throw e
      }
    }
  })

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

const onAssignFromCalendar = (evt: { payload: NewSchedule; mode: 'create' | 'update' }) =>
  run(async () => {
    const yyyyMmDd = evt.payload.date.slice(0, 10)
    if (evt.mode === 'update') {
      await scheduleStore.replaceScheduleByDate(yyyyMmDd, evt.payload.staff_id)
    } else {
      await scheduleStore.createSchedule(evt.payload)
    }
  }, {
    mapError: (e) => {
      const status = httpStatus(e)
      if (status === 409) return httpDetail(e) || 'Staff already assigned for this date'
      return errorMessage(e)
    },
  })
</script>

<template>
  <main class="max-w-3xl mx-auto p-4 space-y-6">
    <h1 class="text-2xl font-semibold">Staff Manager</h1>

    <!-- Global error modal replaces inline banner -->
    <p v-if="loading" class="text-gray-600">Loading…</p>

    <!-- Staff -->
    <div class="flex items-end gap-3">
      <div class="flex-1 min-w-0">
        <StaffForm @submit="onCreate" />
      </div>

    </div>
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
    <CalendarPage
      :staff="staffStore.staff"
      :schedule="scheduleStore.schedule"
      @assign="onAssignFromCalendar"
      @delete-date="onUnassign"
      @generate="({ start, end }) => run(() => scheduleStore.generateIntelligentRange(start, end))"
      @wipe-all="() => run(() => scheduleStore.wipeAll())"
      @export="() => run(() => scheduleStore.exportCsv())"
    />
    <!-- Stats -->
    <StatsPage :staff="staffStore.staff" />
    <ErrorModal />

  </main>
</template>
