<!-- <template>
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
</script> -->

<!-- 평점 작성 -->
<template>
  <div>
    <h1>{{ isEditing ? "Edit Article" : "Create New Article" }}</h1>
    <form @submit.prevent="submitArticle">
      <!-- 제목 입력 -->
      <label>
        Title:
        <input type="text" v-model="title" />
      </label>
      <!-- 내용 입력 -->
      <label>
        Content:
        <textarea v-model="content"></textarea>
      </label>
      <!-- 별점 추가 -->
      <div class="rating-container">
        <h3>Rate this article:</h3>
        <div class="stars" @mouseleave="resetHover">
          <span
            v-for="star in 5"
            :key="star"
            class="star"
            @mousemove="updateHover($event, star)"
            @click="setRating()"
            :style="{
              background: `linear-gradient(to right, gold ${getFillPercentage(star)}%, lightgray ${getFillPercentage(star)}%)`,
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }"
          >
            ★
          </span>
        </div>
        <p class="rating-text">Selected Rating: {{ rating.toFixed(1) }} / 5</p>
      </div>
      <!-- 제출 버튼 -->
      <button type="submit">{{ isEditing ? "Update" : "Submit" }}</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const route = useRoute();
const router = useRouter();

const title = ref('');
const content = ref('');
const rating = ref(0); // 선택된 별점 (소수점 포함)
const hoverRating = ref(0); // 마우스 오버 시 별점 상태
const isEditing = ref(false); // 수정 모드 여부

// 게시글 수정 시 기존 데이터를 로드
onMounted(() => {
  const articleId = route.query.id;
  if (articleId) {
    isEditing.value = true;
    store.getArticleById(articleId).then(() => {
      const article = store.currentArticle;
      title.value = article.title;
      content.value = article.content;
      rating.value = parseFloat(article.rating || 0); // 기존 별점 로드
    });
  }
});

// 마우스 오버 시 점수 업데이트
const updateHover = (event, star) => {
  const rect = event.target.getBoundingClientRect();
  const offsetX = event.clientX - rect.left; // 마우스 위치 계산
  const percentage = (offsetX / rect.width) * 100; // 별 채움 비율 계산
  hoverRating.value = star - 1 + percentage / 100; // 소수점 포함 계산
};

// 별점 설정
const setRating = () => {
  rating.value = hoverRating.value; // 마우스 위치 기반으로 점수 설정
};

// 마우스 오버 해제 시 원래 점수로 복구
const resetHover = () => {
  hoverRating.value = rating.value;
};

// 별의 채움 비율 계산
const getFillPercentage = (star) => {
  if (hoverRating.value >= star) {
    return 100; // 별이 완전히 채워짐
  } else if (hoverRating.value >= star - 1) {
    return (hoverRating.value - (star - 1)) * 100; // 부분적으로 채움
  }
  return 0; // 별이 비어 있음
};

// 게시글 작성 및 수정 요청
const submitArticle = async () => {
  const articleId = route.query.id;
  const payload = {
    title: title.value,
    content: content.value,
    rating: rating.value.toFixed(1), // 소수점 포함 점수
  };

  if (isEditing.value) {
    // 수정
    await store.updateArticle(articleId, payload);
  } else {
    // 새 게시글 작성
    store.createArticle(payload);
  }
  router.push({ name: 'ArticleView' }); // 작성/수정 완료 후 리스트 페이지로 이동
};
</script>

<style scoped>
.rating-container {
  margin-top: 20px;
}

.stars {
  display: flex;
  gap: 10px; /* 별 간격 */
  cursor: pointer;
}

.star {
  font-size: 2.5rem; /* 별 크기 */
  transition: background 0.2s ease-in-out;
  display: inline-block;
  color: lightgray; /* 초기 색상 */
  text-align: center;
  line-height: 1; /* 텍스트가 정렬되도록 설정 */
}

.rating-text {
  margin-top: 10px;
  font-weight: bold;
}
</style>
