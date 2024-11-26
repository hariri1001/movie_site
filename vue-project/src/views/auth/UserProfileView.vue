<template>
  <div class="profile-container">
    <!-- 상단 프로필 섹션 -->
    <div class="profile-header">
      <!-- 왼쪽: 프로필 정보 -->
      <div class="profile-info">
        <!-- 프로필이미지 -->
        <div class="profile-image-section">
          <img 
      :src="profileImageUrl" 
      :alt="profileUser?.username + '의 프로필 이미지'" 
      class="profile-image"
    >
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

      <!-- 오른쪽: 컨텐츠 영역 -->
      <div class="articles-content">
        <!-- 좋아요한 영화 섹션 -->
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

        <!-- 작성한 게시글 섹션 -->
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
    console.log('프로필 응답:', profileResponse); // 응답 데이터 확인
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




const profileImageUrl = computed(() => {
  if (profileUser.value?.profile_image) {
    // 전체 URL이 이미 포함된 경우
    if (profileUser.value.profile_image.startsWith('http')) {
      return profileUser.value.profile_image;
    }
    // 상대 경로인 경우 API_URL과 결합
    return `${store.API_URL}${profileUser.value.profile_image}`;
  }
  return '/public/default_profile.png';
});
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-header {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
  margin-top: 30px;
  /* border: 1px solid #00ba19; */
  border-radius: 8px;
  padding: 40px;
  background-color: #252525;
}

.profile-info {
  flex: 0 0 300px;
}

/* 프로필 이미지 관련 스타일 */
.profile-image-section {
  margin-bottom: 20px;
  text-align: center;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  margin-bottom: 10px;
  object-fit: cover;
}

/* 팔로우 버튼 스타일 수정 */
.follow-button {
  width: 100%;
  margin-top: 10px;
  padding: 8px 15px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  background: #007bff;
  color: white;
}

.follow-button.following {
  background: #005fc4;
}

/* 좋아요한 영화 섹션 */
.liked-content {
  margin-bottom: 30px;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
}

.movie-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.movie-card:hover {
  transform: scale(1.05);
}

.movie-poster {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  object-fit: cover;
}

/* 게시글 섹션 */
.comments-section {
  width: 100%;
}

.comments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.comment-card {
  background: #1a1a1a;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  /* border: 1px solid #00ba19; */
}

.comment-content h3 {
  margin: 0 0 10px 0;
  font-size: 1.2em;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.comment-content p {
  margin: 0 0 15px 0;
  font-size: 0.9em;
  color: #666;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.comment-content button {
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 8px;
  cursor: pointer;
}

.comment-content button:hover {
  background: #0056b3;
}

.no-movies {
  text-align: center;
  padding: 20px;
  background: #1a1a1a;
  border-radius: 8px;
  color: #F8F9FA;
}

h2 {
  margin: 0 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #d2d3d2;
  color: #F8F9FA;
}

/* 통계 스타일 */
.stats {
  margin: 20px 0;
  color: #F8F9FA;
}

.stats p {
  margin: 5px 0;
}

.username {
  font-size: 1.2em;
  font-weight: bold;
  margin: 10px 0;
  color: #F8F9FA;
}

.articles-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.liked-content {
  margin-bottom: 30px;
}


/* 반응형 디자인 */
@media (max-width: 1200px) {
  .content-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 992px) {
  .content-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .profile-header {
    flex-direction: column;
  }
  
  .profile-info {
    flex: none;
    width: 100%;
  }
}
</style>