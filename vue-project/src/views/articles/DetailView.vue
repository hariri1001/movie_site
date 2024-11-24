
<template>
  <div class="review-detail-container">
    <h1>영화 리뷰</h1>
    <div v-if="store.currentArticle" class="review-content">
      <div class="movie-info">
        <div class="movie-content">
          <!-- 포스터 이미지 추가 -->
          <div class="movie-poster-container">
            <img 
              v-if="posterUrl" 
              :src="posterUrl"
              :alt="store.currentArticle.movieTitle"
              class="movie-poster"
              @error="handleImageError"
            />
            <div v-else class="poster-placeholder">
              이미지 없음
            </div>

            <h2>{{ store.currentArticle.movie_title }}</h2>
          </div>

          <div class="review-main">
            <div class="rating-display">
              <div class="stars">
                <span 
                  v-for="star in 5" 
                  :key="star"
                  class="star"
                  :class="{ filled: star <= Math.ceil(store.currentArticle.rating) }"
                >★</span>
              </div>
              <span class="rating-text">{{ store.currentArticle.rating }} / 5</span>
            </div>
            <p class="review-text">{{ store.currentArticle.content }}</p>
            <p class="review-author">
              <strong>작성자 : </strong>
              <span 
                @click="goToUserProfile(store.currentArticle.author)" 
                class="author-link"
              >
                {{ store.currentArticle.author }}
              </span>
            </p>
          </div>
        </div>
      </div>

      

      <div class="button-container">
        <button @click="goBackToList" class="back-button">목록으로</button>
        <template v-if="isAuthor">
          <button @click="editArticle" class="edit-button">수정</button>
          <button @click="deleteArticle" class="delete-button">삭제</button>
        </template>
      </div>

      <div class="comments-section">
        <h3>댓글</h3>
        
        <div class="comment-form">
          <textarea 
            v-model="newComment" 
            placeholder="이 리뷰에 대한 의견을 남겨주세요"
            class="comment-input"
          ></textarea>
          <button @click="submitComment" class="comment-submit-btn">댓글 작성</button>
        </div>

        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <span class="comment-author">{{ comment.author }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p class="comment-content">{{ comment.content }}</p>
            <button 
              v-if="comment.author === store.userProfile?.username" 
              @click="deleteComment(comment.id)"
              class="comment-delete-btn"
            >
              삭제
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRoute, useRouter } from 'vue-router';

const store = useCounterStore();
const route = useRoute();
const router = useRouter();
const comments = ref([]);
const newComment = ref('');

const isAuthor = computed(() => {
  return store.currentArticle && 
         store.userProfile && 
         store.currentArticle.author === store.userProfile.username;
});

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const goBackToList = () => {
  router.push({ name: 'ArticleView' });
};

const editArticle = () => {
  if (!isAuthor.value) {
    alert('수정 권한이 없습니다.');
    return;
  }
  router.push({ name: 'CreateView', query: { id: route.params.id } });
};

const deleteArticle = async () => {
  if (!isAuthor.value) {
    alert('삭제 권한이 없습니다.');
    return;
  }

  if (confirm('정말로 이 리뷰를 삭제하시겠습니까?')) {
    try {
      await store.deleteArticle(route.params.id);
      alert('리뷰가 삭제되었습니다.');
      goBackToList();
    } catch (error) {
      console.error('삭제 중 오류:', error);
    }
  }
};

const submitComment = async () => {
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력해주세요.');
    return;
  }

  try {
    await store.createComment({
      article_id: route.params.id,
      content: newComment.value
    });
    newComment.value = '';
    await fetchComments();
  } catch (error) {
    console.error('댓글 작성 실패:', error);
    alert('댓글 작성에 실패했습니다.');
  }
};

const deleteComment = async (commentId) => {
  if (!confirm('댓글을 삭제하시겠습니까?')) return;

  try {
    await store.deleteComment(commentId);
    await fetchComments();
  } catch (error) {
    console.error('댓글 삭제 실패:', error);
    alert('댓글 삭제에 실패했습니다.');
  }
};

const fetchComments = async () => {
  try {
    const response = await store.getComments(route.params.id);
    comments.value = response;
  } catch (error) {
    console.error('댓글 로드 실패:', error);
  }
};

const goToUserProfile = (username) => {
  router.push({ name: 'UserProfile', params: { username } });
};

onMounted(async () => {
  await store.getArticleById(route.params.id);
  console.log('현재 게시글 데이터:', store.currentArticle);
  if (!store.userProfile) {
    await store.getProfile();
  }
  await fetchComments();
});


// 포스터 URL 생성을 위한 computed 속성 추가
const posterUrl = computed(() => {
  if (store.currentArticle?.movie_id) {
    return `https://image.tmdb.org/t/p/w500${store.currentArticle.movie_poster_path}`;
  }
  return null;
});

// 이미지 로드 실패 시 처리
const handleImageError = (event) => {
  event.target.parentElement.innerHTML = '<div class="poster-placeholder">이미지 로드 실패</div>';
};


</script>

<style scoped>
.review-detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

/* .movie-info {
  background-color: #c2f8ce;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
} */

.movie-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.movie-content {
  display: flex;
  gap: 20px;
  width: 100%;
}

.review-main {
  flex: 1;
}

.movie-poster-container {
  flex: 0 0 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.rating-display {
  margin-top: 10px;
}

.stars {
  display: inline-flex;
  gap: 2px;
}

.star {
  font-size: 1.5rem;
  color: #ddd;
}

.star.filled {
  color: gold;
}

.rating-text {
  margin-left: 10px;
  font-weight: bold;
}

.review-main {
  background-color: rgb(255, 148, 148);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.review-text {
  line-height: 1.6;
  margin-bottom: 20px;
}

.author-link {
  color: #1da1f2;
  cursor: pointer;
}

.author-link:hover {
  text-decoration: underline;
}

.button-container {
  margin: 20px 0;
  display: flex;
  gap: 10px;
}

.back-button, .edit-button, .delete-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s;
}

.back-button {
  background-color: #4CAF50;
  color: white;
}

.edit-button {
  background-color: #2196F3;
  color: white;
}

.delete-button {
  background-color: #f44336;
  color: white;
}

.comments-section {
  margin-top: 30px;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.comment-submit-btn {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.comments-list .comment-item {
  padding: 15px;
  margin-bottom: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.9em;
  color: #666;
}

.comment-content {
  margin-bottom: 8px;
}

.comment-delete-btn {
  padding: 4px 8px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8em;
}

.movie-poster{
  width: 300px;
  
}
</style>