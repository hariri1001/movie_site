import { ref, computed} from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }

    
    
  })
  const router = useRouter()


  // DRF로 전체 게시글 요청을 보내고 응답을 받아 articles에 저장하는 함수
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) => {
        // console.log(res.data)
        articles.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }


  const signUp = async function (payload) {
    try {
      // 회원가입 요청
      const signupResponse = await axios({
        method: 'post',
        url: `${API_URL}/api/v1/accounts/signup/`,
        data: {
          username: payload.username,
          first_name: payload.firstName,
          password1: payload.password1,
          password2: payload.password2,
          email: payload.Email
        }
      })
      console.log('회원가입 성공:', signupResponse.data)
      
      // 성공하면 바로 로그인 시도
      await logIn({
        username: payload.username,
        password: payload.password1
      })
    } catch (error) {
      // 이미 회원가입이 성공한 경우에도 로그인 페이지로 이동
      if (error.response?.status === 500) {
        router.push({ name: 'LogInView' })
      } else {
        console.error('회원가입 실패:', error.response?.data)
        alert('회원가입에 실패했습니다.')
      }
    }
  }
  
  const logIn = async function (payload) {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/api/v1/auth/login/`,
        data: {
          username: payload.username,
          password: payload.password
        }
      })
      
      // 로그인 성공 처리
      token.value = response.data.key
      console.log('로그인 성공, 토큰:', token.value)
      
      // 로그인 성공 후 페이지 이동
      router.push({ name: 'MainView' }).catch((err) => {
        console.error('페이지 이동 실패:', err)
        // 페이지 이동이 실패하면 강제로 새로고침
        window.location.href = '/'
      })
    } catch (error) {
      console.error('로그인 실패:', error)
      if (error.response?.status === 400) {
        alert('가입된 정보가 없습니다. 회원가입을 해주세요.')
      } else {
        alert('로그인에 실패했습니다.')
      }
      router.push({ name: 'LogInView' })
    }
  }

  // 로그아웃
  const logOut = function () {
    // 토큰이 없으면 바로 로그아웃 처리
    if (!token.value) {
      clearAllData()
      router.push({ name: 'ArticleView' })
      return
    }
  
    axios({
      method: 'post',
      url: `${API_URL}/api/v1/auth/logout/`,
      headers: {
        'Authorization': `Token ${token.value}`
      }
    })
      .then((res) => {
        clearAllData()
        router.push({ name: 'ArticleView' })
      })
      .catch((err) => {
        console.log('로그아웃 에러:', err.response?.data)
        // 에러가 나도 로그아웃 처리
        clearAllData()
        router.push({ name: 'ArticleView' })
      })
  }


  
  // onBeforeMount(() => {
  //   clearAllData() // 페이지 로드 시 초기화
  // })

  const clearAllData = () => {
    token.value = null
    localStorage.clear()
    document.cookie.split(";").forEach(c => {
      document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/")
    })
  }



  // 프로필 정보 저장
  const userProfile = ref(null)

  // 프로필 정보 가져오기
  const getProfile = async () => {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/api/v1/accounts/profile/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      userProfile.value = response.data
      console.log(response.data)
    } catch (error) {
      console.error('프로필 조회 실패:', error)
    }
  }

  // 프로필 정보 업데이트
  const updateProfile = async (profileData) => {
    try {
      const response = await axios({
        method: 'put',
        url: `${API_URL}/api/v1/accounts/profile/update/`,
        headers: {
          Authorization: `Token ${token.value}`
        },
        data: {
          first_name: profileData.first_name,
          email: profileData.email
        }
      })
      userProfile.value = response.data
      return true
    } catch (error) {
      console.error('프로필 업데이트 실패:', error)
      return false
    }
  }

  // 회원탈퇴
  const deleteAccount = async () => {
    try {
      await axios({
        method: 'delete',
        url: `${API_URL}/api/v1/accounts/delete/`,
        headers: {
          Authorization: `Token ${token.value}`
        }
      })
      clearAllData() // 로그아웃 처리
      router.push({ name: 'LogInView' }) // 로그인 페이지로 이동
      return true
    } catch (error) {
      console.error('회원탈퇴 실패:', error)
      return false
    }
  }


  return { articles, API_URL, getArticles, signUp, logIn,
     token, isLogin, logOut, userProfile, updateProfile, getProfile, clearAllData, deleteAccount }
}, {
 persist: {
   storage: sessionStorage, 
   paths: ['token', 'userProfile']}
 })
