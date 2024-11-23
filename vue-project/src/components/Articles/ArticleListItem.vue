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
        @click="$emit('toggle-like', article)"
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
