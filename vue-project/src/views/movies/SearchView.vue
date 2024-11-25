<template>
  <div class="container-fluid px-4">
    <div class="title">
      <h2>검색 결과: "{{ $route.query.title }}"</h2>
    </div>
    
    
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <div v-else-if="movies.length === 0" class="alert alert-info" role="alert">
      검색 결과가 없습니다.
    </div>

    <div v-else class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 row-cols-xl-5 g-4">
      <div v-for="movie in movies" :key="movie.id" class="col">
        <div class="card h-100" @click="goToMovie(movie.id)">
          <div class="poster-wrapper">
            <img
              :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
              class="card-img-top"
              alt="movie poster"
              @error="handleImageError"
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const movies = ref([])
const loading = ref(false)
const error = ref(null)
const router = useRouter()

const searchMovies = async (query) => {
  if (!query) return
  
  loading.value = true
  error.value = null
  
  try {
    const response = await axios.get(`https://api.themoviedb.org/3/search/movie`, {
      headers: {
        Authorization: `Bearer ${import.meta.env.VITE_TMDB_API_KEY}`,
        accept: 'application/json'
      },
      params: {
        language: 'ko-KR',
        query: query,
        page: 1,
        include_adult: false
      }
    })
    movies.value = response.data.results
  } catch (err) {
    error.value = '영화를 검색하는 도중 오류가 발생했습니다.'
    console.error('검색 오류:', err)
  } finally {
    loading.value = false
  }
}

const handleImageError = (e) => {
  e.target.src = '/no-image.jpg'
}

watch(() => route.query.title, (newQuery) => {
  searchMovies(newQuery)
})

onMounted(() => {
  if (route.query.title) {
    searchMovies(route.query.title)
  }
})

const goToMovie = (movieId) => {
  router.push({
    name: 'MovieDetail',
    params: { movieId: movieId }
  })
}
</script>

<style scoped>
.title{
  margin-top: 20px;
  margin-bottom: 20px;
}


.container-fluid {
  max-width: 1200px;
}

.poster-wrapper {
  position: relative;
  width: 100%;
  padding-top: 150%; /* 2:3 영화 포스터 비율 */
  overflow: hidden;
}

.card-img-top {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card {
  transition: transform 0.2s;
  border: none; /* 테두리 제거 */
  border-radius: 8px;
  overflow: hidden;
  background: none; /* 배경색 제거 */
}

.card:hover {
  transform: scale(1.02);
  cursor: pointer;
}

/* 반응형 그리드 설정 */
@media (max-width: 576px) {
  .row-cols-1 > * {
    flex: 0 0 100%;
    max-width: 100%;
  }
}

@media (min-width: 576px) and (max-width: 768px) {
  .row-cols-sm-2 > * {
    flex: 0 0 50%;
    max-width: 50%;
  }
}

@media (min-width: 768px) and (max-width: 992px) {
  .row-cols-md-3 > * {
    flex: 0 0 33.333333%;
    max-width: 33.333333%;
  }
}

@media (min-width: 992px) and (max-width: 1200px) {
  .row-cols-lg-4 > * {
    flex: 0 0 25%;
    max-width: 25%;
  }
}

@media (min-width: 1200px) {
  .row-cols-xl-5 > * {
    flex: 0 0 20%;
    max-width: 20%;
  }
}
</style>