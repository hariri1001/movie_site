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
            <div class="video-title">
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

</style>