<template>
  <div>
    
    <ArticleList />
  </div>
</template>

<script setup>
import ArticleList from '@/components/Articles/ArticleList.vue';
import { onMounted } from 'vue';
import { useArticleStore } from '@/stores/article';

const articleStore = useArticleStore();


// 컴포넌트 마운트 시, 라우트 변경 시 게시글 로드
onMounted (() => {
  articleStore.getArticles();
});
</script>