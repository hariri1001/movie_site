<template>
  <div class="article-item">
    <div class="article-content">

      <div class="article-header">
        <div class="author"><strong>작성자:</strong> {{ article.author }}</div>
        <div class="rating-display">
          <span class="stars">
            <span v-for="star in 5" :key="star" class="star" :class="{ filled: star <= Math.ceil(article.rating) }">★</span>
          </span>
          <span class="rating-text">({{ article.rating }} / 5)</span>
        </div>
      </div>

      <!-- 영화 포스터 -->
      <div class="article-main">
        <div class="movie-poster-container">
          <img v-if="posterUrl" :src="posterUrl" :alt="article.movieTitle" class="movie-poster" @error="handleImageError"/>
          <div v-else class="poster-placeholder">
            이미지 없음
          </div>
        </div>
        
        <div class="content-container">
          <h3 class="movie-title">{{ article.movie_title }}</h3>
          <p class="review-content">{{ article.content }}</p>
        </div>
      </div>
      
      
      <div class="article-footer">
        <p>
          <span class="like-button" :class="{ liked: article.isLiked }" @click="$emit('toggle-like', article)">
            👍 
          </span>
          <strong>{{ article.likes_count || 0 }}</strong> Likes
        </p>
        <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }" class="view-details">
          리뷰 상세보기
        </RouterLink>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { RouterLink } from "vue-router";

const props = defineProps({
  article: Object,
});

const posterUrl = computed(() => {
  if (props.article?.movie_poster_path) {
    
    return `https://image.tmdb.org/t/p/w500${props.article.movie_poster_path}`;
    
  }
  return null;
});

const handleImageError = (event) => {
  event.target.parentElement.innerHTML = '<div class="poster-placeholder">이미지 로드 실패</div>';
};
</script>

<style scoped>
.article-item {
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 8px;
  background-color: #272727;
  width: 700px;
  height: 300px;
  box-sizing: border-box; /* 패딩을 높이/너비에 포함 */
  color: #F8F9FA;
  border: 1px solid #00ba19;;
}

/* 메인 콘텐츠 영역 */
.article-content {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* 헤더 영역 스타일링 */
.article-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 10px 10px 10px; /* 상우하좌 패딩 */
  /* border-bottom: 1px solid #00ba19; */
  height: 24px; /* 헤더 높이 축소 */
  font-size: 0.9rem; /* 전체 폰트 크기 축소 */
}


.article-header p {
  margin: 0;
  font-size: 0.9rem;
}

.author{
  font-size: 1rem;
}


/* 별점 표시 스타일링 */
.rating-display {
  display: flex;
  align-items: center;
  gap: 4px;
}

.stars {
  margin: 0 1px;
}

.star.filled {
  color: gold;
}

/* 메인 콘텐츠 영역 스타일링 */
.article-main {
  display: flex;
  gap: 20px;
  flex: 1;
  padding: 25px 0;
  min-height: 0; /* 컨텐츠 영역이 넘치지 않도록 설정 */
}

.movie-poster-container {
  width: 100px; /* 포스터 너비 조정 */
  min-height: 150px; /* 포스터 높이 조정 */
  max-height: 150px; /* 포스터 최대 높이 제한 */
  flex-shrink: 0; /* 포스터 크기 고정 */
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: contain; /* 이미지가 잘리지 않고 온전히 표시되도록 */
  border-radius: 8px;
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.content-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
  overflow-y: auto;
}


.movie-title {
  font-size: 1.2rem;
  margin: 0;
  line-height: 1.2;
}

.review-content {
  margin: 0;
  line-height: 1.4;
  flex: 1;
  overflow-y: auto;
}

/* 푸터 영역 스타일링 */
.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid #00ba19;;
  height: 30px; /* 푸터 높이 고정 */
  font-size: 0.9rem; /* 전체 폰트 크기 축소 */
}


.article-footer p {
  display: flex;
  align-items: center;
  gap: 4px;
  margin: 0;
  font-size: 0.9rem;
}

/* 좋아요 버튼 스타일링 */
.like-button {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: transform 0.2s;
  font-size: 0.9rem;
  background-color: transparent;
}

.like-button + strong {
  margin-right: 2px;
  font-size: 0.9rem;
}

.like-button:hover {
  
  background-color: transparent; /* 호버 시에도 배경색 투명 유지 */
}

.like-button.liked {
  color: #ff4444;
}

/* 좋아요 수 스타일링 */
.like-button + strong {
  margin-right: 4px;
}

/* 상세보기 링크 스타일링 */
/* 상세보기 링크 스타일링 */
.view-details {
  text-decoration: none;
  color: #F8F9FA;
  padding: 4px 12px;
  border: 1px solid #00ba19;;
  border-radius: 8px;
  transition: all 0.2s;
  font-size: 0.85rem;
}

.view-details:hover {
  background-color: #1a1a1a;
  color: rgb(182, 182, 182);
}

/* 구분선 스타일링 */
hr {
  border: none;
  border-top: 1px solid #eee;
  margin: 20px 0;
}

.like-button:hover,
.like-button:active,
.like-button:focus {
  transform: scale(1.1);
  background-color: transparent !important;
  outline: none;
}

.like-button.liked {
  color: #ff4444;
  background-color: transparent !important;
}
</style>