// import axios from 'axios'

// const api = axios.create({
//   baseURL: 'http://127.0.0.1:8000',
//   headers: {
//     'Authorization': `Token ${JSON.parse(localStorage.getItem('counter')).token}`
//   }
// })

// export default api
import axios from 'axios'

const getToken = () => {
  const store = localStorage.getItem('counter')
  return store ? JSON.parse(store).token : null
}

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Authorization': `Token ${getToken() || ''}`
  }
})

export default api