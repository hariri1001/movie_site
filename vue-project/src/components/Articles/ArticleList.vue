<!-- <template>
  <div>
    <h3>Article List</h3>
    <ArticleListItem 
      v-for="article in store.articles"
      :key="article.id"
      :article="article"
    />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import ArticleListItem from '@/components/Articles/ArticleListItem.vue';

const store = useCounterStore();
</script> -->

<!-- <template>
  <div>
    <h3>Article List</h3>
    <ArticleListItem
      v-for="article in store.articles"
      :key="article.id"
      :article="article"
    />
  </div>
</template>

<script setup>
import ArticleListItem from '@/components/Articles/ArticleListItem.vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
</script> -->
<template>
  <div>
    <h3>Article List</h3>
    <ArticleListItem 
      v-for="article in store.articles"
      :key="article.id"
      :article="article"
    />
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useCounterStore } from "@/stores/counter";
import ArticleListItem from "./ArticleListItem.vue";

const store = useCounterStore();

onMounted(() => {
  store.getArticles();
});
</script>
