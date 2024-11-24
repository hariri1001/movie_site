<template>
  <div class="container">
    <!-- 현재 인기 상영작 -->
    
    <div class="carousel-container">
      <h2 class="carousel-title">인기 상영작</h2>
      <div class="carousel">
        <div class="movie-cards" :style="{ transform: `translateX(-${popularPosition}px)` }">
            <div class="movie-card" v-for="(movie, index) in popularMovies" :key="movie.id">
                <!-- <span class="top-badge">TOP 10</span> -->
                <span class="rank-number">{{index + 1}}</span>
                <RouterLink :to="{ name: 'MovieDetail', params: { movieId: movie.id }}" class="text-decoration-none">
                  <div class="card">
                    <div class="poster-wrapper">
                      <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
                          class="card-img-top" 
                          alt="movie poster">
                    </div>
                  </div>
                </RouterLink>
            </div>
        </div>
      </div>
      <button class="carousel-btn prev" @click="movePopular('prev')" :disabled="popularPosition === 0">
        <div class>
          <i class="fas fa-chevron-left"></i>
        </div>
      </button>
      <button class="carousel-btn next" @click="movePopular('next')" :disabled="isEndOfPopular">
        <div class>
          <i class="fas fa-chevron-right"></i>
        </div>
      </button>
    </div>



    <!-- 평점 많이 받은 영화 -->
    
    <div class="carousel-container">
      <h2 class="carousel-title">최고 평점 영화</h2>
      <div class="carousel" ref="carousel">
        <div class="movie-cards" :style="{ transform: `translateX(-${topRatedPosition}px)` }">
          <div class="movie-card" v-for="movie in topRatedMovies" :key="movie.id">
            <RouterLink :to="{ name: 'MovieDetail', params: { movieId: movie.id }}" class="text-decoration-none">
              <div class="card">
                <div class="poster-wrapper">
                  <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`" 
                      class="card-img-top" 
                      alt="movie poster">
                </div>
              </div>
            </RouterLink>
          </div>
        </div>
      </div>
      <button class="carousel-btn prev" @click="moveTopRated('prev')" :disabled="topRatedPosition === 0">
        <div class>
          <i class="fas fa-chevron-left"></i>
        </div>
      </button>
      <button class="carousel-btn next" @click="moveTopRated('next')" :disabled="isEndOfTopRated">
        <div class>
          <i class="fas fa-chevron-right"></i>
        </div>
      </button>
    </div>








    
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import axios from 'axios';

const topRatedMovies = ref([]);
const popularMovies = ref([]);
const TMDB_KEY = import.meta.env.VITE_TMDB_API_KEY;
const topRatedPosition = ref(0);
const popularPosition = ref(0);
const cardWidth = 250;
const visibleCards = 5;

const isEndOfTopRated = computed(() => {
  if (!topRatedMovies.value.length) return true;
  return topRatedPosition.value >= (topRatedMovies.value.length - visibleCards) * cardWidth;
});

const isEndOfPopular = computed(() => {
  if (!popularMovies.value.length) return true;
  return popularPosition.value >= (popularMovies.value.length - visibleCards) * cardWidth;
});

const moveTopRated = (direction) => {
  if (direction === 'next' && !isEndOfTopRated.value) {
    topRatedPosition.value += cardWidth;
  } else if (direction === 'prev' && topRatedPosition.value > 0) {
    topRatedPosition.value -= cardWidth;
  }
};

const movePopular = (direction) => {
  if (direction === 'next' && !isEndOfPopular.value) {
    popularPosition.value += cardWidth;
  } else if (direction === 'prev' && popularPosition.value > 0) {
    popularPosition.value -= cardWidth;
  }
};

onMounted(() => {
  // Top Rated Movies API 요청
  axios.get('https://api.themoviedb.org/3/movie/top_rated', {
    headers: {
      Authorization: `Bearer ${TMDB_KEY}`
    },
    params: {
      language: 'ko-KR',
      page: '1'
    }
  })
  .then((response) => {
    topRatedMovies.value = response.data.results;
  })
  .catch((error) => {
    console.error('Top Rated API 요청 오류:', error);
  });

  // Popular Movies API 요청
  axios.get('https://api.themoviedb.org/3/movie/popular', {
    headers: {
      Authorization: `Bearer ${TMDB_KEY}`
    },
    params: {
      language: 'ko-KR',
      page: '1'
    }
  })
  .then((response) => {
    popularMovies.value = response.data.results;
  })
  .catch((error) => {
    console.error('Popular API 요청 오류:', error);
  });
});
</script>

<style scoped>
.carousel-container {
  position: relative;
  padding: 0 60px; /* 버튼 공간 확보를 위해 패딩 증가 */
  margin: 20px 0;
  overflow: hidden;

  /* 컨테이너 너비 고정 */
  max-width: 1400px; /* 전체 너비 조정 */
  margin: 20px auto; /* 중앙 정렬 */
}

.carousel {
  width: 100%;
  overflow: hidden;
}

.movie-cards {
  display: flex;
  transition: transform 0.3s ease;
}

.movie-card {
  flex: 0 0 auto;
  width: calc(20% - 40px); /* 5개의 카드를 위한 너비 (20%) 및 마진 고려 */
  margin-right: 40px; /* 카드 간격 증가 */
  transition: transform 0.3s ease;
  position: relative; /* position 추가 */
}

.card {
  border: none;
  background: transparent;
}

.poster-wrapper {
  position: relative;
  width: 100%;
  padding-top: 150%; /* 2:3 비율 유지 */
  overflow: hidden;
}

.card-img-top {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
  transition: transform 0.3s ease;
}

.movie-card:hover .card-img-top {
  transform: scale(1.05);
}

/* TOP 10 배지 */
/* .top-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: #e50914;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: bold;
  z-index: 1;
} */


/* 순위 숫자 */

.poster {
  position: relative;
}


.rank-number {
  position: absolute;
  top: 140px;
  left: 115px;
  font-size: 120px;
  font-weight: bold;
  color: rgb(255, 255, 255);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
  z-index: 1;
  opacity: 0.8;
  font-style: italic; /* 이탤릭체 추가 */
  
}

/* 스타일 버튼 */
.carousel-btn {
 position: absolute;
 top: 0;
 bottom: 0;
 width: 100px;
 border: none;
 background: rgba(0, 0, 0, 0.5); /* 배경 추가 */
 cursor: pointer;
 z-index: 2;
 padding: 0;
 display: flex;
 align-items: center;
 justify-content: center;
}

.carousel-btn:hover {
  background: rgba(0, 0, 0, 0.7);
}

.button-circle {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.carousel-btn:hover .button-circle {
  transform: scale(1.1);
}

.carousel-btn i {
  color: #000;
  font-size: 1.2rem;
}

.prev {
  left: 0;
}

.next {
  right: 0;
}

.carousel-btn:disabled {
  opacity: 0;
  cursor: default;
}

/* 반응형 디자인 */
@media (max-width: 1200px) {
  .movie-card {
    width: 200px;
  }
}

@media (max-width: 768px) {
  .movie-card {
    width: 170px;
  }
  
  .carousel-container {
    padding: 0 50px;
  }
  
  .carousel-btn {
    width: 50px;
  }
}

@media (max-width: 576px) {
  .movie-card {
    width: 140px;
  }
  
  .carousel-container {
    padding: 0 40px;
  }
  
  .carousel-btn {
    width: 40px;
  }
  
  .button-circle {
    width: 30px;
    height: 30px;
  }
}
</style>