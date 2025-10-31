type Level = 'debug' | 'info' | 'warn' | 'error'

const LEVELS: Record<Level, number> = {
  debug: 10,
  info: 20,
  warn: 30,
  error: 40,
}

const envLevel = (import.meta.env.VITE_LOG_LEVEL as Level | undefined) || 'debug'
const threshold = LEVELS[envLevel] ?? LEVELS.debug

function enabled(level: Level) {
  return LEVELS[level] >= threshold
}

function ts() {
  return new Date().toISOString()
}

export const log = {
  debug(msg: string, extra?: unknown) {
    if (enabled('debug')) console.debug(`[${ts()}] DEBUG`, msg, extra ?? '')
  },
  info(msg: string, extra?: unknown) {
    if (enabled('info')) console.info(`[${ts()}] INFO`, msg, extra ?? '')
  },
  warn(msg: string, extra?: unknown) {
    if (enabled('warn')) console.warn(`[${ts()}] WARN`, msg, extra ?? '')
  },
  error(msg: string, extra?: unknown) {
    if (enabled('error')) console.error(`[${ts()}] ERROR`, msg, extra ?? '')
  },
}

export function errorMessage(err: unknown): string {
  const anyErr = err as any
  const status = anyErr?.response?.status
  const detail = anyErr?.response?.data?.detail || anyErr?.message || String(err)
  return status ? `${status}: ${detail}` : String(detail)
}

