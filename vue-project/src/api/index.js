// import axios from 'axios'

// const api = axios.create({
//   baseURL: 'http://127.0.0.1:8000',
//   headers: {
//     'Authorization': `Token ${JSON.parse(localStorage.getItem('counter')).token}`
//   }
// })

// export default api
// import axios from 'axios'

// const getToken = () => {
//   const store = localStorage.getItem('counter')
//   return store ? JSON.parse(store).token : null
// }

// const api = axios.create({
//   baseURL: 'http://127.0.0.1:8000',
//   headers: {
//     'Authorization': `Token ${getToken() || ''}`
//   }
// })

// export default api







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