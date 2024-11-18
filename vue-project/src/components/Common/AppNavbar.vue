<template>
    <nav class="navbar bg-dark navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" :to="{ name: 'MainView' }">
          <img src="/favicon.ico" alt="Logo" height="30" class="d-inline-block align-text-top">
        </RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" 
                data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" 
                aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
          <!-- 영화 검색 기능 -->
          <!-- <form class="d-flex" role="search">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form> -->
          <form @submit.prevent="searchMovies" class="d-flex">
            <input v-model="searchQuery" class="form-control me-2" type="search">
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
          <ul class="navbar-nav mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'MainView' }">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'ArticleView' }">Articles</RouterLink>
            </li>
            
            <!-- 로그인 상태에 따라 다른 메뉴 표시 -->
            <template v-if="!store.isLogin">
                <li class="nav-item">
                    <RouterLink class="nav-link" :to="{ name: 'LogInView' }">Login</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" :to="{ name: 'SignUpView' }">SignUp</RouterLink>
                </li>
            </template>
            <template v-else>
                <li class="nav-item">
                    <RouterLink class="nav-link" :to="{ name: 'ProfileView' }">MyProfile</RouterLink>
                </li>
                <li class="nav-item">
                    <button class="btn btn-link nav-link" @click="logOut">Logout</button>
                </li>
            </template>
          </ul>
        </div>
        
      </div>
    </nav>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const logOut = function () {
  store.logOut()
}

import { ref } from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const movies = ref([])
axios.defaults.baseURL = 'http://127.0.0.1:8000'
const searchMovies = async () => {
  try {
    console.log(`검색 쿼리: ${searchQuery.value}`) // 디버깅용
    const response = await axios.get(`/api/v1/movies/search/?q=${searchQuery.value}`)
    movies.value = response.data
  } catch (error) {
    console.error(error)
  }
}

</script>

<style scoped>

</style>