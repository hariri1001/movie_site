<template>
  <div class="container">
    <!-- 평점 많이 받은 영화 -->
    
    <div class="carousel-container">
      <h2 class="carousel-title">최고 평점 작품</h2>
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

});
</script>

<style scoped>
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 0px;
  
}

.carousel-container {
  position: relative;
  padding: 0 30px; /* 버튼 공간을 더 확보 */
  margin: 20px 0;
  overflow: hidden;

  /* 컨테이너 너비 고정 */
  max-width: 1400px; /* 중앙 정렬된 너비 */
  margin: 20px auto;
}

.carousel {
  width: 100%;
  overflow: hidden;
  margin-bottom: 30px;
  margin-top: 20px;
}

.movie-cards {
  display: flex;
  transition: transform 0.3s ease;
}


.movie-card {
  flex: 0 0 auto;
  width: 250px; /* 카드 간격 감소 */
  margin-right: 20px; /* 카드 간격 */
  margin-bottom: 20px;
  transition: transform 0.3s ease;
  position: relative; /* position 추가 */
  max-width: none; /* max-width 제한 해제 */
  aspect-ratio: 2 / 3;
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
  border-radius: 8px; /* 둥근 모서리 */
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.movie-card:hover .card-img-top {
  transform: scale(1.08);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}


.carousel-btn {
  position: absolute;
  top: 50%; /* 버튼을 수직 중앙 정렬 */
  transform: translateY(-50%);
  width: 60px;
  height: 60px;
  border: none;
  background: transparent; /* 배경 제거 */
  cursor: pointer;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease; /* 호버 시 크기 조정만 유지 */
}

.carousel-btn:hover {
  transform: translateY(-50%) scale(1.1); /* 버튼 크기 확대 */
}

.carousel-btn i {
  color: white; /* 화살표를 흰색으로 */
  font-size: 2rem; /* 화살표 크기 */
  transition: color 0.3s ease; /* 호버 시 색상 전환 효과 */
}

.carousel-btn:hover i {
  color: rgba(255, 255, 255, 0.7); /* 호버 시 약간 더 밝은 흰색 */
}

.prev {
  left: 10px;
}

.next {
  right: 10px;
}

.carousel-btn:disabled {
  opacity: 0.3; /* 비활성화된 버튼은 흐리게 표시 */
  cursor: not-allowed;
}

/* 반응형 디자인 */
@media (max-width: 1200px) {
  .movie-card {
    width: 220px;
  }

  .rank-number {
    font-size: 80px;
  }

  .carousel-btn {
    width: 50px;
    height: 50px;
  }

  .carousel-btn i {
    font-size: 1.2rem;
  }
}

@media (max-width: 768px) {
  .movie-card {
    width: 170px;
  }

  .carousel-container {
    padding: 0 50px;
  }

  .rank-number {
    font-size: 60px;
  }

  .carousel-btn {
    width: 45px;
    height: 45px;
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
    height: 40px;
  }

  .carousel-btn i {
    font-size: 1rem;
  }

  .rank-number {
    font-size: 50px;
  }
}
</style>