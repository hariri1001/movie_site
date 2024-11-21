<template>
  <div class="container">
    <h1 class="title">누가 알겠어? 이 카드가 선택한 영화가 네 인생 영화를 만들지도?</h1>
    <div class="movie-cards">
      <div class="card_box" :class="{ 'spread': isSpread }">
        <div
          v-for="(movie, index) in movies"
          :key="movie.id"
          class="card_bind"
          :class="{ 'flip': isFlipped[index] }"
          @click="flipCard(index)"
        >
          <div class="front">
            <img src="/src/assets/card.png" alt="Card Back" />
          </div>
          <div class="back" :class="{ 'shine': isFlipped[index] }">
            <img :src="posterUrl(movie.poster_path)" alt="Movie Poster" />
            <h3>{{ movie.title }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- 모달 컴포넌트 추가 -->
    <MovieDetailModal
      v-if="showModal"
      :movie="selectedMovie"
      :showModal="showModal"
      @close="closeModal"
    />


  </div>
</template>

<script>
import MovieDetailModal from '@/components/movies/MovieDetailModal.vue'; // 모달 컴포넌트 import

export default {
  components: {
    MovieDetailModal,
  },
  data() {
    return {
      movies: [], 
      isFlipped: Array(5).fill(false),
      isSpread: false,
      showModal: false, // 모달 창의 표시 여부
      selectedMovie: null, // 선택된 영화 정보
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
      const apiKey = import.meta.env.VITE_TMDB_API_KEY;
      const randomPage = Math.floor(Math.random() * 500) + 1;
      
      try {
        const response = await fetch(
          `https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&page=${randomPage}&language=ko-KR`,
          {
            headers: {
              Authorization: `Bearer ${apiKey}`,
              'Content-Type': 'application/json'
            },
          }
        );

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const randomMovies = data.results.slice(0, 5);
        this.movies = randomMovies.map((movie) => ({
          id: movie.id,
          title: movie.title,
          poster_path: movie.poster_path,
          overview: movie.overview,
          release_date: movie.release_date,
          vote_average: movie.vote_average,
        }));

        setTimeout(() => {
          this.isSpread = true;
        }, 4400);

      } catch (error) {
        console.error("Error fetching movies:", error);
      }
    },
    // 카드 클릭시 뒤집고 두 번째 클릭 시 영화 상세 모달 띄우기
    flipCard(index) {
      // 첫 번째 클릭: 카드 뒤집기
      if (!this.isFlipped[index]) {
        this.isFlipped[index] = true;
      } else {
        // 두 번째 클릭: 모달 띄우기
        this.selectedMovie = this.movies[index];
        this.showModal = true;
      }
    },

    // 모달 닫기
    closeModal() {
      this.showModal = false;
      this.selectedMovie = null;
      // 카드 다시 뒤집기
      this.isFlipped = Array(5).fill(false);
    },
  },
  created() {
    this.getRandomMovies();
  },
};
</script>

<style scoped>
.container {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.title {
  text-align: center;
  margin-bottom: 50px;
  font-size: 35px;
  color: #eaeaea;
  width: 100%;
}



.movie-cards {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;

}

.card_box {
  position: relative;
  width: 100%;
  max-width: 1400px;
  height: 400px;
  margin: 0 auto;
}

.card_bind {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 180px;
  height: 270px;
  transform-style: preserve-3d;
  transition: all 1s ease;
  cursor: pointer;
  transform: translate(-50%, -50%);
}

.front, .back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

.front {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 10px;
  overflow: hidden;
  background-color: #222;
  background-image: url('@/assets/card.png'); /* 타로카드 배경 */
  background-size: cover;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  border: 5px solid gold; /* 타로카드의 고급스러운 테두리 */
}



.back {
  transform: rotateY(180deg);
  background: white;
}

/* 반짝이는 애니메이션 정의 */
@keyframes shineEffect {
  0% {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2), 0 0 20px rgba(255, 255, 255, 0.3);
  }
  50% {
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5), 0 0 30px rgba(255, 255, 255, 1);
  }
  100% {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2), 0 0 20px rgba(255, 255, 255, 0.3);
  }
}

/* 반짝이는 효과가 적용된 카드 */
.back.shine {
  animation: shineEffect 2s infinite; /* 애니메이션을 무한 반복 */
}






.card_bind.flip {
  transform: rotateY(180deg);
  /* animation: tarotFlip 2s ease-in-out forwards; */
}

/* 카드 셔플 애니메이션 */
.card_bind:nth-child(1) { z-index: 5; }
.card_bind:nth-child(2) {
  animation: shuffle2 0.3s 3 0.8s;
  z-index: 4;
}
.card_bind:nth-child(3) {
  animation: shuffle3 0.3s 2 1s;
  z-index: 3;
}
.card_bind:nth-child(4) {
  animation: shuffle4 3s;
  z-index: 2;
}
.card_bind:nth-child(5) {
  animation: shuffle5 3s;
  z-index: 1;
}


/* 카드 배치 위치 조정 */
.spread .card_bind:nth-child(1) { transform: translate(calc(-50% - 520px), -50%); }
.spread .card_bind:nth-child(2) { transform: translate(calc(-50% - 260px), -50%); }
.spread .card_bind:nth-child(3) { transform: translate(-50%, -50%); }
.spread .card_bind:nth-child(4) { transform: translate(calc(-50% + 260px), -50%); }
.spread .card_bind:nth-child(5) { transform: translate(calc(-50% + 520px), -50%); }

/* 뒤집힌 카드 위치 */
.spread .card_bind.flip { 
  transform: translate(var(--x), -50%) rotateY(180deg);
}

.spread .card_bind:nth-child(1).flip { --x: calc(-50% - 520px); }
.spread .card_bind:nth-child(2).flip { --x: calc(-50% - 260px); }
.spread .card_bind:nth-child(3).flip { --x: -50%; }
.spread .card_bind:nth-child(4).flip { --x: calc(-50% + 260px); }
.spread .card_bind:nth-child(5).flip { --x: calc(-50% + 520px); }

/* 셔플 애니메이션 수정 */
@keyframes shuffle2 {
  0% { transform: translate(-50%, -50%); }
  50% { transform: translate(calc(-50% - 60px), calc(-50% - 10px)) rotate(-5deg); }
  100% { transform: translate(-50%, -50%); }
}

@keyframes shuffle3 {
  0% { transform: translate(-50%, -50%); }
  50% { transform: translate(calc(-50% + 40px), calc(-50% + 10px)); }
  100% { transform: translate(-50%, -50%); }
}

@keyframes shuffle4 {
  30% { transform: translate(calc(-50% + 80px), -50%) rotate(15deg); }
  50% { transform: translate(calc(-50% - 20px), -50%); z-index: 1; }
  80% { transform: translate(calc(-50% - 10px), -50%); }
}

@keyframes shuffle5 {
  30% { transform: translate(calc(-50% - 50px), -50%) rotate(-15deg); }
  50% { transform: translate(calc(-50% + 20px), -50%); }
  80% { transform: translate(calc(-50% + 10px), -50%); }
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

h3 {
  position: absolute;
  bottom: 0;
  width: 100%;
  padding: 10px;
  margin: 0;
  background: rgba(0,0,0,0.7);
  color: white;
  font-size: 14px;
  text-align: center;
}
</style>