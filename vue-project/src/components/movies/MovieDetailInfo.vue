<template>
  <div class="container-fluid p-0">
    <!-- Backdrop Image -->
    <div class="backdrop" :style="`background-image: url(https://image.tmdb.org/t/p/original${movieDetail.backdrop_path})`">
      <div class="backdrop-overlay">
        <div class="container py-5">
          <div class="row">
            <!-- Back Button -->
            <div class="col-12 mb-4">
              <button @click="goToMain" class="back-button">
                <span>← 메인으로</span>
              </button>
            </div>
 
            <!-- Poster and Basic Info -->
            <div class="col-md-4">
              <img :src="`https://image.tmdb.org/t/p/w400${movieDetail.poster_path}`" 
                   class="movie-poster img-fluid rounded shadow" 
                   alt="영화 포스터"/>
            </div>
            
            <div class="col-md-8 text-white">
              <h1 class="movie-title">{{ movieDetail.title }}</h1>
              <div class="movie-meta">
                <p class="mb-2">감독: {{ director }}</p>
                <p class="mb-2">개봉일: {{ movieDetail.release_date }}</p>
                <p class="mb-2">러닝타임: {{ movieDetail.runtime }}분</p>
                <p class="mb-2">평점: {{ movieDetail.vote_average }}</p>
              </div>
              
              <!-- 장르 -->
              <div class="genre-badge">
                <span v-for="genre in movieDetail.genres" 
                      :key="genre.id" 
                      class="badge bg-primary me-2">
                  # {{ genre.name }}
                </span>
              </div>
 
              <div class="like-section">
                <button @click="toggleLike" 
                        class="like-button"
                        :class="{ 'liked': isLiked }">
                  <span class="like-icon">{{ isLiked ? '❤️' : '🤍' }}</span>
                  <span class="like-count">{{ likeCount }}</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
 
    <!-- Content Section -->
    <div class="container mt-5">
      <!-- Overview -->
      <section class="mb-5">
        <h2 class="section-title">줄거리</h2>
        <p>{{ movieDetail.overview }}</p>
      </section>
 
      <!-- Cast -->
      <section class="mb-5">
        <h2 class="section-title">출연진</h2>
        <div class="cast-grid">
          <div v-for="actor in castList" :key="actor.id" class="cast-card">
            <div class="cast-image-container">
              <img :src="actor.profile_path ? `https://image.tmdb.org/t/p/w200${actor.profile_path}` : '/public/default_profile.png'"
                   :alt="actor.name"
                   class="cast-image"/>
              <div class="cast-overlay">
                <div class="cast-info">
                  <p class="actor-name">{{ actor.name }}</p>
                  <p class="character-name">{{ actor.character }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
 
      <!-- Trailer -->
      <section class="mb-5">
        <h2 class="section-title">공식 예고편</h2>
        <button class="youtube-btn">
          <i class="fa-brands fa-youtube"></i>
        </button>
      </section>
    </div>
  </div>
 </template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import axios from 'axios';
import api from '@/api';

const TMDB_KEY = import.meta.env.VITE_TMDB_API_KEY;
const route = useRoute();
const movieDetail = ref({});
const likeCount = ref(0);
const isLiked = ref(false);

// 영화 저장 함수
const saveMovie = async (movieData) => {
  try {
    await api.post('/movies/save/', movieData);
  } catch (error) {
    console.error('영화 저장 실패:', error);
  }
};

// 좋아요 상태 로드
const loadLikeState = async () => {
  try {
    const response = await api.get(`/movies/${route.params.movieId}/likes/`);
    isLiked.value = response.data.is_liked;
    likeCount.value = response.data.like_count;
  } catch (error) {
    console.error('좋아요 상태 로드 실패:', error);
  }
};

// 좋아요 토글
const toggleLike = async () => {
  try {
    const response = await api.post(`/movies/${route.params.movieId}/likes/`);
    isLiked.value = response.data.liked;
    likeCount.value = response.data.like_count;
  } catch (error) {
    console.error('좋아요 처리 실패:', error);
  }
};

// 영화 상세 정보 로드
const loadMovieDetail = async () => {
  try {
    console.log('전달받은 movie ID:', route.params.movieId); // 디버깅용 로그 추가
    const res = await axios.get(
      `https://api.themoviedb.org/3/movie/${route.params.movieId}?language=ko-KR`,
      {
        headers: {
          Authorization: `Bearer ${TMDB_KEY}`,
        },
      }
    );
    
    movieDetail.value = res.data;
    
    // 영화 데이터 저장
    const movieData = {
      tmdb_id: res.data.id,
      title: res.data.title,
      overview: res.data.overview,
      release_date: res.data.release_date,
      vote_count: res.data.vote_count,
      vote_average: res.data.vote_average,
      poster_path: res.data.poster_path
    };
    
    await saveMovie(movieData);
    await loadLikeState();
    
  } catch (err) {
    console.error('영화 상세 정보 로드 실패:', err);
  }
};



//뒤로가기
import { useRouter } from 'vue-router'

const router = useRouter()

const goToMain = () => {
 router.push({ name: 'MainView' })
}


const castList = ref([]);
const director = ref('');
// 출연진 정보를 가져오는 함수
const loadCastInfo = async () => {
  try {
    const res = await axios.get(
      `https://api.themoviedb.org/3/movie/${route.params.movieId}/credits?language=ko-KR`,
      {
        headers: {
          Authorization: `Bearer ${TMDB_KEY}`,
        },
      }
    );
    // 주요 출연진만 필터링 (예: 상위 10명)
    castList.value = res.data.cast.slice(0, 10);
    // 감독 정보 찾기
    const directorInfo = res.data.crew.find(person => person.job === 'Director');
    director.value = directorInfo ? directorInfo.name : '정보 없음';
  } catch (err) {
    console.error('출연진 정보 로드 실패:', err);
  }
};







onMounted(() => {
  loadMovieDetail();
  loadCastInfo();
});


</script>

<style scoped>
.genre-badge {
  display: inline-block;
  margin-bottom: 10px;
  background-color: rgba(255,255,255,0.1);
  border-radius: 20px;
  font-size: 1.25rem;  /* 폰트 크기 변경 */
}

.youtube-btn {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.fa-youtube {
  color: #FF0000;
  font-size: 2rem;
}

/* 좋아요 */
.like-section {
  margin: 1rem 0;
  text-align: left; 
}

.like-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background: #f8f9fa;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 0;
}

.like-button.liked {
  background: #ffe0e0;
}

.like-icon {
  font-size: 1.2em;
}

.like-count {
  font-size: 0.9em;
  margin-left: 4px;
}

.like-button:hover {
  transform: scale(1.05);
}

/* 뒤로가기 버튼 */
.back-button {
 margin-top: 20px; /* 네브바 아래로 조정 */
 padding: 10px 10px;
 background-color: #4CAF50;
 color: white;
 border: none;
 border-radius: 4px;
 cursor: pointer;
 font-size: 1rem;
 align-self: flex-start; /* 왼쪽 정렬 */
}

.back-button:hover {
 background-color: #45a049;
}

/* 출연진 */
.cast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  padding: 20px;
  justify-items: center;
}

