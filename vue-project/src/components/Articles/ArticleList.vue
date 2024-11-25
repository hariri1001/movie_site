
 <template>
  <div class="review-list-container">
    <div class="review-header">
      <h2>지금 뜨는 코멘트</h2>
      <div class="controls-container">
        <RouterLink :to="{ name: 'CreateView' }" class="create-link">
          <h6>코멘트 작성</h6>
        </RouterLink>
        <div class="sort-controls">
          <select v-model="sortBy" @change="sortReviews" class="sort-select">
            <option value="latest">최신순</option>
            <option value="rating">평점순</option>
            <option value="likes">좋아요순</option>
          </select>
        </div>

      </div>
      
    </div>

    <div class="reviews-grid">
      <ArticleListItem v-for="article in sortedArticles" :key="article.id" :article="article" @toggle-like="handleToggleLike"/>
    </div>

    <div v-if="store.articles.length === 0" class="no-reviews">
      아직 작성된 리뷰가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import ArticleListItem from "./ArticleListItem.vue";

const store = useCounterStore();
const sortBy = ref('latest');

const sortedArticles = computed(() => {
  const articles = [...store.articles];
  
  switch (sortBy.value) {
    case 'rating':
      return articles.sort((a, b) => b.rating - a.rating);
    case 'likes':
      return articles.sort((a, b) => (b.likes_count || 0) - (a.likes_count || 0));
    case 'latest':
    default:
      return articles.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  }
});

const handleToggleLike = async (article) => {
  try {
    const { liked, likes_count } = await store.toggleArticleLike(article.id);
    const targetArticle = store.articles.find((a) => a.id === article.id);
    if (targetArticle) {
      targetArticle.isLiked = liked;
      targetArticle.likes_count = likes_count;
    }
  } catch (error) {
    console.error("좋아요 상태 업데이트 실패:", error);
  }
};

const sortReviews = () => {
  // 정렬 방식이 변경될 때 필요한 추가 로직이 있다면 여기에 구현
  console.log('Sort changed to:', sortBy.value);
};

onMounted(async () => {
  await store.getArticles();
});
</script>

<style scoped>
.review-list-container {
  max-width: 740px;
  margin: 0 auto;
  padding: 20px;
}

.review-header {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

/* 버튼과 정렬 컨트롤을 위한 새로운 컨테이너 */
.controls-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sort-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.sort-select {
  padding: 8px;
  border: 1px solid #00ba19;;
  border-radius: 4px;
  background-color: #1a1a1a;
}

.reviews-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
}

.no-reviews {
  text-align: center;
  padding: 40px;
  background-color: #fcffbd;
  border-radius: 8px;
  color: #999898;
}


.create-link {
  display: inline-block;
  padding: 5px 16px;
  background-color: #00ba19;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.create-link:hover {
  background-color: #029916;;
}

</style>