<template>
  <div class="profile-container">
    <!-- 상단 프로필 섹션 -->
    <div class="profile-header">

      <!-- 왼쪽: 프로필 정보 -->
      <div class="profile-info">
        <!-- 프로필이미지 업로드 -->
        <div class="profile-image-section">
          <img :src="store.userProfile?.profile_image ? `${store.API_URL}${store.userProfile.profile_image}` : 
              '/public/default_profile.png'" alt="프로필 이미지" class="profile-image">
          <input type="file" @change="handleImageUpload" accept="image/*" ref="fileInput" style="display: none">
          <button @click="$refs.fileInput.click()">이미지 변경</button>
        </div>



        <p class="username">{{ store.userProfile?.username }}</p>
        <p class="username">{{ store.userProfile?.first_name || '이름 없음' }}</p>
        <div class="stats">
          
          <p class="username">{{ store.userProfile?.email }}</p>
          <p>movies: {{ likedMovies.length }}</p>
          <p>followers: {{ store.userProfile?.followers_count || 0 }}</p>
          <p>following: {{ store.userProfile?.followings_count || 0 }}</p>
        </div>
        <button v-if="!isEditing" @click="startEditing" class="edit-button">
          회원 정보 수정
        </button>
        <button @click="deleteAccount" class="delete-button">회원탈퇴</button>
      </div>

      <!-- 오른쪽: 좋아요한 영화 그리드 -->
      <div class="articles-content">
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
import '@/assets/styles/profile.css'

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
    
    console.log('프로필 데이터:', store.userProfile);
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

// 프로필 이미지 상태 관리
const defaultImage = '/public/default_profile.png'

// 파일 입력 참조
const fileInput = ref(null)

// 이미지 업로드 처리 함수
const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('image', file)

  try {
    const response = await axios.post(
      `${store.API_URL}/api/v1/accounts/profile/image/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Token ${store.token}`,
        },
      }
    )
    console.log('이미지 업로드 성공:', response.data)
    // 프로필 정보 새로고침
    await store.getProfile()
  } catch (error) {
    console.error('이미지 업로드 실패:', error)
  }
}






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
}

.profile-info {
  flex: 0 0 300px;
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

.content-grid {
  display: grid;
  /* 5개의 열로 고정 */
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
  height: auto;
  border-radius: 8px;
}

/* 게시글 섹션 스타일 */
.comments-section {
  width: 100%;
}

.comments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.comment-card {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comment-content h3 {
  margin: 0 0 10px 0;
  font-size: 1.2em;
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
  border-radius: 4px;
  cursor: pointer;
}

.comment-content button:hover {
  background: #0056b3;
}

.no-movies {
  text-align: center;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
  color: #666;
}

h2 {
  margin: 0 0 20px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #eee;
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

/* 프로필 수정 폼 스타일 */
.profile-form {
  margin-top: 20px;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.button-group {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.save-button, .cancel-button {
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-button {
  background: #28a745;
  color: white;
}

.cancel-button {
  background: #dc3545;
  color: white;
}

.edit-button, .delete-button {
  width: 100%;
  margin-top: 10px;
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-button {
  background: #007bff;
  color: white;
}

.delete-button {
  background: #dc3545;
  color: white;
  margin-top: 10px;
}

/* 반응형 디자인을 위한 미디어 쿼리 추가 */
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
