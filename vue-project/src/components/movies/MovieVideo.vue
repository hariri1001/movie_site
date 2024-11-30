<template>
  <div>
    <div class="carousel-container">
      <PopularMoviesCarousel 
        :popularMovies="popularMovies"
        :movePopular="movePopular"
        :isEndOfPopular="isEndOfPopular"
        :popularPosition="popularPosition" />
    </div>
    <div v-if="loading" class="Movie-trailer">
        <div class="overlay">
        </div>
    </div>
    <div v-else-if="selectedMovie" class="Movie-trailer">
      <iframe 
          width="100%" 
          height="100%" 
          :src="`https://www.youtube.com/embed/${selectedMovie.videoKey}?autoplay=1&mute=1&controls=0&rel=0&loop=1&playlist=${selectedMovie.videoKey}&modestbranding=1&showinfo=0&iv_load_policy=3&fs=0&disablekb=1&playsinline=1`"
          frameborder="0" 
          allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen>
      </iframe>
      <!-- <div class="overlay">
          <div class="content">
              <h1 class="movie-title">{{ selectedMovie.title }}</h1>
              <p class="movie-desc">{{ selectedMovie.overview }}</p>
              <p class="release-date">{{ formatDate(selectedMovie.release_date) }} 개봉</p>
          </div>
      </div> -->
    </div>
  </div>
      
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import PopularMoviesCarousel from '@/components/movies/PopularMoviesCarousel.vue';

const TMDB_KEY = import.meta.env.VITE_TMDB_API_KEY;
const selectedMovie = ref(null);
const loading = ref(false);

const popularMovies = ref([]);
const popularPosition = ref(0);
const cardWidth = 250;
const visibleCards = 5;

const isEndOfPopular = computed(() => {
  if (!popularMovies.value.length) return true;
  return popularPosition.value >= (popularMovies.value.length - visibleCards) * cardWidth;
});

const movePopular = (direction) => {
  if (direction === 'next' && !isEndOfPopular.value) {
    popularPosition.value += cardWidth;
  } else if (direction === 'prev' && popularPosition.value > 0) {
    popularPosition.value -= cardWidth;
  }
};





const formatDate = (dateString) => {
    const date = new Date(dateString);
    return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`;
};

const fetchTMDB = async (endpoint) => {
    const response = await fetch(`https://api.themoviedb.org/3${endpoint}`, {
        headers: {
            Authorization: `Bearer ${TMDB_KEY}`,
            'Content-Type': 'application/json',
        },
    });
    if (!response.ok) {
        throw new Error(`TMDB API Error: ${response.status}`);
    }
    return response.json();
};

const findMovieWithTrailer = async (movies) => {
    for (const movie of movies) {
        const videosData = await fetchTMDB(`/movie/${movie.id}/videos?language=ko-KR`);
        let trailer = videosData.results.find(
            (video) => video.type === 'Trailer' && video.site === 'YouTube' && video.iso_639_1 === 'ko'
        );
        if (!trailer) {
            trailer = videosData.results.find(
                (video) => video.type === 'Trailer' && video.site === 'YouTube'
            );
        }
        if (trailer) {
            return { ...movie, videoKey: trailer.key };
        }
    }
    return null;
};

const getRandomMovie = async () => {
    loading.value = true;
    try {
      const moviesData = await fetchTMDB('/movie/now_playing?language=ko-KR&page=1');
      const shuffledMovies = [...moviesData.results].sort(() => Math.random() - 0.5);
      const movieWithTrailer = await findMovieWithTrailer(shuffledMovies);
      if (movieWithTrailer) {
          selectedMovie.value = movieWithTrailer;
      }
      // 인기 상영작 영화 데이터 가져오기
      const popularMoviesData = await fetchTMDB('/movie/popular?language=ko-KR&page=1');
      popularMovies.value = popularMoviesData.results;
    } catch (error) {
        console.error('Error fetching movie data:', error);
    } finally {
        loading.value = false;
    }
};


onMounted(() => {
    getRandomMovie();
});

</script>

<style scoped>
.carousel-container {
  position: absolute;
  top: 80%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  width: 100%; /* 캐러셀 너비를 80%로 설정 */
  max-width: 1400px; /* 최대 너비를 1400px로 제한 */
  height: 70%; /* 캐러셀 높이를 70%로 설정 */
}

.Movie-trailer::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4); /* 어둡게 하는 반투명 검정색 배경 */
  z-index: 1;
}



.Movie-trailer {
  position: relative;
  width: 100%;
  height: 100vh; /* 화면 전체 높이 */
  overflow: hidden;
  z-index: 0; /* 비디오 영상을 배경으로 배치 */
}

.Movie-trailer iframe {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%; /* 너비를 120%로 확장 */
    height: 120%; /* 높이를 120%로 확장 */
    transform: translate(-50%, -50%); /* 중앙 정렬 */
    pointer-events: none; /* 클릭 방지 */
}

.overlay {
  position: absolute;
  top: 50%;
  left: 2%;
  transform: translateY(-50%);
  width: auto;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 0;
  background: none;
}

.movie-title {
  font-size: 2.5em;
  font-weight: bold;
  margin-bottom: 10px;
}

.movie-desc {
  font-size: 1em;
  margin-bottom: 10px;
}

.release-date {
  font-size: 1em;
  color: #ccc;
  margin-bottom: 20px;
}


/* 애니메이션 유지 */
@keyframes bounce {
  0%,
  100% {
    transform: translateY(0) rotate(45deg);
  }
  50% {
    transform: translateY(10px) rotate(45deg);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1); /* 버튼이 커졌다가 */
    opacity: 0.8; /* 투명도가 살짝 줄어듦 */
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>