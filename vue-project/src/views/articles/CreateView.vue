
<template>
  <div class="create-review-container">
    <h1>{{ isEditing ? "영화 커멘트 수정" : "영화 커멘트 작성" }}</h1>
    
    <!-- 영화 검색 섹션 -->
    <div v-if="!selectedMovie && !isEditing" class="search-section">
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          @input="searchMovies"
          placeholder="영화 제목을 입력하세요"
          class="search-input"
        />
      </div>
      
      <div v-if="searchResults.length > 0" class="search-results">
        <div 
          v-for="movie in searchResults" 
          :key="movie.id"
          @click="selectMovie(movie)"
          class="movie-item"
        >
          <h3>{{ movie.title }}</h3>
          <p>{{ movie.releaseDate }}</p>
        </div>
      </div>
    </div>

    <!-- 선택된 영화 정보 및 리뷰 작성 폼 -->
    <div v-if="selectedMovie || isEditing" class="review-container">
      <div class="selected-movie-info">
        <img 
          :src="`https://image.tmdb.org/t/p/w500${selectedMovie.posterPath}`" 
          :alt="selectedMovie.title" 
          class="movie-poster"
        />
        <h2>{{ selectedMovie.title }}</h2>
        <p>개봉일: {{ selectedMovie.releaseDate }}</p>
      </div>

      <form @submit.prevent="submitReview" class="review-form">
        <div class="rating-container">
          <h3>별점</h3>
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
            >★</span>
          </div>
          <p class="rating-text">선택한 별점: {{ rating.toFixed(1) }} / 5</p>
        </div>

        <div class="review-content">
          <label>리뷰 내용:</label>
          <textarea 
            v-model="content" 
            placeholder="영화에 대한 감상을 자유롭게 작성해주세요"
            rows="6"
          ></textarea>
        </div>
        <div class="button-group">
        <button type="submit" class="submit-button">
          {{ isEditing ? "리뷰 수정" : "리뷰 등록" }}
        </button>
        <button type="button" @click="cancelReview" class="cancel-button">
          취소
        </button>
      </div>
        
      </form>
    </div>

    
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { storeToRefs } from 'pinia';  // storeToRefs 추가
import { useRoute, useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const route = useRoute();
const router = useRouter();

// store에서 필요한 상태들을 가져옴
const { searchResults, isLoading, error } = storeToRefs(store);

const searchQuery = ref('');
const selectedMovie = ref(null);
const content = ref('');
const rating = ref(0);
const hoverRating = ref(0);
const isEditing = ref(false);


// 영화 검색 함수를 store의 함수 사용하도록 수정
const searchMovies = async () => {
  if (searchQuery.value.length < 2) {
    return;
  }
  await store.searchMovies(searchQuery.value);
};


const selectMovie = (movie) => {
  console.log(movie);
  selectedMovie.value = {
    id: movie.id,
    title: movie.title,
    posterPath: movie.posterPath, // poster_path로 수정
    releaseDate: movie.release_date // releaseDate 추가
  };
  console.log(selectedMovie.value.posterPath);
  console.log('selectedMovie.value:', selectedMovie.value);
  searchQuery.value = '';
};

// 별점 관련 함수들
const updateHover = (event, star) => {
  const rect = event.target.getBoundingClientRect();
  const offsetX = event.clientX - rect.left;
  const percentage = (offsetX / rect.width) * 100;
  hoverRating.value = star - 1 + percentage / 100;
};

const setRating = () => {
  rating.value = hoverRating.value;
};

const resetHover = () => {
  hoverRating.value = rating.value;
};

const getFillPercentage = (star) => {
  const currentRating = hoverRating.value || rating.value;
  if (currentRating >= star) return 100;
  if (currentRating >= star - 1) return (currentRating - (star - 1)) * 100;
  return 0;
};

// 리뷰 제출
const submitReview = async () => {
  if (!selectedMovie.value && !isEditing.value) {
    alert('영화를 선택해주세요.');
    return;
  }

  if (rating.value === 0) {
    alert('별점을 선택해주세요.');
    return;
  }

  if (!content.value.trim()) {
    alert('리뷰 내용을 작성해주세요.');
    return;
  }

  console.log('선택된 영화:', selectedMovie.value); // 로그 추가

  const payload = {
    movieId: selectedMovie.value.id,
    movieTitle: selectedMovie.value.title,
    content: content.value,
    rating: rating.value.toFixed(1),
  };

  try {
    if (isEditing.value) {
      await store.updateArticle(route.query.id, payload);
    } else {
      await store.createArticle(payload);
    }
    router.push({ name: 'ArticleView' });
  } catch (error) {
    console.error('리뷰 저장 실패:', error);
    alert('리뷰 저장에 실패했습니다.');
  }
};

const cancelReview = () => {
  router.push({ name: 'ArticleView' });
};

// 수정 모드일 경우 기존 데이터 로드
onMounted(async () => {
  const articleId = route.query.id;
  if (articleId) {
    isEditing.value = true;
    await store.getArticleById(articleId);
    const article = store.currentArticle;
    selectedMovie.value = {
      id: article.movieId,
      title: article.movieTitle,
      posterPath: article.posterPath, // posterPath 추가
      releaseDate: article.releaseDate // releaseDate 추가
    };
    content.value = article.content;
    rating.value = parseFloat(article.rating || 0);
  }
});
</script>

<style scoped>
.create-review-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.search-section {
  margin-bottom: 30px;
}

.search-input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-results {
  margin-top: 10px;
  border: 1px solid #c4c3c3;
  border-radius: 4px;
  max-height: 300px;
  overflow-y: auto;
}

.movie-item {
  padding: 10px;
  cursor: pointer;
  border-bottom: 1px solid #797878;
}

.movie-item:hover {
  background-color: #f89595;
}

.selected-movie-info {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #aed5fc;
  border-radius: 4px;
}

.rating-container {
  margin: 20px 0;
}

.stars {
  display: flex;
  gap: 10px;
  cursor: pointer;
}

.star {
  font-size: 2.5rem;
  transition: background 0.2s ease-in-out;
}

.review-content textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #6e6d6d;
  border-radius: 4px;
}

.button-group {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.submit-button, .cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-button {
  background-color: #4CAF50;
  color: white;
}

.cancel-button {
  background-color: #f44336;
  color: white;
}

.rating-text {
  margin-top: 10px;
  font-weight: bold;
}

.movie-poster {
  max-width: 200px;
  height: auto;
  border-radius: 4px;
  margin-right: 20px;
}

.review-container {
  display: flex;
  gap: 40px;
}

.selected-movie-info {
  flex: 1; /* Take up 1 part of the available space */
  padding: 15px;
  background-color: #aed5fc;
  border-radius: 4px;
}

.review-form {
  flex: 1; /* Take up 1 part of the available space */
}

/* Responsive styles */
@media screen and (max-width: 768px) {
  .review-container {
    flex-direction: column;
  }
}

</style>