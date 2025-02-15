<template>
    <div class="container">
    <!-- 인기 상영작 캐러셀 -->
        <div class="carousel-container">
        <h2 class="carousel-title">POST HOT 랭킹</h2>
        <div class="carousel">
            <div class="movie-cards" :style="{ transform: `translateX(-${popularPosition}px)` }">
            <div class="movie-card" v-for="(movie, index) in popularMovies" :key="movie.id">
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
            <div>
            <i class="fas fa-chevron-left"></i>
            </div>
        </button>
        <button class="carousel-btn next" @click="movePopular('next')" :disabled="isEndOfPopular">
            <div>
            <i class="fas fa-chevron-right"></i>
            </div>
        </button>
        </div>
    </div>
</template>
  
<script setup>
import { defineProps, computed } from 'vue';

const props = defineProps({
  popularMovies: {
    type: Array,
    required: true
  },
  movePopular: {
    type: Function,
    required: true
  },
  isEndOfPopular: {
    type: Boolean,
    required: true
  },
  popularPosition: {
    type: Number,
    required: true
  }
});

const isEndOfCarousel = computed(() => {
  if (!props.popularMovies.length) return true;
  return props.popularPosition >= (props.popularMovies.length - visibleCards) * 250;
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

/* 순위 숫자 */
.rank-number {
position: absolute;
bottom: -30px; /* 아래쪽으로 더 많이 내려감 */
right: 20px; /* 오른쪽에서 10px 왼쪽으로 */
font-size: 130px; /* 기존 크기 유지 */
font-weight: bold; /* 기존 굵기 유지 */
color: rgba(255, 255, 255, 0.8); /* 기존 스타일 유지 */
text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5); /* 기존 그림자 유지 */
font-style: italic; /* 기존 이탤릭체 유지 */
z-index: 1; /* 카드 이미지 위에 표시 */
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