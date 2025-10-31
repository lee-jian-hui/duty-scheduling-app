export type Schedule = {
  id: string
  // ISO datetime string from backend
  date: string
  staff_id: number
}

export type NewSchedule = {
  // ISO datetime string to satisfy backend (construct from YYYY-MM-DD)
  date: string
  staff_id: number
}

