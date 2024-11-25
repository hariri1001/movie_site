<template>
    <div>
        <div v-if="loading" class="Movie-trailer">
            <div class="overlay">
                <div class="content">
                    <h1 class="movie-title">로딩중...</h1>
                </div>
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
            <div class="overlay">
                <div class="content">
                    <h1 class="movie-title">{{ selectedMovie.title }}</h1>
                    <p class="movie-desc">{{ selectedMovie.overview }}</p>
                    <p class="release-date">{{ formatDate(selectedMovie.release_date) }} 개봉</p>
                </div>
            </div>
            <!-- 스크롤 안내 -->
            <div class="scroll-indicator" @click="scrollToNextSection">
                <p>Click</p>
                <div class="arrow"></div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const TMDB_KEY = import.meta.env.VITE_TMDB_API_KEY;
const selectedMovie = ref(null);
const loading = ref(false);

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
    } catch (error) {
        console.error('Error fetching movie data:', error);
    } finally {
        loading.value = false;
    }
};

// 아래로 스크롤 함수
const scrollToNextSection = () => {
    const nextSection = document.querySelector('.carousel-container'); // 스크롤할 섹션
    if (nextSection) {
        nextSection.scrollIntoView({ behavior: 'smooth' }); // 부드러운 스크롤
    }
};

onMounted(() => {
    getRandomMovie();
});
</script>

<style scoped>
.Movie-trailer {
    position: relative;
    width: 100%;
    height: 100vh; /* 화면 전체 높이 */
    overflow: hidden;
}

.Movie-trailer iframe {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 120%; /* 너비를 120%로 확장 */
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

.content {
    color: white;
    max-width: 800px;
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

/* 스크롤 안내 스타일 */
.scroll-indicator {
    position: absolute;
    bottom: 10px; /* 화면 더 아래쪽으로 이동 */
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    color: white;
    font-size: 2rem; /* 텍스트 크기는 유지 */
    font-weight: bold;
    cursor: pointer;
    animation: pulse 1.5s infinite; /* 클릭 버튼에 맥박 효과 추가 */
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8); /* 텍스트 그림자 추가 */
}

.scroll-indicator .arrow {
    width: 30px; /* 화살표 크기 유지 */
    height: 30px;
    border: solid white;
    border-width: 0 3px 3px 0;
    display: inline-block;
    margin-top: 0px; /* 클릭 버튼과 화살표 간격을 줄임 */
    transform: rotate(45deg); /* 화살표를 대각선 아래 방향으로 설정 */
    animation: bounce 1.5s infinite; /* 위아래로 움직이는 애니메이션 */
    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5); /* 화살표 테두리 그림자 효과 추가 */
}

/* 애니메이션 유지 */
@keyframes bounce {
    0%, 100% {
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