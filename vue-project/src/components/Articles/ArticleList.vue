<!-- <template>
  <div>
    <h3>Article List</h3>
    <ArticleListItem 
      v-for="article in store.articles"
      :key="article.id"
      :article="article"
      @toggle-like="handleToggleLike"
    />
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import ArticleListItem from "./ArticleListItem.vue";

const store = useCounterStore();

// 좋아요 상태 변경 핸들러
const handleToggleLike = async (article) => {
  try {
    const { liked, likes_count } = await store.toggleArticleLike(article.id);

    // 상태를 부모에서 직접 업데이트
    const targetArticle = store.articles.find((a) => a.id === article.id);
    if (targetArticle) {
      targetArticle.isLiked = liked;
      targetArticle.likes_count = likes_count;
    }
  } catch (error) {
    console.error("좋아요 상태 업데이트 실패:", error);
  }
};

onMounted(() => {
  store.getArticles();
});
</script> -->

<template>
  <div>
    <h3>Article List</h3>
    <ArticleListItem
      v-for="article in articles"
      :key="article.id"
      :article="article"
      @toggle-like="handleToggleLike"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import ArticleListItem from "./ArticleListItem.vue";

const store = useCounterStore();
const articles = ref([]);

onMounted(async () => {
  await store.getArticles();
  articles.value = store.articles; // Pinia 스토어에서 상태 가져오기
});

const handleToggleLike = async (article) => {
  try {
    const { liked, likes_count } = await store.toggleArticleLike(article.id);

    // articles 배열에서 해당 게시글 상태 업데이트
    const targetArticle = articles.value.find((a) => a.id === article.id);
    if (targetArticle) {
      targetArticle.isLiked = liked;
      targetArticle.likes_count = likes_count;
    }
  } catch (error) {
    console.error("좋아요 상태 업데이트 실패:", error);
  }
};
</script>

