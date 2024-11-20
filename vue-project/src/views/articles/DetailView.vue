<!-- 뒤로가기 -->
<!-- <template>
  <div>
    <h1>Article Details</h1>
    <div v-if="store.currentArticle">
      <h3>{{ store.currentArticle.title }}</h3>
      <p>{{ store.currentArticle.content }}</p>
    </div>
    
    <button @click="goBackToList" class="back-button">목록으로 돌아가기</button>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRoute, useRouter } from 'vue-router';

const store = useCounterStore();
const route = useRoute();
const router = useRouter(); -->

<!-- 게시글 목록으로 돌아가기 -->
<!-- const goBackToList = () => {
  router.push({ name: 'ArticleView' });
};

onMounted(() => {
  store.getArticleById(route.params.id);
});
</script>

<style scoped>
.back-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.back-button:hover {
  background-color: #45a049;
}
</style> -->
<template>
  <div>
    <h1>Article Details</h1>
    <div v-if="store.currentArticle">
      <h3>{{ store.currentArticle.title }}</h3>
      <p>{{ store.currentArticle.content }}</p>
      <p><strong>작성자:</strong> {{ store.currentArticle.author }}</p> <!-- 작성자 표시 -->
    </div>
    <div class="button-container">
      <button @click="goBackToList" class="back-button">목록으로 돌아가기</button>
      <button @click="editArticle" class="edit-button">수정</button>
      <button @click="deleteArticle" class="delete-button">삭제</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRoute, useRouter } from 'vue-router';

const store = useCounterStore();
const route = useRoute();
const router = useRouter();

const goBackToList = () => {
  router.push({ name: 'ArticleView' });
};

const editArticle = () => {
  router.push({ name: 'CreateView', query: { id: route.params.id } });
};

const deleteArticle = async () => {
  if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    try {
      await store.deleteArticle(route.params.id); // Pinia 스토어에서 삭제 호출
      alert('게시글이 삭제되었습니다.');
      goBackToList(); // 삭제 후 리스트 페이지로 이동
    } catch (error) {
      console.error('삭제 중 오류:', error);
    }
  }
};


onMounted(() => {
  store.getArticleById(route.params.id);
});
</script>

<style scoped>
.button-container {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

/* 기존 버튼 스타일 유지 */
.back-button, .edit-button, .delete-button {
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  color: white;
}

.back-button {
  background-color: #4CAF50;
}

.back-button:hover {
  background-color: #45a049;
}

.edit-button {
  background-color: #2196F3;
}

.edit-button:hover {
  background-color: #0b7dda;
}

.delete-button {
  background-color: #f44336;
}

.delete-button:hover {
  background-color: #da190b;
}
</style>
