
<template>
  <div class="review-detail-container">
    <!-- <h1>영화 코멘트</h1> -->
    <br>
    <div class="back-button-container">
      <button @click="goBackToList" class="back-button">목록</button>
    </div>
    <div v-if="articleStore.currentArticle" class="review-content">
      <div class="movie-info">
        <div class="movie-content">
          <!-- 포스터 이미지 추가 -->
          <div class="movie-poster-container">
            <img 
              v-if="posterUrl" 
              :src="posterUrl"
              :alt="articleStore.currentArticle.movieTitle"
              class="movie-poster"
              @error="handleImageError"
            />
            <div v-else class="poster-placeholder">
              이미지 없음
            </div>

            <p>{{ articleStore.currentArticle.movie_title }}</p>
          </div>

          <div class="review-main">
            <div class="review-header">
              <div class="review-author">
                <p><strong>작성자 : </strong>
                <span 
                  @click="goToUserProfile(articleStore.currentArticle.author)" 
                  class="author-link"
                >
                  {{ articleStore.currentArticle.author }}
                </span></p>
              </div>

              <div class="rating-display">
                <div class="stars">
                  <span 
                    v-for="star in 5" 
                    :key="star"
                    class="star"
                    :class="{ filled: star <= Math.ceil(articleStore.currentArticle.rating) }"
                  >★</span>
                </div>
                <span class="rating-text">{{ articleStore.currentArticle.rating }} / 5</span>
              </div>
            </div>

            <p class="review-text">{{ articleStore.currentArticle.content }}</p>
            
          </div>
        </div>
      </div>

      

      <div class="button-container">
        
        <template v-if="isAuthor">
          <button @click="editArticle" class="edit-button">repost-it</button>
          <button @click="deleteArticle" class="delete-button">삭제</button>
        </template>
      </div>

      <div class="comments-section">
        <h3>댓글</h3>
        
        <div class="comment-form">
          <textarea 
            v-model="newComment" 
            placeholder="이 코멘트에 대한 의견을 남겨주세요"
            class="comment-input"
          ></textarea>
          <div class="button-wrapper">
            <button @click="submitComment" class="comment-submit-btn">댓글 작성</button>
          </div>
          
        </div>

        <div class="comments-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <span class="comment-author">{{ comment.author }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <div>
              <p class="comment-content">{{ comment.content }}</p>
            </div>
            
            <button 
              v-if="comment.author === profileStore.userProfile?.username" 
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
import { useArticleStore } from '@/stores/article';
import { useProfileStore } from '@/stores/profile';
import { useCommentStore } from '@/stores/comments';
import { useRoute, useRouter } from 'vue-router';

const articleStore = useArticleStore();
const profileStore = useProfileStore();
const commentStore = useCommentStore();

const route = useRoute();
const router = useRouter();

const comments = ref([]);
const newComment = ref('');

const isAuthor = computed(() => {
  return articleStore.currentArticle && 
         profileStore.userProfile && 
         articleStore.currentArticle.author  === profileStore.userProfile.username ;
});

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
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

  if (confirm('정말로 이 코멘트 삭제하시겠습니까?')) {
    try {
      await articleStore.deleteArticle(route.params.id);
      alert('커멘트가 삭제되었습니다.');
      goBackToList();
    } catch (error) {
      console.error('삭제 중 오류:', error);
    }
  }
};
///////
const goToUserProfile = (username) => {
  router.push({ name: 'UserProfile', params: { username } });
};


