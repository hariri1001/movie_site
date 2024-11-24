<template>
    <nav class="navbar navbar-expand-lg" style="background-color: black;" data-bs-theme="dark">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" :to="{ name: 'MainView' }">
          <img src="/POSTlogo.png" alt="Logo" height="30" class="d-inline-block align-text-top">
        </RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" 
                aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
          <ul class="navbar-nav mb-2 mb-lg-0">
            <!-- 검색창 추가 -->
            <form class="d-flex me-auto" @submit.prevent="searchMovies">
              <input 
                class="form-control me-2" 
                type="search" 
                placeholder="영화 검색" 
                aria-label="Search"
                v-model="searchQuery"
              >
              <button class="btn btn-outline-light" type="submit">Search</button>
            </form>



            <!-- <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'MainView' }">Home</RouterLink>
            </li> -->
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'ArticleView' }">Articles</RouterLink>
            </li>
            
            <!-- 로그인 상태에 따라 다른 메뉴 표시 -->
            <template v-if="!store.isLogin">
                <li class="nav-item">
                    <RouterLink class="nav-link" :to="{ name: 'LogInView' }">로그인</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" :to="{ name: 'SignUpView' }">회원가입</RouterLink>
                </li>
            </template>
            <template v-else>
                <li class="nav-item">
                    <RouterLink class="nav-link" :to="{ name: 'ProfileView' }">프로필</RouterLink>
                </li>
                <li class="nav-item">
                  <RouterLink class="nav-link" :to="{ name: 'MovieRandom' }">
                    <i class="fas fa-thumbs-up me-1"></i>랜덤무비
                  </RouterLink>
                </li>
                <li class="nav-item">
                    <button class="btn btn-link nav-link" @click="logOut">로그아웃</button>
                </li>
            </template>
          </ul>
        </div>
        
      </div>
    </nav>
</template>

<script setup>

import axios from 'axios'
import { useCounterStore } from '@/stores/counter'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const searchQuery = ref('')


const store = useCounterStore()
const logOut = function () {
  store.logOut()
}


const searchMovies = async () => {
  if (searchQuery.value.trim()) {
    try {
      router.push({
        name: 'SearchView',
        query: { title: searchQuery.value }
      })
      searchQuery.value = '' // 검색 후 입력창 초기화
    } catch (error) {
      console.error('검색 중 오류 발생:', error)
    }
  }
}


axios.defaults.baseURL = 'http://127.0.0.1:8000'

</script>

<style scoped>
li {
  color: aquamarine;
}
</style>