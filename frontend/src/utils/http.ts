export function httpStatus(err: unknown): number | undefined {
  const anyErr = err as any
  return anyErr?.response?.status
}

export function httpDetail(err: unknown): string | undefined {
  const anyErr = err as any
  return anyErr?.response?.data?.detail
}

