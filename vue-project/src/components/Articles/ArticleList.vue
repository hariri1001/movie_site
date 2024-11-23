<template>
  <div>
    <h3>Article List</h3>
    <ArticleListItem v-for="article in store.articles" :key="article.id" :article="article" @toggle-like="handleToggleLike"
    />
  </div>
</template>

<script setup>

import { onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import ArticleListItem from "./ArticleListItem.vue";

const store = useCounterStore();

// 컴포넌트 마운트 시 게시글 로드
onMounted(async () => {
  await store.getArticles();
  console.log('현재 게시글 목록:', store.articles); // 디버깅용
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
</script>

