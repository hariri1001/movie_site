<!-- <template>
  <div class="article-item">
    <h5>{{ article.id }}. {{ article.title }}</h5>
    <p>{{ article.content }}</p>
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
        @click="toggleLike(article)"
      >
        ❤️
      </span>
      <strong>{{ article.likes_count || 0 }}</strong> Likes
    </p>
    <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }">
      View Details
    </RouterLink>
    <hr />
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";

// Props로 article 데이터를 명시적으로 선언
defineProps({
  article: Object, // 게시글 데이터
});

const store = useCounterStore();

// 좋아요 토글 함수
const toggleLike = async (article) => {
  try {
    const { liked, likesCount } = await store.toggleArticleLike(article.id);
    article.isLiked = liked; // 서버에서 반환된 좋아요 상태
    article.likes_count = likesCount; // 서버에서 반환된 좋아요 수
  } catch (error) {
    console.error("좋아요 상태 업데이트 실패:", error);
  }
};
</script>

<style scoped>
.article-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.stars {
  display: inline-flex;
  gap: 2px;
}

.star {
  font-size: 1.2rem;
  color: lightgray;
}

.star.filled {
  color: gold;
}

.like-button {
  font-size: 1.5rem;
  cursor: pointer;
  color: lightgray;
  transition: color 0.3s ease;
}

.like-button.liked {
  color: red;
}

.like-button:hover {
  color: darkred;
}
</style> -->
<template>
  <div class="article-item">
    <h5>{{ article.title }}</h5>
    <p>{{ article.content }}</p>
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
        @click="toggleLike(article)"
      >
        ❤️
      </span>
      <strong>{{ article.likes_count || 0 }}</strong> Likes
    </p>
    <RouterLink :to="{ name: 'DetailView', params: { id: article.id } }">
      View Details
    </RouterLink>
    <hr />
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { useCounterStore } from "@/stores/counter";

defineProps({
  article: Object,
});

const store = useCounterStore();

const toggleLike = async (article) => {
  try {
    const { liked, likes_count } = await store.toggleArticleLike(article.id);
    article.isLiked = liked;
    article.likes_count = likes_count;
  } catch (error) {
    console.error("좋아요 상태 업데이트 실패:", error);
  }
};
</script>

<style scoped>
.article-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.stars {
  display: inline-flex;
  gap: 2px;
}

.star {
  font-size: 1.2rem;
  color: lightgray;
}

.star.filled {
  color: gold;
}

.like-button {
  font-size: 1.5rem;
  cursor: pointer;
  color: lightgray;
  transition: color 0.3s ease;
}

.like-button.liked {
  color: red;
}

.like-button:hover {
  color: darkred;
}
</style>
