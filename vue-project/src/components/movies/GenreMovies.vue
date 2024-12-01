<template>
    <div class="container">
      <!-- 장르 목록 -->
       
      <div class="mb-6">
        <h2 class="genre-title">장르별 영화</h2>
        <div class="flex">
          <button
            v-for="genre in genres"
            :key="genre.id"
            @click="selectGenre(genre)"
            class="px-4 py-2 rounded-full"
            :class="{ 'genre-button-selected': selectedGenre && selectedGenre.id === genre.id }"

          >
          <span class="genre-text"># {{ genre.name }}</span>
          </button>
        </div>
      </div>
  
      <!-- 영화 목록 -->
      <div v-if="selectedGenre" class="movie-container">
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
      movies.value = response.data.results.slice(0, 10)  // 20개만 표시
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

.genre-button {
  padding: 8px 16px;   /* px-4 py-2 */
  border-radius: 9999px;  /* rounded-full */
  background-color: #1f2937;  /* bg-gray-800 */
  color: #d1d5db;  /* text-gray-300 */
  margin: 4px;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.genre-button:hover {
  background-color: #374151;  /* hover:bg-gray-700 */
}

.genre-button-selected {
  background-color: #ffffff;  /* bg-white */
  color: #000000;  /* text-black */
}

/* 선택된 버튼의 호버 효과를 다르게 하고 싶다면 */
.genre-button-selected:hover {
  background-color: #f3f4f6;
}

/* 텍스트 스타일링 */
.genre-text {
  font-size: 0.875rem;  /* text-sm */
  font-weight: 500;     /* font-medium */
}

.genre-title{
  margin-bottom: 20px;
}


.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 0px;
  
}




/* 장르별 영화 목록 컨테이너 스타일 */
.movie-container {
  position: relative;
  /* padding: 0 60px; */
  margin: 20px 0;
  max-width: 1400px;
  margin: 20px auto;
}


.movie-card {
    width: 250px;  /* 원하는 카드 크기 */
    margin-right: 20px;
    margin-bottom: 20px;
    transition: transform 0.3s ease;
    position: relative;
    aspect-ratio: 2 / 3;
    overflow: hidden;
    border-radius: 8px;
    background-color: #333;
    max-width: none; /* max-width 제한 해제 */
}


/* 각 행의 5번째 카드마다 마진 제거 */
.movie-card:nth-child(5n) {
  margin-right: 0;
}


/* 그리드 레이아웃을 flex로 변경 */
.grid-layout {
  display: flex;
  flex-wrap: wrap;
  gap: 0; /* gap 제거하고 margin으로 대체 */
  padding: 20px 35px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 포스터 래퍼 스타일 통일 */
.movie-card .poster-wrapper,
.poster-image {
  position: relative;
  width: 100%;
  padding-top: 150%; /* 2:3 비율 유지 */
  overflow: hidden;
}

.poster-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
  transition: transform 0.3s ease;
  padding-top: 0; /* 이미지에는 padding 제거 */
}

/* 호버 효과 통일 */
.movie-card:hover .poster-image,
.movie-card:hover .card-img-top {
  transform: scale(1.05);
}

/* 반응형 디자인 통일 */
@media (max-width: 1200px) {
  .movie-card {
    width: calc(25% - 30px);
    margin-right: 30px;
  }
}

@media (max-width: 768px) {
  .movie-card {
    width: calc(33.333% - 20px);
    margin-right: 20px;
  }
}

@media (max-width: 576px) {
  .movie-card {
    width: calc(50% - 15px);
    margin-right: 15px;
  }
}



  /* .movie-title {
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
  } */
  
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

/* 장르 버튼 컨테이너 스타일 */
.mb-6 {
  max-width: 1400px;  /* 캐러셀과 동일한 너비 */
  margin: 0 auto;     /* 중앙 정렬 */
  padding: 0 35px;    /* 캐러셀과 동일한 패딩 */
}

/* 장르 버튼 스타일 */
.flex {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;  /* 간격을 더 좁게 조정 */
  justify-content: flex-start;
  width: 100%;
  align-items: flex-start; /* 위쪽 정렬로 변경 */
}

/* 개별 장르 버튼 */
.rounded-full {
  background: none;
  border: 1px solid #ead200;
  color: #ffffff;
  padding: 4px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  display: inline-flex;
  align-items: center;
  transition: all 0.3s ease;
}

/* 호버 및 선택된 상태 스타일 */
.rounded-full:hover {
  background-color: #ead200;
  color: rgb(3, 3, 3);
}

/* 반응형 스타일 */
@media (max-width: 1200px) {
  .mb-6 {
    max-width: 1100px;
  }
}

@media (max-width: 768px) {
  .mb-6 {
    max-width: 800px;
    padding: 0 50px;
  }
}

@media (max-width: 576px) {
  .mb-6 {
    max-width: 100%;
    padding: 0 40px;
  }
  
  .rounded-full {
    padding: 6px 12px;
    font-size: 12px;
  }
}


  
  </style>