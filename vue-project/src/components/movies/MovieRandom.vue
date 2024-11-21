<template>
  <div class="movie-cards">
    <div
      class="flip-card"
      v-for="(movie, index) in movies"
      :key="movie.id"
      @click="flipCard(index)"
    >
      <div class="flip-card-inner" :class="{ 'flip': isFlipped[index] }">
        <!-- 카드 앞면 -->
        <div class="flip-card-front">
          <img src="https://via.placeholder.com/200x300?text=%3F" alt="Card Back" />
        </div>
        <!-- 카드 뒷면 -->
        <div class="flip-card-back">
          <img :src="posterUrl(movie.poster_path)" alt="Movie Poster" />
          <h3>{{ movie.title }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      movies: [], // 5개의 영화 데이터를 저장
      isFlipped: Array(5).fill(false), // 5개의 카드 상태 (뒤집혀진 여부)
    };
  },
  computed: {
    posterUrl() {
      return (path) => {
        return path
          ? `https://image.tmdb.org/t/p/w500${path}`
          : "https://via.placeholder.com/200x300?text=No+Image";
      };
    },
  },
  methods: {
    async getRandomMovies() {
      const apiKey  = import.meta.env.VITE_TMDB_API_KEY
      const randomPage = Math.floor(Math.random() * 500) + 1; // 1~500 중 랜덤 페이지 선택
      const url = "https://api.themoviedb.org/3/discover/movie";

      try {
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${apiKey}`, // Bearer Token 인증
          },
          params: {
            sort_by: "popularity.desc",
            page: randomPage,
            language: 'ko-KR',
          },
        });

        const data = response.data;
        const randomMovies = data.results.slice(0, 5); // 5개의 영화 가져오기
        this.movies = randomMovies.map((movie) => ({
          id: movie.id,
          title: movie.title,
          poster_path: movie.poster_path,
        }));
      } catch (error) {
        console.error("Error fetching movies:", error.response?.data || error.message);
      }
    },
    flipCard(index) {
      this.isFlipped[index] = !this.isFlipped[index]; // 클릭된 카드만 뒤집기
    },
  },
  created() {
    this.getRandomMovies();
  },
};

</script>

<style scoped>
.movie-cards {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.flip-card {
  perspective: 1000px;
  cursor: pointer;
  width: 200px; /* 카드 크기 조정 */
  height: 300px; /* 카드 크기 조정 */
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  text-align: center;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flip-card-inner.flip {
  transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
}

.flip-card-front {
  background-color: #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
}

.flip-card-back {
  transform: rotateY(180deg);
  background-color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

img {
  width: 100%;
  height: auto;
  object-fit: cover;
}
</style>
