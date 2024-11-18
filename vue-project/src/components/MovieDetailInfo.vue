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

          <button @click="toggleLike" class="btn btn-outline-danger">
            <i class="fas fa-heart"></i>
            좋아요 {{ likeCount }}
          </button>
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
import axios from "axios";
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

const TMDB_KEY = import.meta.env.VITE_TMDB_API_KEY;
const route = useRoute();
const ID = ref(route.params.movieId);
// const movieDetail = ref([]);
const movieDetail = ref({}); // 빈 배열([])이 아닌 빈 객체({})로 초기화
const likeCount = ref(0);    // 좋아요 수 상태 추가
const isLiked = ref(false);  // 좋아요 상태 추가

// onMounted(() => {
//   axios
//     .get(`https://api.themoviedb.org/3/movie/${route.params.movieId}?language=ko-KR`, {
//       headers: {
//         Authorization: `Bearer ${TMDB_KEY}`,
//       },
//     })
//     .then((res) => {
//       movieDetail.value = res.data;
//       console.log(res.data);
//     })
//     .catch((err) => {
//       console.log(err);
//     });
// });

// 로컬 스토리지에서 좋아요 상태 불러오기
const loadLikeState = () => {
  const storedLikes = localStorage.getItem('movieLikes');
  if (storedLikes) {
    const likes = JSON.parse(storedLikes);
    if (likes[ID.value]) {
      isLiked.value = true;
      likeCount.value = likes[ID.value];
    }
  }
};

// 좋아요 상태 저장하기
const saveLikeState = () => {
  const storedLikes = localStorage.getItem('movieLikes');
  const likes = storedLikes ? JSON.parse(storedLikes) : {};
  
  if (isLiked.value) {
    likes[ID.value] = likeCount.value;
  } else {
    delete likes[ID.value];
  }
  
  localStorage.setItem('movieLikes', JSON.stringify(likes));
};

// 좋아요 토글 함수
const toggleLike = () => {
  isLiked.value = !isLiked.value;
  if (isLiked.value) {
    likeCount.value += 1;
  } else {
    likeCount.value = Math.max(0, likeCount.value - 1);
  }
  saveLikeState();
};

onMounted(() => {
  // 영화 정보 가져오기
  axios
    .get(`https://api.themoviedb.org/3/movie/${route.params.movieId}?language=ko-KR`, {
      headers: {
        Authorization: `Bearer ${TMDB_KEY}`,
      },
    })
    .then((res) => {
      movieDetail.value = res.data;
      console.log(res.data);
      // 영화 정보를 가져온 후 좋아요 상태 불러오기
      loadLikeState();
    })
    .catch((err) => {
      console.log(err);
    });
});

// ID가 변경될 때마다 좋아요 상태 다시 불러오기
watch(ID, () => {
  loadLikeState();
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
</style>
