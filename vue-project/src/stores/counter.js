import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const articles = ref([]) // 전체 게시글 목록
  const currentArticle = ref(null) // 현재 상세 보기 중인 게시글
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const router = useRouter()

  const isLogin = computed(() => !!token.value)

  // **게시글 관련 메서드**

  // DRF로 전체 게시글 요청
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then((res) => {
        articles.value = res.data
      })
      .catch((err) => {
        console.error('게시글 가져오기 실패:', err)
      })
  }

  // 단일 게시글 가져오기 (상세 보기)
  const getArticleById = function (articleId) {
    axios
      .get(`${API_URL}/api/v1/articles/${articleId}/`, {
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
      .then((res) => {
        currentArticle.value = res.data;
      })
      .catch((err) => {
        console.error('게시글 상세 가져오기 실패:', err);
      });
  };

  // 새 게시글 작성
  const createArticle = function (payload) {
    axios({
      method: 'post',
      url: `${API_URL}/api/v1/articles/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
      data: {
        title: payload.title,
        content: payload.content,
      },
    })
      .then(() => {
        getArticles() // 게시글 목록 새로고침
        router.push({ name: 'ArticleView' }) // 게시글 리스트 페이지로 이동
      })
      .catch((err) => {
        console.error('게시글 작성 실패:', err)
        alert('게시글 작성 중 오류가 발생했습니다.')
      })
  }

  // **인증 관련 메서드**
  const signUp = async function (payload) {
    try {
      const signupResponse = await axios({
        method: 'post',
        url: `${API_URL}/api/v1/accounts/signup/`,
        data: {
          username: payload.username,
          first_name: payload.firstName,
          password1: payload.password1,
          password2: payload.password2,
          email: payload.Email,
        },
      })
      console.log('회원가입 성공:', signupResponse.data)
      await logIn({
        username: payload.username,
        password: payload.password1,
      })
    } catch (error) {
      console.error('회원가입 실패:', error.response?.data)
      alert('회원가입에 실패했습니다.')
    }
  }

  const logIn = async function (payload) {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/api/v1/auth/login/`,
        data: {
          username: payload.username,
          password: payload.password,
        },
      })
      token.value = response.data.key
      console.log('로그인 성공:', token.value)
      router.push({ name: 'MainView' })
    } catch (error) {
      console.error('로그인 실패:', error)
      alert('로그인에 실패했습니다.')
    }
  }

  const logOut = function () {
    if (!token.value) {
      clearAllData()
      router.push({ name: 'ArticleView' })
      return
    }

    axios({
      method: 'post',
      url: `${API_URL}/api/v1/auth/logout/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then(() => {
        clearAllData()
        router.push({ name: 'ArticleView' })
      })
      .catch((err) => {
        console.error('로그아웃 실패:', err)
        clearAllData()
        router.push({ name: 'ArticleView' })
      })
  }

  const clearAllData = () => {
    token.value = null
    localStorage.clear()
    document.cookie.split(';').forEach((c) => {
      document.cookie = c
        .replace(/^ +/, '')
        .replace(/=.*/, '=;expires=' + new Date().toUTCString() + ';path=/')
    })
  }

  // **프로필 관련 메서드**
  const userProfile = ref(null)

  const getProfile = async () => {
    try {
      const response = await axios({
        method: 'get',
        url: `${API_URL}/api/v1/accounts/profile/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
      userProfile.value = response.data
    } catch (error) {
      console.error('프로필 조회 실패:', error)
    }
  }

  const updateProfile = async (profileData) => {
    try {
      const response = await axios({
        method: 'put',
        url: `${API_URL}/api/v1/accounts/profile/update/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
        data: {
          first_name: profileData.first_name,
          email: profileData.email,
        },
      })
      userProfile.value = response.data
      return true
    } catch (error) {
      console.error('프로필 업데이트 실패:', error)
      return false
    }
  }

  const deleteAccount = async () => {
    try {
      await axios({
        method: 'delete',
        url: `${API_URL}/api/v1/accounts/delete/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      })
      clearAllData()
      router.push({ name: 'LogInView' })
      return true
    } catch (error) {
      console.error('회원탈퇴 실패:', error)
      return false
    }
  }

  return {
    articles,
    currentArticle,
    API_URL,
    token,
    isLogin,
    getArticles,
    getArticleById,
    createArticle,
    signUp,
    logIn,
    logOut,
    userProfile,
    updateProfile,
    getProfile,
    clearAllData,
    deleteAccount,
  }
})