const submitComment = async () => {
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력해주세요.');
    return;
  }

  try {
    await commentStore.createComment({
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
    await commentStore.deleteComment(commentId);
    await fetchComments();
  } catch (error) {
    console.error('댓글 삭제 실패:', error);
    alert('댓글 삭제에 실패했습니다.');
  }
};

const fetchComments = async () => {
  try {
    const response = await commentStore.getComments(route.params.id);
    comments.value = response;
  } catch (error) {
    console.error('댓글 로드 실패:', error);
  }
};


onMounted(async () => {
  await articleStore.getArticleById(route.params.id);
  console.log('현재 게시글 데이터:', articleStore.currentArticle);
  if (!profileStore.userProfile) {
    await profileStore.getProfile();
  }
  await fetchComments();
});


// 포스터 URL 생성을 위한 computed 속성 추가
const posterUrl = computed(() => {
  if (articleStore.currentArticle?.movie_id) {
    return `https://image.tmdb.org/t/p/w500${articleStore.currentArticle.movie_poster_path}`;
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
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
}


.movie-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #272727;
  /* border: 2px solid #00ba19; */
}

.movie-content {
  display: flex;
  gap: 10px;
  width: 100%;
}


.review-main {
  background-color: #1a1a1a;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  color: #F8F9FA;
  width: 100%;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  /* border-bottom: 1px solid #00ba19; */
}

.review-author {
  display: flex;
  align-items: center;
}


.movie-poster-container {
  position: relative;
  flex: 0 0 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #F8F9FA;
  font-size: 1.5rem;
}

.movie-poster {
  width: 170px;
  height: 250px; /* 영화 포스터 표준 비율(2:3) */
  object-fit: cover;
  border-radius: 8px;
  margin: 0 !important; /* 기존 마진 제거 */
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}


.movie-poster-container p {
  margin-top: 15px; /* 원하는 간격만큼 조정 가능 */
  margin-bottom: 0px;
  font-size: 1.2rem;
}

.rating-display {
  margin-top: 0px;
}

.stars {
  display: inline-flex;
  gap: 2px;
}

.star {
  font-size: 1.2rem;
  color: #ddd;
}

.star.filled {
  color: gold;
}



.review-main {
  background-color: #1a1a1a;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  color: #F8F9FA;
}

.rating-text {
  margin-left: 10px;
  
}

.review-text {
  line-height: 1.6;
  margin-top: 20px;
  font-size: 1rem;
}

.review-author p {
  margin: 0;
}

.author-link {
  color: #1da1f2;
  cursor: pointer;
}

.rating-display {
  display: flex;
  align-items: center;
  gap: 10px;
}
.author-link:hover {
  text-decoration: underline;
}

.button-container {
  display: flex;
  justify-content: flex-end; /* 오른쪽 정렬 */
  gap: 8px; /* 버튼 사이 간격 */
  margin: 10px 0;
}

/* 공통 버튼 스타일 */
.button {
 border: 1px solid #ead200;
 background: none;
 border-radius: 8px;
 cursor: pointer;
 font-size: 0.85rem;
 color: #ffffff;
 display: flex;
 align-items: center;
 justify-content: center;
 transition: all 0.2s;
}

.button:hover {
 background-color: #ead200;
 color: rgb(3, 3, 3);
}

.back-button-container {
 display: flex;
 margin: 0px 0px 20px 0;
 justify-content: flex-end;
}

.back-button {
 background: none;
 border: 1px solid #ead200;
 color: #ffffff;
 width: 80px;
 height: 40px;
 border-radius: 8px;
 cursor: pointer;
}

.back-button:hover {
 background-color: #ead200;
 color: rgb(3, 3, 3);
}

.edit-button {
 background: none;
 border: 1px solid #ead200;
 color: #ffffff;
 width: 95px;
 height: 40px;
 border-radius: 8px;
}

.edit-button:hover {
 background-color: #ead200;
 color: rgb(3, 3, 3);
}

.delete-button {
 background: none;
 border: 1px solid #ead200;
 color: #ffffff;
 width: 80px;
 height: 40px;
 border-radius: 8px;
}

.delete-button:hover {
 background-color: #ead200;
 color: rgb(3, 3, 3);
}

.comments-section {
  margin-top: 30px;
}

.comment-form {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  
}

.comment-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  /* border: 2px solid #00ba19; */
  border-radius: 8px;
  resize: vertical;
  background-color: #272727;
  color: #F8F9FA;
}

.button-wrapper {
  display: flex;
  justify-content: flex-end;
}

.comment-submit-btn {
 background: none;
 border: 1px solid #ead200;
 color: #ffffff;
 padding: 4px 12px;
 border-radius: 8px;
 cursor: pointer;
 font-size: 0.85rem;
 width: 120px;
 height: 40px;
 display: flex;
 justify-content: center;
 align-items: center;
}


.comment-submit-btn:hover {
 background-color: #ead200;
 color: rgb(3, 3, 3);
}

.comments-list .comment-item {
  padding: 15px;
  margin-bottom: 10px;
  background-color: #272727;;
  border-radius: 8px;
  /* border: 2px solid #00ba19; */
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
 background: none;
 border: 1px solid #ead200;
 color: #ffffff;
 padding: 4px 12px;
 border-radius: 8px;
 cursor: pointer;
 font-size: 0.85rem;
}

.comment-delete-btn:hover {
 background-color: #ead200;
 color: rgb(3, 3, 3);
}


</style>