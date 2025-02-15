
<template>
  <div class="create-review-container">
    <h2>{{ isEditing ? "repost-it" : "코멘트 작성" }}</h2>
    
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
        <div class="left">
          <img 
            :src="`https://image.tmdb.org/t/p/w500${selectedMovie.posterPath}`" 
            :alt="selectedMovie.title" 
            class="movie-poster"
          />
        </div>
        <div class="right">
          <h3>{{ selectedMovie.title }}</h3>
          <p>개봉일: {{ selectedMovie.releaseDate }}</p>
          <p>줄거리: {{ selectedMovie.overview }}</p>
        </div>
        
      </div>
      
      


      <form @submit.prevent="submitReview" class="review-form">
        <div class="rating-container">
          <div class="rating-header">
            <h3>별점 : 
              <span class="stars" @mouseleave="resetHover">
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
              </span></h3>
              <p class="rating-text">선택한 별점: {{ rating.toFixed(1) }} / 5</p>
          </div>
        </div>

        <div class="review-content">
          <label>내용:</label>
          <textarea 
            v-model="content" 
            placeholder="영화에 대한 감상을 자유롭게 작성해주세요"
            rows="6"
          ></textarea>
        </div>

        <div class="button-group">
        <button type="submit" class="submit-button">
          {{ isEditing ? "repost-it" : "post-it" }}
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
import { useArticleStore } from '@/stores/article';
import { useMovieStore } from '@/stores/movie';

const articleStore = useArticleStore();
const movieStore = useMovieStore();
const route = useRoute();
const router = useRouter();

// store에서 필요한 상태들을 가져옴
const { searchResults, isLoading, error } = storeToRefs(movieStore);

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
  await movieStore.searchMovies(searchQuery.value);
};


const selectMovie = (movie) => {
  console.log(movie);
  selectedMovie.value = {
    id: movie.id,
    title: movie.title,
    posterPath: movie.posterPath, // poster_path로 수정
    releaseDate: movie.releaseDate, // releaseDate 추가
    overview: movie.overview,
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
    alert('커멘트 내용을 작성해주세요.');
    return;
  }

  console.log('선택된 영화:', selectedMovie.value); // 로그 추가
  
  const payload = {
    movieId: selectedMovie.value.id,
    movieTitle: selectedMovie.value.title,
    movie_poster_path: selectedMovie.value.posterPath,
    content: content.value,
    rating: rating.value.toFixed(1),
    overview: selectedMovie.value.overview,
    movie_release_date: selectedMovie.value.releaseDate, // 수정된 부분
  };

  try {
    if (isEditing.value) {
      await articleStore.updateArticle(route.query.id, payload);
    } else {
      await articleStore.createArticle(payload);
    }
    router.push({ name: 'ArticleView' });
  } catch (error) {
    console.error('리뷰 저장 실패:', error);
    alert('커멘트 저장에 실패했습니다.');
  }
};

const cancelReview = () => {
  router.push({ name: 'ArticleView' });
};


onMounted(async () => {
  const articleId = route.query.id;
  console.log('articleId:', articleId);
  if (articleId) {
    isEditing.value = true;
    await articleStore.getArticleById(articleId);
    const article = articleStore.currentArticle;
    selectedMovie.value = {
      id: article.movie_id,
      title: article.movie_title,
      posterPath: article.movie_poster_path,
      releaseDate: article.movie_release_date,
      overview: article.overview,
    };
    content.value = article.content;
    rating.value = parseFloat(article.rating || 0);
  }
});
</script>

<style scoped>
.create-review-container {
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
  /* border: 1px solid #00ba19; */
  border-radius: 8px;
  margin-top: 30px;
  background-color: #272727;
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
  background-color: #1da746;
}


/* 영화 정보 컨테이너 조정 */
.selected-movie-info {
  display: flex;
  gap: 30px;  /* 간격 증가 */
  align-items: flex-start;
  background-color: #1a1a1a;
  padding: 25px;
  border-radius: 8px;
  color: #F8F9FA;
  margin-top: 30px;
  position: relative; /* 추가 */
}

.stars {
  display: inline-flex;
  gap: 5px;
  cursor: pointer;
}

.star {
  font-size: 1.5rem;
  transition: background 0.2s ease-in-out;
}


.review-content {
  margin-bottom: 20px;
}

.review-content textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #6e6d6d;
  border-radius: 4px;
  resize: vertical;
  background-color: #1a1a1a;
  color: #F8F9FA;
}

.review-content label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}



.button-group {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: flex-end; /* 오른쪽 정렬 */
}

.submit-button, .cancel-button {
 background: none;
 border: 1px solid #ead200;
 color: #ffffff;
 padding: 4px 12px;
 border-radius: 8px;
 cursor: pointer;
 font-size: 0.85rem;
 min-width: 80px; /* 버튼 최소 너비 설정 */
 height: 35px; /* 버튼 높이 설정 */
 display: flex;
 align-items: center;
 justify-content: center;
 transition: all 0.2s;
}

.submit-button:hover, .cancel-button:hover {
 background-color: #ead200;
 color: rgb(3, 3, 3);
}

.rating-text {
  margin-top: 10px;
  font-weight: bold;
}

.movie-poster {
  position: relative; /* 추가 */
  width: 150px;
  height: 220px;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-left: 0 !important; /* 기존 margin-left 제거 */
}

.rating-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.rating-container {
  margin-bottom: 20px;
}

.rating-header h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  font-size: 1.0rem;
}

.rating-text {
  margin: 0;
  font-weight: bold;
}





.review-form {
  width: 100%;
  margin-top: 30px;
}





/* 오른쪽 영화 정보 스타일 */
.right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 줄거리 스타일 */
.overview {
  margin-top: 10px;
  line-height: 1.6;
  max-height: 150px;  /* 줄거리 높이 제한 */
  overflow-y: auto;
  padding-right: 10px;
}

/* 스크롤바 스타일링 */
.overview::-webkit-scrollbar {
  width: 6px;
}

.overview::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.overview::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

/* 줄거리 스타일 수정 */
.right p {
  margin: 0;
  padding: 5px 0;
}

/* 줄거리 텍스트 제한 */
.right p:last-child {
  display: -webkit-box;
  -webkit-line-clamp: 4; /* 4줄로 제한 */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.5;
  max-height: none; /* 기존 max-height 제거 */
  padding-right: 10px;
}


</style>