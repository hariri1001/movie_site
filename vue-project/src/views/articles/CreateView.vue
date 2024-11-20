<template>
  <div>
    <h1>Create New Article</h1>
    <form @submit.prevent="submitArticle">
      <label>
        Title:
        <input type="text" v-model="title" />
      </label>
      <label>
        Content:
        <textarea v-model="content"></textarea>
      </label>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const title = ref('');
const content = ref('');

const submitArticle = () => {
  store.createArticle({ title: title.value, content: content.value });
};
</script>
