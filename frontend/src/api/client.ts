import axios from 'axios'
import { API_BASE_URL } from '@/config'
import { log } from '@/utils/logger'

export const api = axios.create({
  baseURL: API_BASE_URL,
})

api.interceptors.request.use((config) => {
  log.debug('API request', { method: config.method, url: config.url })
  return config
})

api.interceptors.response.use(
  (resp) => {
    log.debug('API response', { url: resp.config?.url, status: resp.status })
    return resp
  },
  (error) => {
    const status = error?.response?.status
    const detail = error?.response?.data?.detail || error.message
    log.error('API error', {
      method: error?.config?.method,
      url: error?.config?.url,
      status,
      detail,
    })
    return Promise.reject(error)
  }
)
