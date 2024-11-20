<template>
  <div>
    <h1>Article Details</h1>
    <div v-if="store.currentArticle">
      <h3>{{ store.currentArticle.title }}</h3>
      <p>{{ store.currentArticle.content }}</p>
      <p><strong>Published:</strong> {{ store.currentArticle.created_at }}</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRoute } from 'vue-router';

const store = useCounterStore();
const route = useRoute();

onMounted(() => {
  store.getArticleById(route.params.id);
});
</script>
