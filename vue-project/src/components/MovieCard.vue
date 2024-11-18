<template>
  <div class="container">
    <div class="carousel-container">
      <div class="carousel" ref="carousel">
        <div class="movie-cards" :style="{ transform: `translateX(-${currentPosition}px)` }">
          <div class="movie-card" v-for="movie in movies" :key="movie.id">
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
      <!-- 넷플릭스 스타일의 버튼 -->
      <button class="carousel-btn prev" @click="moveCarousel('prev')" :disabled="currentPosition === 0">
        <div class="button-circle">
          <i class="fas fa-chevron-left"></i>
        </div>
      </button>
      <button class="carousel-btn next" @click="moveCarousel('next')" :disabled="isEndOfCarousel">
        <div class="button-circle">
          <i class="fas fa-chevron-right"></i>
        </div>
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import axios from 'axios';

const movies = ref([]);
const TMDB_KEY = import.meta.env.VITE_TMDB_API_KEY;
const currentPosition = ref(0);
const carousel = ref(null);
const cardWidth = 250; // 카드 하나의 너비 (margin 포함)
const visibleCards = 5; // 한 번에 보여질 카드 수

const isEndOfCarousel = computed(() => {
  if (!movies.value.length) return true;
  return currentPosition.value >= (movies.value.length - visibleCards) * cardWidth;
});

const moveCarousel = (direction) => {
  if (direction === 'next' && !isEndOfCarousel.value) {
    currentPosition.value += cardWidth;
  } else if (direction === 'prev' && currentPosition.value > 0) {
    currentPosition.value -= cardWidth;
  }
};

onMounted(() => {
  // API 요청 방식 수정
  axios.get('https://api.themoviedb.org/3/movie/top_rated', {
    headers: {
      Authorization: `Bearer ${TMDB_KEY}`  // Bearer 토큰 방식으로 변경
    },
    params: {
      language: 'ko-KR',
      page: '1'
    }
  })
  .then((response) => {
    movies.value = response.data.results;
    console.log('영화 데이터:', response.data);
  })
  .catch((error) => {
    console.error('API 요청 오류:', error);
  });
});
</script>

<style scoped>
.carousel-container {
  position: relative;
  padding: 0 60px; /* 버튼 공간 확보를 위해 패딩 증가 */
  margin: 20px 0;
  overflow: hidden;
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
  width: 230px;
  margin-right: 10px;
  transition: transform 0.3s ease;
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

/* 넷플릭스 스타일 버튼 */
.carousel-btn {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 60px; /* 버튼 영역 넓히기 */
  border: none;
  background: rgba(0, 0, 0, 0.5); /* 반투명 검정 배경 */
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 2;
  padding: 0;
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