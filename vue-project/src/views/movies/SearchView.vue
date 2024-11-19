<template>
  <div class="container mt-4">
    <h2>검색 결과: "{{ $route.query.title }}"</h2>
    
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

    <div v-else class="row row-cols-1 row-cols-md-4 g-4">
      <div v-for="movie in movies" :key="movie.id" class="col">
        <div class="card h-100" @click="goToMovie(movie.id)">
          <img 
            :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
            class="card-img-top" 
            alt="movie poster"
            @error="handleImageError"
          >
          <!-- <div class="card-body">
            <h5 class="card-title">{{ movie.title }}</h5>
            <p class="card-text">{{ movie.overview?.slice(0, 100) }}...</p>
            <p class="card-text">
              <small class="text-muted">평점: {{ movie.vote_average }}</small>
            </p>
          </div>
          <div class="card-footer">
            <small class="text-muted">개봉일: {{ movie.release_date }}</small>
          </div> -->
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
  e.target.src = '/no-image.jpg'  // 적절한 대체 이미지 경로로 변경
}

watch(() => route.query.title, (newQuery) => {
  searchMovies(newQuery)
})

onMounted(() => {
  if (route.query.title) {
    searchMovies(route.query.title)
  }
})

// 영화 상세 페이지로 이동
const goToMovie = (movieId) => {
  router.push({ 
    name: 'MovieDetail',  // 또는 실제 사용 중인 라우트 이름
    params: { movieId: movieId }  // route.params.movieId를 사용하고 있으므로 'movieId'로 변경
  })
}


</script>

<style scoped>
.card-img-top {
  height: 300px;
  object-fit: cover;
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: scale(1.02);
  cursor: pointer;
}

/* 긴 제목이나 설명이 카드 레이아웃을 깨지지 않도록 */
.card-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-text {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
</style>