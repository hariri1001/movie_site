






import axios from 'axios'
import { useCounterStore } from '@/stores/counter'

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000'
})

// 요청 인터셉터 추가
api.interceptors.request.use(
  config => {
    const store = useCounterStore()
    if (store.token) {
      config.headers.Authorization = `Token ${store.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

export default api