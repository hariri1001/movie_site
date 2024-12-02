<template>
  <div class="profile-container">
    <!-- 프로필 섹션 -->
    <div class="profile-header">
      <!-- 왼쪽: 프로필 이미지와 버튼들 -->
      <div class="left-section">
        <div class="profile-image-container">
          <img 
            :src="profileStore.userProfile?.profile_image || defaultImage" 
            :key="Date.now()"
            alt="프로필 이미지" 
            class="profile-image" 
            @error="handleImageError"
          />
        </div>
        <!-- 버튼 그룹을 이미지 아래로 이동 -->
        <div class="button-group">
          <button @click="triggerFileInput" class="action-button image">이미지 변경</button>
          
          <input 
            type="file" 
            @change="handleImageUpload" 
            accept="image/*"
            ref="fileInputRef" 
            style="display: none"
          >
        </div>
      </div>

      <!-- 오른쪽: 사용자 정보 -->
      <div class="right-section">
        <div class="user-info">
          <p>{{ profileStore.userProfile?.first_name || '이름 없음' }}</p>
          <p>ID : {{ profileStore.userProfile?.username }}</p>
          <p>EMAIL : {{ profileStore.userProfile?.email }}</p>
        </div>
        <div class="stats">
          <p>movies: {{ likedMovies.length }}</p>
          <p>followers: {{ profileStore.userProfile?.followers_count || 0 }}</p>
          <p>following: {{ profileStore.userProfile?.followings_count || 0 }}</p>
        </div>
        <div class="right-section-buttons">
          <button v-if="!isEditing" @click="startEditing" class="action-button">회원 정보 수정</button>
          <button @click="deleteAccount" class="action-button delete">회원탈퇴</button>
        </div>
      </div>
    </div>

    <!-- 좋아하는 영화 섹션 -->
    <div class="content-section">
      <h3>내가 좋아하는 영화</h3>
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
      <h3>내가 작성한 코멘트</h3>
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

    <!-- 프로필 수정 모달 (기존과 동일) -->
    <div v-if="isEditing" class="modal-overlay">
      <form @submit.prevent="submitUpdate" class="profile-form">
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
  </div>
</template>




<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useProfileStore } from '@/stores/profile';
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { useRouter } from 'vue-router';
import '@/assets/styles/profile.css'

const authStore = useAuthStore();
const profileStore = useProfileStore();
const movieStore = useMovieStore();
const router = useRouter();

const fileInputRef = ref(null); 
const isEditing = ref(false);
const error = ref(null);
const editForm = ref({
  first_name: '',
  email: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
});
const likedMovies = ref([]);
const userArticles = ref([]); // 내가 작성한 게시글 데이터를 저장


// django로 api요청
const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터 추가
// store에서 토큰을 가져와서 헤더에 추가
api.interceptors.request.use((config) => {
  const token = authStore.token;
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
    await profileStore.getProfile();
    
    console.log('프로필 데이터:', profileStore.userProfile);
    await fetchLikedMovies();
    await fetchUserArticles();
  } catch (err) {
    console.error("데이터를 불러오는데 실패했습니다:", err);
  }
});


// ***프로필 수정 관련 함수***
const startEditing = () => {
  editForm.value = {
    first_name: profileStore.userProfile?.first_name || '',
    email: profileStore.userProfile?.email || '',
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
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
  const success = await profileStore.updateProfile(editForm.value);
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
  const success = await profileStore.deleteAccount();
  if (success) {
    router.push({ name: 'LogInView' });
    alert("회원탈퇴가 완료되었습니다.");
  } else {
    alert("회원탈퇴에 실패했습니다.");
  }
};


// ***프로필 이미지 업로드***
const defaultImage = '/public/default_profile.png'
// const fileInput = ref(null)

// 파일 입력 트리거 함수
const triggerFileInput = () => {
  if (fileInputRef.value) {
    fileInputRef.value.click();
  }
};

const handleImageError = (e) => {
  console.error('이미지 로드 실패. 현재 src:', e.target.src);
  e.target.src = defaultImage;
};


// 이미지 업로드 처리 함수
const handleImageUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  try {
    // store의 updateProfileImage 메서드 사용
    const success = await profileStore.updateProfileImage(file);
    
    if (success) {
      console.log('이미지 업로드 성공');
    } else {
      alert('이미지 업로드에 실패했습니다.');
    }
  } catch (error) {
    console.error('이미지 업로드 중 오류 발생:', error);
    alert('이미지 업로드 중 오류가 발생했습니다.');
  }
};
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
  /* border: 2px solid #ead200; */
}

.button-group {
  display: flex;
  gap: 8px;  /* 버튼 사이의 간격 */
  margin-top: 10px;
  justify-content: center;
}

.action-button {
    /* 버튼들이 동일한 너비를 가지도록 */
  padding: 6px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  white-space: nowrap;

}

.action-button {
  background-color: transparent;
  border: 1px solid #ead200;
  color: #ffffff;
}

.action-button:hover {
  background-color: #ead200;
  color: #1a1a1a;
}

.action-button.image {
  width: auto; /* 버튼 크기를 내용에 맞게 조정 */
  min-width: 100px; /* 최소 너비 설정 */
  text-align: center; /* 텍스트 중앙 정렬 */
}

.action-button.delete {
  border: 1px solid #ead200;
}

.action-button.delete:hover {
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

.right-section-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end; /* 오른쪽 정렬 */
  margin-top: auto; /* 버튼들을 아래쪽으로 밀어냄 */
}

.right-section-buttons .action-button {
  width: auto; /* 버튼 너비를 내용에 맞게 조정 */
}



/* 나머지 스타일은 이전과 동일 */
.content-section {
  background-color: #272727;
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 30px;
  
}

.content-section h2 {
  color: white;
  margin-top: 0;
  margin-bottom: 20px;
}



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




.article-grid {
  display: grid;
  grid-template-columns: repeat(1, 1fr);  /* 2열로 변경 */
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
  font-size: 1.15rem; /* 제목 크기 축소 */
}

.article-card p {
  color: #ccc;
  margin: 0 0 15px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-size: 0.9rem; /* 본문 텍스트 크기 축소 */
}

.view-button {
  background: none;
  border: 1px solid #ead200;
  color: #ffffff;
  padding: 4px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  margin-left: auto; /* 버튼을 오른쪽으로 밀어냄 */
  display: block;
}

.view-button:hover {
  background-color: #ead200;
  color: rgb(3, 3, 3);
}

/* 모달 스타일 */
.profile-form {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #272727;
  padding: 30px;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  z-index: 1001;
  color: white;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: white;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #333;
  color: white;
}

.save-button, .cancel-button {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  border: 1px solid #ead200;
  background-color: transparent;
  color: white;
}

.save-button:hover, .cancel-button:hover {
  background-color: #ead200;
  color: #1a1a1a;
}

/* 모달 오버레이 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}



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
}
</style>