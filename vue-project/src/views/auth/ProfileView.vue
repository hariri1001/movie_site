<template>
  <div class="profile-container">
    <!-- 상단 프로필 섹션 -->
    <div class="profile-header">
      <!-- 왼쪽: 프로필 정보 -->
      <div class="profile-info">
        <div class="profile-image"></div>
        <p class="username">{{ store.userProfile?.username }}</p>
        
        <div class="stats">
          <p class="username">{{ store.userProfile?.first_name }}</p>
          <p class="username">{{ store.userProfile?.email }}</p>
          <p>movies: {{ likedMovies.length }}</p>
          <p>followers: 0</p>
          <p>following: 0</p>
        </div>
        <button v-if="!isEditing" @click="startEditing" class="edit-button">
          회원 정보 수정
        </button>
        <button @click="deleteAccount" class="delete-button">회원탈퇴</button>
      </div>

      <!-- 오른쪽: 좋아요한 영화 그리드 -->
      <div class="liked-content">
        <h2>내가 좋아하는 영화</h2>
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
  <h2>내가 작성한 게시글</h2>
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


    <!-- 프로필 수정 폼 -->
    <form v-if="isEditing" @submit.prevent="submitUpdate" class="profile-form">
      <div class="form-group">
        <label for="editFirstName">이름:</label>
        <input type="text" id="editFirstName" v-model="editForm.first_name">
      </div>
      
      <div class="form-group">
        <label for="editEmail">이메일:</label>
        <input type="email" id="editEmail" v-model="editForm.email">
      </div>

      <div class="form-group">
        <label for="currentPassword">현재 비밀번호:</label>
        <input type="password" id="currentPassword" v-model="editForm.currentPassword">
      </div>

      <div class="form-group">
        <label for="newPassword">새 비밀번호:</label>
        <input type="password" id="newPassword" v-model="editForm.newPassword">
      </div>

      <div class="form-group">
        <label for="confirmPassword">비밀번호 확인:</label>
        <input type="password" id="confirmPassword" v-model="editForm.confirmPassword">
      </div>

      <div class="button-group">
        <button type="submit" class="save-button">저장</button>
        <button type="button" @click="cancelEditing" class="cancel-button">취소</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import axios from 'axios';
import { useRouter } from 'vue-router';

const store = useCounterStore();
const isEditing = ref(false);
const error = ref(null);
const editForm = ref({
  first_name: '',
  email: '',
});
const likedMovies = ref([]);
const userArticles = ref([]); // 내가 작성한 게시글 데이터를 저장
const router = useRouter();

// Axios 인스턴스 생성
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터 추가
api.interceptors.request.use((config) => {
  const token = store.token;
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// 좋아요한 영화 가져오기
const fetchLikedMovies = async () => {
  try {
    error.value = null;
    const response = await api.get('/movies/liked-movies/');
    likedMovies.value = response.data;
  } catch (err) {
    console.error("좋아요한 영화를 불러오는데 실패했습니다:", err);
  }
};

// 사용자 게시글 가져오기
const fetchUserArticles = async () => {
  try {
    error.value = null;
    const response = await api.get('/api/v1/articles/user/');
    userArticles.value = response.data;
  } catch (err) {
    console.error("사용자 게시글 데이터를 불러오는데 실패했습니다:", err);
  }
};

// 상세보기 이동
const goToMovieDetail = (movieId) => {
  router.push({ name: 'MovieDetail', params: { movieId } });
};

const goToArticleDetail = (articleId) => {
  router.push({ name: 'DetailView', params: { id: articleId } });
};

// 페이지 로드 시 데이터 가져오기
onMounted(async () => {
  try {
    await store.getProfile();
    await fetchLikedMovies();
    await fetchUserArticles();
  } catch (err) {
    console.error("데이터를 불러오는데 실패했습니다:", err);
  }
});

// 프로필 수정 관련 함수
const startEditing = () => {
  editForm.value = {
    first_name: store.userProfile?.first_name || '',
    email: store.userProfile?.email || '',
  };
  isEditing.value = true;
};

const cancelEditing = () => {
  isEditing.value = false;
};

const submitUpdate = async () => {
  if (!editForm.value.email) {
    alert("이메일은 필수 입력값입니다.");
    return;
  }
  if (editForm.value.newPassword !== editForm.value.confirmPassword) {
    alert("새 비밀번호와 비밀번호 확인이 일치하지 않습니다.");
    return;
  }
  const success = await store.updateProfile(editForm.value);
  if (success) {
    isEditing.value = false;
    alert("프로필이 성공적으로 업데이트되었습니다.");
  } else {
    alert("프로필 업데이트에 실패했습니다.");
  }
};

// 계정 삭제
const deleteAccount = async () => {
  if (!confirm("정말 탈퇴하시겠습니까?")) return;
  const success = await store.deleteAccount();
  if (success) {
    router.push({ name: 'LogInView' });
    alert("회원탈퇴가 완료되었습니다.");
  } else {
    alert("회원탈퇴에 실패했습니다.");
  }
};
</script>

<style scoped>
.profile-container {
  /* max-width: 1200px; */
  width: 100%;
  margin: 0 auto;
  padding: 40px 20px;
  background-color: #1a1a1a;
  color: white;
}

.profile-header {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
}

.profile-info {
  width: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-color: #333;
  margin-bottom: 15px;
}

.username {
  font-size: 1.2em;
  margin-bottom: 10px;
}

.stats {
  text-align: center;
  margin-bottom: 20px;
  font-size: 0.9em;
  color: #ccc;
}

.delete-button {
 background-color: #dc3545;
 color: white;
 padding: 8px 16px;
 border: none;
 border-radius: 4px;
 cursor: pointer;
 margin-top: 10px;
}


.liked-content {
  flex: 1;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(120px, 1fr));
  gap: 15px;
  margin-top: 20px;
}

.movie-card {
  /* 영화 포스터 비율 (2:3) 유지 */
  aspect-ratio: 2/3;
  overflow: hidden;
  border-radius: 8px;
  background-color: #333;
  transition: transform 0.3s ease;
  /* 카드 최대 크기 제한 */
  max-width: 200px;
  justify-self: center;
}

.movie-card:hover {
  transform: scale(1.05);
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: contain; /* cover에서 contain으로 변경하여 이미지가 짤리지 않도록 */
}

.comments-section {
  margin-top: 40px;
}

.comments-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.comment-card {
  background-color: #333;
  padding: 20px;
  border-radius: 8px;
  aspect-ratio: 16/9;
}

.edit-button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

/* 기존 폼 스타일 유지 */
.profile-form {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #1a1a1a;
  padding: 40px;
  border-radius: 8px;
  width: 90%;
  max-width: 460px;
  z-index: 1000;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  color: white;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #4CAF50;
  border-radius: 4px;
  background-color: #333;
  color: white;
}

.button-group {
  display: flex;
  gap: 10px;
}

.save-button {
  background-color: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-button {
  background-color: #f44336;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

</style>