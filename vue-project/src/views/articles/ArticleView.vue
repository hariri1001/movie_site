<template>
  <div>
    <h1>코멘트 게시판</h1>
    <RouterLink :to="{ name: 'CreateView' }">
      <h2>게시글 생성</h2>
    </RouterLink>
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/Articles/ArticleList.vue';
import { onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();


// 컴포넌트 마운트 시, 라우트 변경 시 게시글 로드
onMounted (() => {
  store.getArticles();
});
</script>