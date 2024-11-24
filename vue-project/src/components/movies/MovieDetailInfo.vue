<template>
  <div class="container-fluid p-0">
    <!-- Backdrop Image -->
    <div class="backdrop" :style="`background-image: url(https://image.tmdb.org/t/p/original${movieDetail.backdrop_path})`">
      <div class="backdrop-overlay">
        <div class="container py-1">
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
                <button @click="toggleLike" class="like-button" :class="{ 'liked': isLiked }">
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
    <div class="Content-container">
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
        <div v-if="trailerKey" class="trailer-thumbnails">
          <div class="video-card" @click="showTrailer = true">
            <div class="thumbnail-container">
              <img 
                :src="`https://img.youtube.com/vi/${trailerKey}/maxresdefault.jpg`"
                alt="영화 예고편 썸네일"
                class="thumbnail-image"
              />
              <div class="play-overlay">
                <i class="fa-solid fa-play"></i>
              </div>
            </div>
            <div class="video-title ">
              <h3>{{ movieDetail.title }} 공식 예고편</h3>
            </div>
          </div>
        </div>
        <p v-if="noTrailerMessage">{{ noTrailerMessage }}</p>

        <!-- YouTube Modal -->
        <div v-if="showTrailer" class="trailer-modal">
          <div class="trailer-content">
            <button @click="showTrailer = false" class="close-button">×</button>
            <div class="video-container">
              <iframe 
                :src="`https://www.youtube.com/embed/${trailerKey}?autoplay=1`"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
              </iframe>
            </div>
          </div>
        </div>
      </section>

    </div>
  </div>
 </template>

<script setup>
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import axios from 'axios';
import api from '@/api';
import '@/assets/styles/movieDetail.css';

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

// 로그인된 사용자만 좋아요 가능
// const isLoggedIn = ref(localStorage.getItem('isLoggedIn') === 'true');
const isLoggedIn = ref(true); 
console.log(localStorage.getItem('isLoggedIn'));
// 좋아요 토글
const toggleLike = async () => {
  try {
    const response = await api.post(`/movies/${route.params.movieId}/likes/`);
    isLiked.value = response.data.liked;
    likeCount.value = response.data.like_count;
  } catch (error) {
    console.error('좋아요 처리 실패:', error);
    alert('로그인이 필요합니다.');
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


// YouTube 관련 상태 추가
const trailerKey = ref(null);
const showTrailer = ref(false);
const noTrailerMessage = ref('예고편이 없습니다.');

// 예고편 정보를 가져오는 함수
const loadTrailerInfo = async () => {
  try {
    const response = await axios.get(
      `https://api.themoviedb.org/3/movie/${route.params.movieId}/videos?language=ko-KR`,
      {
        headers: {
          Authorization: `Bearer ${TMDB_KEY}`,
        },
      }
    );
    
    // 한국어 예고편 우선, 없으면 영어 예고편 사용
    const trailer = response.data.results.find(
      video => 
        (video.type === 'Trailer' || video.type === 'Teaser') && 
        (video.site === 'YouTube') &&
        (video.iso_639_1 === 'ko')
    ) || response.data.results.find(
      video => 
        (video.type === 'Trailer' || video.type === 'Teaser') && 
        (video.site === 'YouTube')
    );

    if (trailer) {
      trailerKey.value = trailer.key;
      noTrailerMessage.value = ''; // 예고편 정보가 있으면 메시지 초기화
    } else {
      trailerKey.value = null;
      noTrailerMessage.value = '예고편이 없습니다.';
    }
  } catch (error) {
    console.error('예고편 정보 로드 실패:', error);
    noTrailerMessage.value = '예고편 정보를 불러오는 데 실패했습니다.';
  }
};





onMounted(() => {
  loadMovieDetail();
  loadCastInfo();
  loadTrailerInfo();
});


</script>

<style scoped>
.backdrop {
  position: relative;
  background-size: cover;
  background-position: center;
  height: 500px !important; /* !important 추가 */
  min-height: 500px !important; /* 최소 높이도 강제 지정 */
  width: 100%;
  overflow: hidden; /* 내부 컨텐츠가 넘치지 않도록 */
}

.backdrop-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  height: 300px ;
  background: linear-gradient(to right, rgba(0, 0, 0, 0.9) 0%, rgba(0, 0, 0, 0.6) 100%);
}

/* 기존 스타일들을 유지하면서 포스터 이미지 크기도 조절 */
.movie-poster {
  max-height: 350px; /* 포스터 높이도 함께 조절 */
  width: auto;
  object-fit: cover;
  margin-left: 140px;
}

.back-button {
  background: none;
  border: none;
  color: white;
  font-size: 1.1rem;
  padding: 8px 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button:hover {
  opacity: 0.8;
}

.movie-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.movie-meta {
  font-size: 1.1rem;
  opacity: 0.9;
}

.genre-badge {
  margin: 1rem 0;
}

.genre-badge .badge {
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  margin-right: 0.5rem;
}

.like-button {
  background: none;
  border: 2px solid white;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.like-button.liked {
  background-color: rgba(255, 255, 255, 0.2);
}

.like-icon {
  font-size: 1.2rem;
}

.Content-container{
  max-width: 1200px; /* 최대 너비 설정 */
  margin: 0 auto; /* 중앙 정렬 */
  padding-left: 5rem !important; /* 왼쪽 여백 */
  padding-right: 5rem !important; /* 오른쪽 여백 */
}

.cast-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1.5rem;
  padding: 0rem;
  margin: 0; /* 마진 제거 */
}

.cast-card {
  text-align: center; /* 카드 내부 텍스트 중앙 정렬 */
  
}

.cast-image-container {
  position: relative;
  width: 100%;
  aspect-ratio: 1/1;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 0.5rem; /* 이미지와 텍스트 사이 간격 */
}

.cast-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cast-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0));
  padding: 1rem 0.5rem;
  text-align: center; /* 오버레이 내부 텍스트 중앙 정렬 */
}

.cast-info {
  color: white;
}

.actor-name {
  font-weight: bold;
  font-size: 0.9rem;
  margin: 0;
  margin-bottom: 0.2rem;
}

.character-name {
  font-size: 0.8rem;
  margin: 0;
  opacity: 0.8;
}

/* 반응형 조정 */
@media (max-width: 768px) {
  .cast-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 1rem;
  }
  
  .actor-name {
    font-size: 0.8rem;
  }
  
  .character-name {
    font-size: 0.7rem;
  }
}


/* 예고편 섹션 하단 여백 추가 */
section.mb-5:last-child {
  margin-bottom: 5rem !important; /* 마지막 섹션에 더 큰 여백 추가 */
}

.trailer-thumbnails {
  padding: 0;
  margin-bottom: 3rem; /* 예고편 섹션 아래 여백 추가 */
}

.video-card {
  max-width: 800px;
  margin-bottom: 5rem; /* 비디오 카드 아래 여백 추가 */
}
</style>