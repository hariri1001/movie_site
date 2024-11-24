<template>
    <div class="movie-search">
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          @input="searchMovies"
          placeholder="영화 제목을 입력하세요"
          class="search-input"
        />

        <!-- 영화 검색 섹션 -->
        <div v-if="!selectedMovie && !isEditing" class="search-section">
          <div class="search-box">
            <input 
              type="text" 
              v-model="searchQuery" 
              @input="searchMovies"
              placeholder="영화 제목을 입력하세요 (2글자 이상)"
              class="search-input"
            />
          </div>
          
          <!-- 로딩 표시 -->
          <div v-if="isLoading" class="loading-message">
            검색 중...
          </div>

          <!-- 에러 메시지 -->
          <div v-if="error" class="error-message">
            {{ error }}
          </div>

          <!-- 검색 결과 -->
          <div v-if="searchResults.length > 0" class="search-results">
            <div 
              v-for="movie in searchResults" 
              :key="movie.id"
              @click="selectMovie(movie)"
              class="movie-item"
            >
              <!-- 영화 포스터 -->
              <img 
                v-if="movie.posterPath" 
                :src="movie.posterPath" 
                :alt="movie.title"
                class="movie-poster"
              />
              <div class="movie-info">
                <h3>{{ movie.title }}</h3>
                <p class="release-date">개봉일: {{ movie.releaseDate }}</p>
                <p v-if="movie.overview" class="movie-overview">
                  {{ movie.overview.slice(0, 100) }}{{ movie.overview.length > 100 ? '...' : '' }}
                </p>
              </div>
            </div>
          </div>

          <!-- 검색 결과가 없을 때 -->
          <div v-else-if="searchQuery.length >= 2 && !isLoading" class="no-results">
            검색 결과가 없습니다.
          </div>
        </div>



      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useCounterStore } from '@/stores/counter';
  
  const store = useCounterStore();
  const searchQuery = ref('');
  const searchResults = ref([]);
  const emit = defineEmits(['select-movie']);
  
  const searchMovies = async () => {
    if (searchQuery.value.length < 2) {
      searchResults.value = [];
      return;
    }
    
    try {
      const response = await axios.get(
        `${store.API_URL}/api/v1/movies/search/`,
        {
          params: { query: searchQuery.value },
          headers: { Authorization: `Token ${store.token}` }
        }
      );
      
      searchResults.value = response.data.map(movie => ({
        id: movie.id,
        title: movie.title,
        release_date: movie.release_date,
        poster_url: movie.poster_url,
        posterPath: movie.poster_path 
        ? `https://image.tmdb.org/t/p/w300${movie.poster_path}` 
        : null,
      }));
    } catch (error) {
      console.error('영화 검색 실패:', error);
    }
  };
  
  const selectMovie = (movie) => {
    emit('select-movie', movie);
    searchResults.value = [];
    searchQuery.value = '';
  };
  </script>
  
  <style scoped>
  .movie-search {
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
  }
  
  .search-input {
    width: 100%;
    padding: 8px;
    font-size: 16px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .search-results {
    position: absolute;
    width: 100%;
    max-height: 400px;
    overflow-y: auto;
    background: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    z-index: 1000;
  }
  
  .movie-item {
    display: flex;
    padding: 10px;
    cursor: pointer;
    border-bottom: 1px solid #eee;
  }
  
  .movie-item:hover {
    background-color: #f5f5f5;
  }
  
  .movie-poster {
    width: 50px;
    height: 75px;
    object-fit: cover;
    margin-right: 10px;
  }
  
  .movie-info {
    flex: 1;
  }
  
  .movie-info h4 {
    margin: 0 0 5px 0;
  }
  
  .movie-info p {
    margin: 0;
    color: #666;
    font-size: 14px;
  }


  .loading-message {
    text-align: center;
    padding: 20px;
    color: #666;
  }

  .error-message {
    color: #f44336;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #f44336;
    border-radius: 4px;
    background-color: #ffebee;
  }

  .movie-item {
    display: flex;
    padding: 15px;
    gap: 15px;
    align-items: start;
  }

  .movie-poster {
    width: 100px;
    height: 150px;
    object-fit: cover;
    border-radius: 4px;
  }

  .movie-info {
    flex: 1;
  }

  .movie-info h3 {
    margin: 0 0 8px 0;
    font-size: 1.2rem;
  }

  .release-date {
    color: #666;
    font-size: 0.9rem;
    margin: 5px 0;
  }

  .movie-overview {
    font-size: 0.9rem;
    color: #444;
    line-height: 1.4;
    margin: 8px 0 0 0;
  }

  .no-results {
    text-align: center;
    padding: 20px;
    color: #666;
    background-color: #ffdddd;
    border-radius: 4px;
    margin-top: 10px;
  }

  </style>