export function formatISODate(date: Date): string {
  // Always format as YYYY-MM-DD in UTC to avoid tz drift
  const iso = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()))
    .toISOString()
  return iso.slice(0, 10)
}

export function daysInMonth(year: number, monthIndex0: number): number {
  return new Date(year, monthIndex0 + 1, 0).getDate()
}

export function getMonthMatrix(year: number, monthIndex0: number) {
  // Returns a 6x7 matrix of Date objects covering the month view (Sun..Sat)
  const first = new Date(Date.UTC(year, monthIndex0, 1))
  const firstDow = first.getUTCDay() // 0=Sun
  const total = daysInMonth(year, monthIndex0)

  const matrix: Date[][] = []
  let dayCounter = 1 - firstDow
  for (let week = 0; week < 6; week++) {
    const row: Date[] = []
    for (let dow = 0; dow < 7; dow++) {
      row.push(new Date(Date.UTC(year, monthIndex0, dayCounter)))
      dayCounter++
    }
    matrix.push(row)
  }
  return matrix
}

// Robustly extract YYYY-MM-DD from API datetime strings without tz drift
export function dateKeyFromISO(isoLike: string): string {
  // API returns strings like `2025-11-03T00:00:00` or `...Z`. The first 10 chars are the date.
  if (typeof isoLike === 'string' && isoLike.length >= 10) return isoLike.slice(0, 10)
  // Fallback
  try {
    return new Date(isoLike as any).toISOString().slice(0, 10)
  } catch {
    return String(isoLike)
  }
}
