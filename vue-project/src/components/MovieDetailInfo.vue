<template>
  <div class="container">
    <div class="row justify-content-center text-center mt-4">
      <img :src="`https://image.tmdb.org/t/p/w200${movieDetail.poster_path}`" 
            class="img-fluid rounded shadow mb-4" 
            alt="영화 포스터"
            style="max-width: 300px;"/>
      <div class="container">
        <h3>{{ movieDetail.title }}</h3>
        <p>개봉일: {{ movieDetail.release_date }}</p>
        <p>러닝타임: {{ movieDetail.runtime }}</p>
        <p>TMDB 평점{{ movieDetail.vote_average }}</p>

        <div> 
          <p v-if="movieDetail.like_count !== undefined">좋아요 수: {{ movieDetail.like_count }}</p>
          <button @click="toggleLike" :class="{ 'liked': isLiked }">
            <span v-if="isLiked">❤️</span>
            <span v-else>🤍</span>
            좋아요
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
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import axios from 'axios';
import api from '@/api';


const TMDB_KEY = import.meta.env.VITE_TMDB_API_KEY;
const route = useRoute();
const ID = ref(route.params.movieId);

const movieDetail = ref({like_count: 0});

const likeCount = ref(0);    // 좋아요 수 상태 추가
const isLiked = ref(false);  // 좋아요 상태 추가



const loadLikeState = async () => {
  try {
    const response = await api.get(`/movies/${route.params.movieId}/likes/`);
    isLiked.value = response.data.is_liked;
    movieDetail.value.like_count = response.data.count;
  } catch (error) {
    console.error('좋아요 상태 로드 실패:', error);
  }
};

const toggleLike = async () => {
  try {
    const response = await api.post(`/movies/${route.params.movieId}/likes/`);
    isLiked.value = response.data.liked;
    movieDetail.value.like_count = response.data.count;
  } catch (error) {
    console.error('좋아요 처리 실패:', error);
  }
};

onMounted(() => {
 axios
   .get(`https://api.themoviedb.org/3/movie/${route.params.movieId}?language=ko-KR`, {
     headers: {
       Authorization: `Bearer ${TMDB_KEY}`,
     },
   })
   .then((res) => {
    const movieData = {
      id: res.data.id,
      title: res.data.title,
      overview: res.data.overview,
      release_date: res.data.release_date,
      vote_count: res.data.vote_count,
      vote_average: res.data.vote_average,
      poster_path: res.data.poster_path
    };


    api.post('/movies/save/', movieData)  // 먼저 영화 저장
     movieDetail.value = { ...res.data, like_count: 0 }; // 기존 데이터 유지하면서 like_count 추가
     loadLikeState();
    })
   .catch((err) => {
     console.log(err);
   });
});

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
  color: #FF0000;  /* YouTube 빨간색 */
  font-size: 2rem;  /* 아이콘 크기 조절 */
}


.liked {
 color: red;
}
</style>