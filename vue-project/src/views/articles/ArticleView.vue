<template>
  <div>
    <h1>Articles</h1>
    <RouterLink :to="{ name: 'CreateView' }">Create New Article</RouterLink>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/Articles/ArticleList.vue';
import { onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();

// 컴포넌트 마운트 시 게시글 로드
onMounted(() => {
  store.getArticles();
});
</script>