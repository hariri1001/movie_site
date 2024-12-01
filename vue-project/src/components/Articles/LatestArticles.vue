<template>
    <section v-if="isLogin" class="container">
      <div class="article-section">
        <h2 class="latest-title">최신 게시글</h2>

        <div v-if="latestArticles.length > 0" class="grid-layout">
          <div v-for="article in latestArticles" :key="article.id" class="article-item">
            <div class="article-header">
              <p><strong>작성자:</strong> {{ article.author }}</p>
              <p>
                <span class="stars">
                  <span v-for="star in 5" :key="star" class="star" :class="{ filled: star <= Math.floor(article.rating) }">
                    ★
                  </span>
                </span>
                <!-- ({{ article.rating || "N/A" }} / 5) -->
              </p>
            </div>
            
            <div class="article-content">
              <h5>{{ article.title }}</h5>
              <p>{{ truncateContent(article.content) }}</p>
            </div>
            
            <div class="article-footer">
              <p>
                <span class="like-button" :class="{ liked: article.isLiked }" @click="handleLike(article)">
                  👍
                </span>
                <strong>{{ article.likes_count || 0 }}</strong> 
              </p>
              
              <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }" class="view-details">
                자세히 보기
              </RouterLink>
            </div>
            
          </div>
        </div>
      </div>
    </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import { useAuthStore } from '@/stores/auth'

const articleStore = useArticleStore();
const authStore = useAuthStore();
const latestArticles = ref([])
const isLogin = computed(() => authStore.isLogin)

const fetchLatestArticles = async () => {
  try {
    console.log('게시글 가져오기 시작')
    await articleStore.getArticles()
    console.log('articleStore.articles:', articleStore.articles)
    latestArticles.value = articleStore.articles.slice(0, 3)
    console.log('최신 게시글:', latestArticles.value)
  } catch (error) {
    console.error('최신 게시글을 불러오는데 실패했습니다:', error)
  }
}

const handleLike = async (article) => {
  try {
    await articleStore.toggleArticleLike(article.id)
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

hr {
  border: 1px solid #cccccc;;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  /* padding: 0 60px; */
  
}

.article-section {
  position: relative;
  margin: 20px auto;
  max-width: 1400px;
  padding: 0 20px;
  
}

.latest-title {
  margin-bottom: 20px;
  font-size: 2rem;
  /* font-weight: bold; */
}

.grid-layout {
  display: flex;
  gap: 20px;
  padding: 20px 0;
  max-width: 1400px;
  margin: 0 auto;
}

.article-item {
  flex: 0 0 auto;
  width: calc(33.333% - 14.3px);
  background: rgba(41, 41, 41, 0.95);
  height: 200px;
  padding: 15px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  /* border: 1px solid #00ba19;; */

}


.article-item h5 {
  font-size: 0.9rem;
  font-weight: bold;
  margin-bottom: 0px;
}

.article-item p {
  font-size: 0.8rem;
  margin: 2px 0;
  line-height: 1.2;
}

.article-item .article-content h5 {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #aaaaaa;
  font-size: 0.9rem;
  font-weight: bold;
}

.article-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: auto;
}

.stars {
  display: inline-flex;
  gap: 1px;
}

.star {
  font-size: 0.8rem;
  color: lightgray;
}

.star.filled {
  color: gold;
}



/* 좋아요 버튼 스타일링 */
.like-button {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  border-radius: 4px;
  transition: transform 0.1s;
  font-size: 1.4rem;
  background-color: transparent;
  width: 50px;
  margin: 0;
  padding: 0;
  gap: 2px; /* 아이콘과 텍스트 사이 간격 조절 */
  border: none; /* 테두리 제거 */
}

.like-button + strong {
  margin-left: -20px; /* 음수 마진으로 간격 줄이기 */
  font-size: 1.1rem;
}

.like-button:hover {
  
  background-color: transparent; /* 호버 시에도 배경색 투명 유지 */
}


.read-more {
  font-size: 0.8rem;
  color: #3182ce;
  text-decoration: none;
  margin-top: 4px;
}

.article-header {
  display: flex;
  justify-content: space-between; /* 작성자와 별점 사이에 공간을 배치 */
  align-items: center; /* 수직 중앙 정렬 */
  border-bottom: 1px solid #aaaaaa;
  padding-bottom: 10px;
  
}

.article-header p {
  margin: 0; /* p 태그의 기본 margin 제거 */
  display: flex; /* p 내부의 요소들을 수평 정렬 */
  align-items: center; /* 아이템들을 수직 중앙 정렬 */
  font-size: 13px;
}

.stars {
  display: flex; /* 별점들을 수평으로 정렬 */
  margin-right: 8px; /* 별점과 숫자 사이에 간격 추가 */
}

.star {
  font-size: 1.2rem; /* 별 크기 설정 */
  color: #ccc; /* 기본 별 색 */
}

.star.filled {
  color: gold; /* 채워진 별의 색상 */
}

strong {
  margin-right: 4px; /* 작성자 앞에 약간의 간격 추가 */
}



.article-footer {
  display: flex;
  align-items: center; /* 요소들이 수직으로 중앙에 배치되도록 */
  justify-content: space-between; /* 요소들 사이에 공간을 배치하고 양쪽 끝에 배치 */
}

.article-footer p {
  margin: 0; /* p 태그의 기본 margin 제거 */
  display: flex; /* p 내부의 요소들을 수평 정렬 */
  align-items: center; /* 아이템들 수직 중앙 정렬 */
}

.like-button {
  cursor: pointer;
  margin-right: 8px; /* 좋아요 버튼과 숫자 사이에 간격 추가 */
}

strong {
  margin-right: 8px; /* 좋아요 숫자와 "자세히 보기" 사이에 간격 추가 */
}

RouterLink {
  text-decoration: none; /* 기본 링크 스타일 제거 */
  color: #007bff; /* 링크 색상 설정 */
}


.view-details {
  text-decoration: none;
  color: #F8F9FA;
  padding: 4px 12px;
  /* border: 1px solid #00ba19; */
  border-radius: 8px;
  transition: all 0.2s;
  font-size: 0.85rem;
}

.view-details:hover {
  background-color: #1a1a1a;
  color: rgb(182, 182, 182);
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
    width: calc(50% - 20px);
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