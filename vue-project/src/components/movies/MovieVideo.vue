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
                :src="`https://www.youtube.com/embed/${selectedMovie.videoKey}?autoplay=1&mute=1&controls=0&rel=0&loop=1&playlist=${selectedMovie.videoKey}&modestbranding=1&showinfo=0`"
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
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const TMDB_KEY = import.meta.env.VITE_TMDB_API_KEY;
const selectedMovie = ref(null);

const formatDate = (dateString) => {
    const date = new Date(dateString);
    return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`;
};

const fetchTMDB = async (endpoint) => {
    const response = await fetch(`https://api.themoviedb.org/3${endpoint}`, {
        headers: {
            'Authorization': `Bearer ${TMDB_KEY}`,
            'Content-Type': 'application/json'
        }
    });
    if (!response.ok) {
        throw new Error(`TMDB API Error: ${response.status}`);
    }
    return response.json();
};


const findMovieWithTrailer = async (movies) => {
    for (const movie of movies) {
        const videosData = await fetchTMDB(`/movie/${movie.id}/videos?language=ko-KR`);
        
        // 예고편 찾기 (한국어 우선, 없으면 영어)
        let trailer = videosData.results.find(
            video => video.type === "Trailer" && video.site === "YouTube" && video.iso_639_1 === "ko"
        );
        
        // 한국어 예고편이 없으면 영어 예고편 검색
        if (!trailer) {
            trailer = videosData.results.find(
                video => video.type === "Trailer" && video.site === "YouTube"
            );
        }
        
        if (trailer) {
            return {
                ...movie,
                videoKey: trailer.key,  // 원래 키만 저장
                videoParams: {          // 유튜브 자막 숨김
                    cc_load_policy: 0
                }
            };
        }
    }
    return null;
};


const loading = ref(false);

const getRandomMovie = async () => {
    loading.value = true;
    try {
        const moviesData = await fetchTMDB('/movie/now_playing?language=ko-KR&page=1');
        
        if (!moviesData.results || moviesData.results.length === 0) {
            throw new Error('No movies found');
        }
        
        // 결과 배열을 랜덤하게 섞기
        const shuffledMovies = [...moviesData.results]
            .sort(() => Math.random() - 0.5);
        
        // 예고편이 있는 영화 찾기
        const movieWithTrailer = await findMovieWithTrailer(shuffledMovies);
        
        if (movieWithTrailer) {
            selectedMovie.value = movieWithTrailer;
        } else {
            // 예고편이 있는 영화를 찾지 못한 경우 재시도
            getRandomMovie();
        }
    } catch (error) {
        console.error('Error fetching movie data:', error);
        // 에러 발생시 재시도
        if (selectedMovie.value === null) {
            setTimeout(getRandomMovie, 1000);
        }
    } finally {
        loading.value = false;
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
    height: 600px;
    overflow: hidden;
}

.Movie-trailer iframe {
    position: absolute;
    width: 100%;
    height: 100%;
    pointer-events: none;
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        to bottom,
        rgba(0,0,0,0.1) 0%,
        rgba(0,0,0,0.3) 50%,
        rgba(0,0,0,0.7) 100%
    );
    z-index: 1;
    display: flex;
    align-items: flex-end;
    padding: 50px;
}

.content {
    color: white;
    max-width: 800px;
}

.movie-title {
    font-size: 3em;
    font-weight: bold;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}

.movie-desc {
    font-size: 1.2em;
    margin-bottom: 10px;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
}


.release-date {
    font-size: 1em;
    color: #ccc;
    margin-bottom: 20px;
}

.controls {
    display: flex;
    gap: 15px;
    align-items: center;
}

.control-btn {
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

.detail-btn {
    background-color: #e71a0f;
    color: white;
    font-weight: bold;
}

.detail-btn:hover {
    background-color: #c41810;
}
</style>