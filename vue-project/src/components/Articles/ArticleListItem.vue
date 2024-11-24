<template>
  <div class="article-item">
    <div class="article-content">
      <!-- 영화 포스터 추가 -->
      <div class="movie-poster-container">
        <img 
          v-if="posterUrl" 
          :src="posterUrl"
          :alt="article.movieTitle"
          class="movie-poster"
          @error="handleImageError"
        />
        <div v-else class="poster-placeholder">
          이미지 없음
        </div>
      </div>

      <div class="article-info">
        <h3 class="movie-title">{{ article.movie_title }}</h3>
        <p class="review-content">{{ article.content }}</p>
        <p><strong>작성자:</strong> {{ article.author }}</p>
        <div class="rating-display">
          <span class="stars">
            <span 
              v-for="star in 5" 
              :key="star"
              class="star"
              :class="{ filled: star <= Math.ceil(article.rating) }"
            >★</span>
          </span>
          <span class="rating-text">({{ article.rating }} / 5)</span>
        </div>
        <p>
          <span
            class="like-button"
            :class="{ liked: article.isLiked }"
            @click="$emit('toggle-like', article)"
          >
            👍 
          </span>
          <strong>{{ article.likes_count || 0 }}</strong> Likes
        </p>
        <RouterLink 
          :to="{ name: 'DetailView', params: { id: article.id } }"
          class="view-details"
        >
          리뷰 상세보기
        </RouterLink>
      </div>
    </div>
    <hr />
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
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: rgb(255, 124, 189);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.article-content {
  display: flex;
  gap: 20px;
}

.movie-poster-container {
  width: 150px;
  min-width: 150px;
  height: 225px;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f0f0f0;
}

.movie-poster {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.2s;
}

.movie-poster:hover {
  transform: scale(1.05);
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e0e0e0;
  color: #666;
}

.article-info {
  flex: 1;
}

.movie-title {
  margin: 0 0 10px 0;
  font-size: 1.4rem;
  color: #333;
}

.review-content {
  margin: 10px 0;
  line-height: 1.6;
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

.rating-display {
  margin: 10px 0;
}

.rating-text {
  margin-left: 8px;
  color: #666;
}

.like-button {
  font-size: 1.2rem;
  cursor: pointer;
  transition: transform 0.2s;
  margin-right: 5px;
}

.like-button:hover {
  transform: scale(1.1);
}

.like-button.liked {
  color: #ff4b4b;
}

.view-details {
  display: inline-block;
  margin-top: 10px;
  padding: 8px 15px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.view-details:hover {
  background-color: #45a049;
}
</style>