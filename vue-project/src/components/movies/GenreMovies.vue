<template>
    <div class="container mx-auto p-4">
      <!-- 장르 목록 -->
      <div class="mb-6">
        <div class="flex flex-wrap gap-2">
          <button
            v-for="genre in genres"
            :key="genre.id"
            @click="selectGenre(genre)"
            class="px-4 py-2 rounded-full"
            :class="selectedGenre && selectedGenre.id === genre.id ? 
              'bg-white text-black' : 'bg-gray-800 text-gray-300 hover:bg-gray-700'"
          >
            # {{ genre.name }}
          </button>
        </div>
      </div>
  
      <!-- 영화 목록 -->
      <div v-if="selectedGenre" class="mt-8">
        <div class="grid-layout">
          <RouterLink
            v-for="movie in movies" 
            :key="movie.id"
            class="movie-card"
            :to="{ name: 'MovieDetail', params: { movieId: movie.id }}"
          >
            <img 
              v-if="movie.poster_path"
              :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`"
              :alt="movie.title"
              class="poster-image"
            />
            <div class="movie-title">{{ movie.title }}</div>
          </RouterLink>
        </div>
      </div>
  
      <!-- 로딩 상태 -->
      <div v-if="loading" class="text-center py-4">
        <p>로딩 중...</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const genres = ref([])
  const selectedGenre = ref(null)
  const movies = ref([])
  const loading = ref(false)
  const TMDB_KEY = import.meta.env.VITE_TMDB_API_KEY;
  
  const tmdb = axios.create({
    baseURL: 'https://api.themoviedb.org/3',
    headers: {
      'Authorization': `Bearer ${TMDB_KEY}`,
      'accept': 'application/json'
    },
    params: {
      language: 'ko-KR'
    }
  })
  
  const fetchGenres = async () => {
    try {
      const response = await tmdb.get('/genre/movie/list')
      genres.value = response.data.genres
      if (genres.value.length > 0 && !selectedGenre.value) {
        selectGenre(genres.value[0])
      }
    } catch (error) {
      console.error('장르 목록 가져오기 실패:', error)
    }
  }
  
  const fetchMoviesByGenre = async (genreId) => {
    loading.value = true
    try {
      const response = await tmdb.get('/discover/movie', {
        params: {
          with_genres: genreId,
          sort_by: 'popularity.desc',
          page: 1  // 첫 페이지만 가져오기
        }
      })
      movies.value = response.data.results.slice(0, 20)  // 20개만 표시
    } catch (error) {
      console.error('영화 목록 가져오기 실패:', error)
    } finally {
      loading.value = false
    }
  }
  
  const selectGenre = (genre) => {
    selectedGenre.value = genre
    fetchMoviesByGenre(genre.id)
  }
  
  onMounted(() => {
    fetchGenres()
  })
  </script>
  
  <style scoped>
  .grid-layout {
    display: grid;
    grid-template-columns: repeat(5, 1fr);  /* 5개 컬럼으로 고정 */
    gap: 16px;
    padding: 20px 0;
  }
  
  .movie-card {
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.3s ease;
    aspect-ratio: 2/3;
    background-color: #1a1a1a;
  }
  
  .movie-card:hover {
    transform: scale(1.05);
    z-index: 1;
  }
  
  .poster-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .movie-title {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 10px;
    background: linear-gradient(to top, rgba(0,0,0,0.9), rgba(0,0,0,0));
    color: white;
    font-weight: bold;
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  /* 반응형 디자인 */
  @media (max-width: 1024px) {
    .grid-layout {
      grid-template-columns: repeat(4, 1fr);  /* 태블릿에서는 4개 */
    }
  }
  
  @media (max-width: 768px) {
    .grid-layout {
      grid-template-columns: repeat(3, 1fr);  /* 작은 태블릿에서는 3개 */
    }
  }
  
  @media (max-width: 480px) {
    .grid-layout {
      grid-template-columns: repeat(2, 1fr);  /* 모바일에서는 2개 */
    }
  }
  </style>