import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

// 요청 인터셉터 추가
api.interceptors.request.use(
  config => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Token ${authStore.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

export default api