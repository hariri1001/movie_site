<template>
  <div>
    <h1>Article Details</h1>
    <div v-if="store.currentArticle">
      <h3>{{ store.currentArticle.title }}</h3>
      <p>{{ store.currentArticle.content }}</p>
      <p>
        <strong>작성자:</strong>
        <span @click="goToUserProfile(store.currentArticle.author)" class="author-link">
          {{ store.currentArticle.author }}
        </span>
      </p>
    </div>

    <div class="button-container">
      <button @click="goBackToList" class="back-button">목록으로 돌아가기</button>
      <!-- 작성자와 현재 사용자가 같을 때만 수정/삭제 버튼 표시 -->
      <template v-if="isAuthor">
        <button @click="editArticle" class="edit-button">수정</button>
        <button @click="deleteArticle" class="delete-button">삭제</button>
      </template>
    </div>


  </div>
</template>

<script setup>
import { onMounted, computed  } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRoute, useRouter } from 'vue-router';

const store = useCounterStore();
const route = useRoute();
const router = useRouter();


// 현재 사용자가 글 작성자인지 확인하는 computed 속성
const isAuthor = computed(() => {
  return store.currentArticle && 
         store.userProfile && 
         store.currentArticle.author === store.userProfile.username;
});




const goBackToList = () => {
  router.push({ name: 'ArticleView' });
};




const editArticle = () => {
  if (!isAuthor.value) {
    alert('수정 권한이 없습니다.');
    return;
  }
  router.push({ name: 'CreateView', query: { id: route.params.id } });
};

const deleteArticle = async () => {
  if (!isAuthor.value) {
    alert('삭제 권한이 없습니다.');
    return;
  }

  if (confirm('정말로 이 게시글을 삭제하시겠습니까?')) {
    try {
      await store.deleteArticle(route.params.id);
      alert('게시글이 삭제되었습니다.');
      goBackToList();
    } catch (error) {
      console.error('삭제 중 오류:', error);
    }
  }
};

onMounted(async () => {
  // 게시글 정보와 함께 사용자 프로필 정보도 확인
  await store.getArticleById(route.params.id);
  if (!store.userProfile) {
    await store.getProfile();
  }
});

// 다른 사용자의 프로필로 이동
const goToUserProfile = (username) => {
  router.push({ name: 'UserProfile', params: { username } });
};





</script>

<style scoped>
.author-link {
  color: #1da1f2;
  cursor: pointer;
}

.author-link:hover {
  text-decoration: underline;
}


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
