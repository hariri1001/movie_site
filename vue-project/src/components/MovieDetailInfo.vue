<template>
  <div class="container">
    
   <div class="row justify-content-center text-center">
      <div class="d-flex w-100 ">
        <button @click="goToMain" class="back-button">
          <span>← 메인으로</span>
        </button>
      </div>
      <img :src="`https://image.tmdb.org/t/p/w200${movieDetail.poster_path}`" 
            class="img-fluid rounded shadow mb-4" 
            alt="영화 포스터"
            style="max-width: 300px;"/>
      <div class="container">
        <h3>{{ movieDetail.title }}</h3>
        <p>개봉일: {{ movieDetail.release_date }}</p>
        <p>러닝타임: {{ movieDetail.runtime }}</p>
        <p>TMDB 평점: {{ movieDetail.vote_average }}</p>

        <div class="like-section">
          <button 
            @click="toggleLike" 
            class="like-button"
            :class="{ 'liked': isLiked }"
          >
            <span class="like-icon">{{ isLiked ? '❤️' : '🤍' }}</span>
            <span class="like-count">{{ likeCount }}</span>
          </button>
        </div>

      </div>
      <hr>
      <div>
          <h3>장르</h3>
          <p v-for="genre in movieDetail.genres" :key="genre.id" class="badge bg-primary me-2 mb-2">{{ genre.name }}</p>
      </div>
      <hr>
      <div>
          <h3>줄거리</h3>
          <p>{{ movieDetail.overview }}</p>
      </div>
      <hr>
      <div>
          <h3>공식 예고편</h3>
          <button class="youtube-btn">
            <i class="fa-brands fa-youtube"></i>
          </button>
      </div>
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
      id: res.data.id,
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

onMounted(() => {
  loadMovieDetail();
});

//뒤로가기
import { useRouter } from 'vue-router'

const router = useRouter()

const goToMain = () => {
 router.push({ name: 'MainView' })
}


</script>

<style scoped>
.genre-badge {
  transition: background-color 0.3s ease;
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

.like-section {
  margin: 1rem 0;
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
  margin: 0 auto;
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

</style>