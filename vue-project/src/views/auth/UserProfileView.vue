<template>
  <div class="profile-container">
    <!-- 프로필 섹션 -->
    <div class="profile-header">
      <!-- 왼쪽: 프로필 이미지와 정보 -->
      <div class="left-section">
        <div class="profile-image-container">
          <img 
            :src="profileImageUrl"
            :alt="profileUser?.username + '의 프로필 이미지'"
            class="profile-image"
          />
        </div>
        <!-- 팔로우 버튼 -->
        <div class="button-group">
          <button 
            v-if="showFollowButton"
            @click="handleFollow" 
            class="action-button"
            :class="{ 'following': isFollowing }"
          >
            {{ isFollowing ? '팔로잉' : '팔로우' }}
          </button>
        </div>
      </div>

      <!-- 오른쪽: 사용자 정보 -->
      <div class="right-section">
        <div class="user-info">
          <p>{{ profileUser?.first_name || '이름 없음' }}</p>
          <p>ID : {{ profileUser?.username }}</p>
          <p>EMAIL : {{ profileUser?.email }}</p>
        </div>
        <div class="stats">
          <p>movies: {{ likedMovies.length }}</p>
          <p>followers: {{ profileUser?.followers_count || 0 }}</p>
          <p>following: {{ profileUser?.following_count || 0 }}</p>
        </div>
      </div>
    </div>

    <!-- 좋아하는 영화 섹션 -->
    <div class="content-section">
      <h3>좋아하는 영화</h3>
      <div v-if="likedMovies.length === 0" class="no-content">
        좋아요한 영화가 없습니다.
      </div>
      <div v-else class="movie-grid">
        <div 
          v-for="movie in likedMovies" 
          :key="movie.id" 
          class="movie-card"
          @click="goToMovieDetail(movie.tmdb_id)"
        >
          <img 
            :src="`https://image.tmdb.org/t/p/w400${movie.poster_path}`" 
            :alt="movie.title" 
            class="movie-poster"
          >
        </div>
      </div>
    </div>

    <!-- 작성한 게시글 섹션 -->
    <div class="content-section">
      <h3>작성한 코멘트</h3>
      <div class="article-grid">
        <div 
          v-for="article in userArticles" 
          :key="article.id" 
          class="article-card"
        >
          <h3>{{ article.title }}</h3>
          <p>{{ article.content }}</p>
          <button @click="goToArticleDetail(article.id)" class="view-button">
            자세히 보기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useProfileStore } from '@/stores/profile';
import { useMovieStore } from '@/stores/movie';
import { useRoute, useRouter } from 'vue-router';


const authStore = useAuthStore();
const profileStore = useProfileStore();
const movieStore = useMovieStore();

const route = useRoute();
const router = useRouter();

const profileUser = ref(null);
const likedMovies = ref([]);
const userArticles = ref([]);
const error = ref(null);

// 팔로우 버튼 표시 여부
const showFollowButton = computed(() => {
  return profileStore.userProfile && 
         profileUser.value && 
         profileStore.userProfile.username !== profileUser.value.username;
});

// 팔로우 상태
const isFollowing = computed(() => {
  return profileUser.value?.is_followed || false;
});

// 팔로우/언팔로우 처리
const handleFollow = async () => {
  try {
    await profileStore.toggleFollow(profileUser.value.username);
    // 프로필 정보 새로고침
    await loadProfileData();
  } catch (error) {
    console.error('팔로우 처리 실패:', error);
  }
};


// 프로필 데이터 로드
const loadProfileData = async () => {
  try {
    const username = route.params.username;
    await profileStore.getProfile();

    // 프로필 정보 로드
    const profileResponse = await profileStore.getUserProfile(username);
    console.log('프로필 응답:', profileResponse); // 응답 데이터 확인
    profileUser.value = profileResponse;

    // 다른 사용자가 작성한 게시글 목록 로드
    userArticles.value = await profileStore.getUserArticles(username);
    
    // 좋아요한 영화 목록 로드 - MovieStore 사용
    try {
      likedMovies.value = await movieStore.getUserLikedMovies(username);
    } catch (error) {
      console.error('좋아요한 영화 로드 실패:', error);
      likedMovies.value = [];
    }
  } catch (error) {
    console.error('프로필 데이터 로드 실패:', error);
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
    return `${profileStore.API_URL}${profileUser.value.profile_image}`;
  }
  return '/public/default_profile.png';
});


</script>

<style scoped>
.profile-container {
  max-width: 700px;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #1a1a1a;
  min-height: 100vh;
}

.profile-header {
  display: flex;
  gap: 20px;
  background-color: #272727;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 25px;
}

.left-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
  flex-shrink: 0;
  margin-left: 20px;
}

.profile-image-container {
  width: 150px;
  height: 150px;
}

.profile-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.button-group {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  justify-content: center;
}

.action-button {
  padding: 6px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  white-space: nowrap;
  background-color: transparent;
  border: 1px solid #ead200;
  color: #ffffff;
  width: auto;
  min-width: 100px;
  text-align: center;
}

.action-button:hover {
  background-color: #ead200;
  color: #1a1a1a;
}

.right-section {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-left: 40px;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.user-info p {
  margin: 0;
  color: white;
  font-size: 1.0rem;
}

.stats {
  display: flex;
  gap: 15px;
  color: #ccc;
  margin-bottom: 15px;
}

.stats p {
  margin: 0;
}

/* 콘텐츠 섹션 스타일 */
.content-section {
  background-color: #272727;
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.content-section h3 {
  color: white;
  margin-top: 0;
  margin-bottom: 20px;
}

/* 영화 그리드 */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(4, 140px);
  gap: 15px;
  margin-top: 20px;
  justify-content: center;
  border-radius: 8px;
}

.movie-card {
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
  background-color: #1a1a1a;
  width: 140px;
  height: 210px;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: fill;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  margin-left: 0 !important;
}

.movie-card:hover {
  transform: scale(1.05);
}

/* 게시글 그리드 */
.article-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 11px;
}

.article-card {
  background-color: #333;
  padding: 12px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.article-card h3 {
  color: white;
  margin: 0 0 10px 0;
  font-size: 1.15rem;
}

.article-card p {
  color: #ccc;
  margin: 0 0 15px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-size: 0.9rem;
}

.view-button {
  background: none;
  border: 1px solid #ead200;
  color: #ffffff;
  padding: 4px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  margin-left: auto;
  display: block;
}

.view-button:hover {
  background-color: #ead200;
  color: rgb(3, 3, 3);
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    align-items: center;
  }

  .left-section {
    align-items: center;
  }

  .button-group {
    flex-direction: column;
    width: 100%;
  }

  .user-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 10px;
  }

  .stats {
    justify-content: center;
  }

  .movie-grid {
    grid-template-columns: repeat(2, 140px);
  }
}

.no-content {
  text-align: center;
  padding: 20px;
  color: #ccc;
  background-color: #333;
  border-radius: 8px;
}
</style>