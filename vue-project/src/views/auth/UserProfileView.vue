<template>
  <div class="profile-container">
    <!-- 상단 프로필 섹션 -->
    <div class="profile-header">
      <!-- 왼쪽: 프로필 정보 -->
      <div class="profile-info">
        <!-- 프로필이미지 -->
        <div class="profile-image-section">
          <img :src="profileUser?.profile_image ? `${store.API_URL}${profileUser.profile_image}` : 
              '/public/default_profile.png'" alt="프로필 이미지" class="profile-image">
        </div>

        <p class="username">{{ profileUser?.username }}</p>
        
        <div class="stats">
          <p class="username">{{ profileUser?.first_name }}</p>
          <p class="username">{{ profileUser?.email }}</p>
          <p>movies: {{ likedMovies.length }}</p>
          <p>followers: {{ profileUser?.followers_count || 0 }}</p>
          <p>following: {{ profileUser?.following_count || 0 }}</p>
        </div>
        
        <!-- 팔로우 버튼 (본인 프로필이 아닐 때만 표시) -->
        <button 
          v-if="showFollowButton"
          @click="handleFollow" 
          :class="['follow-button', { 'following': isFollowing }]"
        >
          {{ isFollowing ? '팔로잉' : '팔로우' }}
        </button>
      </div>

      <!-- 오른쪽: 좋아요한 영화 그리드 -->
      <div class="liked-content">
        <h2>좋아하는 영화</h2>
        <div v-if="likedMovies.length === 0" class="no-movies">
            좋아요한 영화가 없습니다.
        </div>
        <div v-else class="content-grid">
          <div v-for="movie in likedMovies" :key="movie.id" class="movie-card" @click="goToMovieDetail(movie.tmdb_id)">
            <img :src="`https://image.tmdb.org/t/p/w200${movie.poster_path}`" :alt="movie.title" class="movie-poster">
          </div>
        </div>
      </div>
    </div>

    <div class="comments-section">
      <h2>작성한 게시글</h2>
      <div class="comments-grid">
        <div class="comment-card" v-for="article in userArticles" :key="article.id">
          <div class="comment-content">
            <h3>{{ article.title }}</h3>
            <p>{{ article.content }}</p>
            <button @click="goToArticleDetail(article.id)">자세히 보기</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import '@/assets/styles/profile.css'

const store = useCounterStore();
const route = useRoute();
const router = useRouter();

const profileUser = ref(null);
const likedMovies = ref([]);
const userArticles = ref([]);
const error = ref(null);

// 팔로우 버튼 표시 여부
const showFollowButton = computed(() => {
  return store.userProfile && 
         profileUser.value && 
         store.userProfile.username !== profileUser.value.username;
});

// 팔로우 상태
const isFollowing = computed(() => {
  return profileUser.value?.is_followed || false;
});

// API 설정
const api = axios.create({
  baseURL: store.API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = store.token;
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// 프로필 데이터 로드
const loadProfileData = async () => {
  try {
    const username = route.params.username;
    // 프로필 정보 로드
    const profileResponse = await store.getUserProfile(username);
    profileUser.value = profileResponse;

    // 사용자의 게시글 목록 로드
    const articlesResponse = await api.get('/api/v1/articles/user/', {
      params: { username }
    });
    userArticles.value = articlesResponse.data;

    // 좋아요한 영화 목록 로드
    const moviesResponse = await api.get('/movies/liked-movies/');
    likedMovies.value = moviesResponse.data;
  } catch (error) {
    console.error('프로필 데이터 로드 실패:', error);
  }
};

// 팔로우/언팔로우 처리
const handleFollow = async () => {
  try {
    await store.toggleFollow(profileUser.value.username);
    // 프로필 정보 새로고침
    await loadProfileData();
  } catch (error) {
    console.error('팔로우 처리 실패:', error);
  }
};

// 상세보기 이동
const goToMovieDetail = (movieId) => {
  router.push({ name: 'MovieDetail', params: { movieId } });
};

const goToArticleDetail = (articleId) => {
  router.push({ name: 'DetailView', params: { id: articleId } });
};

onMounted(() => {
  loadProfileData();
});
</script>

<style scoped>
.follow-button {
  padding: 8px 20px;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  background-color: #1da1f2;
  color: white;
  font-weight: bold;
  margin-top: 10px;
}

.follow-button.following {
  background-color: #e0e0e0;
}
</style>