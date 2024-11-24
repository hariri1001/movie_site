<template>
    <section v-if="isLogin" class="container">
      <div class="article-section">
        <h2 class="latest-title">최신 게시글</h2>
        <div v-if="latestArticles.length > 0" class="grid-layout">
          <div 
            v-for="article in latestArticles" 
            :key="article.id" 
            class="article-item"
          >
            <h5>{{ article.title }}</h5>
            <p>{{ truncateContent(article.content) }}</p>
            <p><strong>작성자:</strong> {{ article.author }}</p>
            <p>
              <strong>평점:</strong>
              <span class="stars">
                <span
                  v-for="star in 5"
                  :key="star"
                  class="star"
                  :class="{ filled: star <= Math.floor(article.rating) }"
                >
                  ★
                </span>
              </span>
              ({{ article.rating || "N/A" }} / 5)
            </p>
            <p>
              <span
                class="like-button"
                :class="{ liked: article.isLiked }"
                @click="handleLike(article)"
              >
                👍
              </span>
              <strong>{{ article.likes_count || 0 }}</strong> Likes
            </p>
            <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }">
              자세히 보기
            </RouterLink>
          </div>
        </div>
      </div>
    </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const latestArticles = ref([])
const isLogin = computed(() => store.isLogin)

const fetchLatestArticles = async () => {
  try {
    console.log('게시글 가져오기 시작')
    await store.getArticles()
    console.log('store.articles:', store.articles)
    latestArticles.value = store.articles.slice(0, 3)
    console.log('최신 게시글:', latestArticles.value)
  } catch (error) {
    console.error('최신 게시글을 불러오는데 실패했습니다:', error)
  }
}

const handleLike = async (article) => {
  try {
    await store.toggleArticleLike(article.id)
  } catch (error) {
    console.error('좋아요 처리 실패:', error)
  }
}

const truncateContent = (content) => {
  return content?.length > 100 ? content.slice(0, 100) + '...' : content
}

onMounted(async () => {
  if (isLogin.value) {
    await fetchLatestArticles()
  }
})
</script>

<style scoped>
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 60px;
}

.article-section {
  position: relative;
  margin: 20px auto;
  max-width: 1400px;
  padding: 0 60px;
}

.latest-title {
  margin-bottom: 20px;
  font-size: 2rem;
  font-weight: bold;
}

.grid-layout {
  display: flex;
  gap: 0;
  padding: 20px 0;
  max-width: 1400px;
  margin: 0 auto;
}

.article-item {
  flex: 0 0 auto;
  width: calc(33.333% - 40px); /* 3개의 카드를 위한 너비 */
  margin-right: 40px; /* movie-card와 동일한 마진 */
  background: rgba(30, 30, 30, 0.95);
  padding: 15px;
  border-radius: 30px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.article-item h5 {
  font-size: 0.9rem; /* 제목 크기 더 축소 */
  font-weight: bold;
  margin-bottom: 2px;
}

.article-item p {
  font-size: 0.8rem; /* 본문 크기 더 축소 */
  margin: 1px 0; /* 마진 축소 */
  line-height: 1.2; /* 줄간격 축소 */
}

.stars {
  display: inline-flex;
  gap: 1px; /* 별 간격 축소 */
}

.star {
  font-size: 0.8rem; /* 별 크기 축소 */
  color: lightgray;
}

.star.filled {
  color: gold;
}

.like-button {
  font-size: 0.9rem; /* 좋아요 버튼 크기 축소 */
  cursor: pointer;
  color: lightgray;
}

a {
  font-size: 0.8rem; /* 링크 크기 축소 */
  color: #3182ce;
  text-decoration: none;
  margin-top: 2px;
}

/* 반응형 유지 */
@media (max-width: 1200px) {
  .container, .article-section {
    padding: 0 40px;
  }
}

@media (max-width: 768px) {
  .grid-layout {
    gap: 20px;
    flex-wrap: wrap;
  }
  
  .article-item {
    width: calc(50% - 10px);
  }
  
  .article-section {
    padding: 0 40px;
  }
}

@media (max-width: 576px) {
  .article-item {
    width: 100%;
  }
  
  .container, .article-section {
    padding: 0 20px;
  }
}
</style>