.cast-card {
  width: 120px;
  height: 120px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  background: #000;
}

.cast-image-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.cast-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.cast-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.overlay-content {
  text-align: center;
  color: white;
  padding: 10px;
}

.actor-name {
  font-size: 1em;
  font-weight: bold;
  margin: 0 0 5px 0;
}

.character-name {
  font-size: 0.9em;
  margin: 0;
  opacity: 0.8;
}

.backdrop {
 position: relative;
 background-size: cover;
 background-position: center;
 min-height: 600px;
}

.backdrop-overlay {
 background: rgba(0, 0, 0, 0.7);
 min-height: 600px;
}

.movie-poster {
 max-width: 100%;
 box-shadow: 0 0 20px rgba(0,0,0,0.5);
}

.section-title {
 font-size: 2rem;
 margin-bottom: 1.5rem;
 color: #ede7e7;
}

.movie-title{
  margin-bottom: 30px;
  font-size: 3.5rem;
  font-weight: 300;
  line-height: 1.2;
  text-align: left; /* 왼쪽 정렬 */
  margin-left: 0;   /* 왼쪽 마진 제거 */
}

.movie-meta{
  margin-bottom:  30px;
  font-size: 1.25rem;
}


/* 호버 효과 */
.cast-card:hover .cast-overlay {
  opacity: 1;
}

.cast-card:hover .cast-image {
  transform: scale(1.1);
}


/* 반응형 디자인 */
@media (max-width: 768px) {
  .cast-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
  
  .cast-card {
    width: 120px;
  }

  .cast-image-container {
    height: 180px;
  }

  .actor-name {
    font-size: 0.9em;
  }

  .character-name {
    font-size: 0.8em;
  }
}




</style>