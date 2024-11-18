<template>
    <div>
        <MovieListView/>
    </div>
    <!-- <section class="my-5">
        <div class="container-fluid">
        <h1 class="text-center mb-5 fw-bold">Box Office</h1>
        <div class="row g-4">
            <div v-for="movie in movies" 
                 :key="movie.id" 
                 class="col-12 col-sm-4 col-md-2-4 col-lg-1-7">
            <div class="movie-card">
                <div class="poster-wrapper">
                    <img 
                        :src="getMovieImageUrl(movie.poster_path)" 
                        :alt="movie.title" 
                        class="poster-image"
                    >
                </div>
            </div>
            </div>
        </div>
        </div>
    </section> -->
</template>

<script setup>
// import { ref, onMounted } from 'vue'
import MovieListView from './MovieListView.vue';

// const movies = ref([])
// const baseImageUrl = "https://image.tmdb.org/t/p/w500"

// const getMovieImageUrl = (posterPath) => {
//     return baseImageUrl + posterPath
// }

// onMounted(async () => {
//     try {
//         const response = await fetch('/movies.json')
//         movies.value = await response.json()
//     } catch (error) {
//         console.error('영화 데이터를 불러오는 중 오류 발생:', error)
//     }
// })
</script>

<style scoped>
h1 {
    color: rgb(3, 155, 8);
}
.container-fluid {
    padding: 0 2rem;
    max-width: 1800px;
    margin: 0 auto;
}

/* 반응형 그리드 클래스 */
.col-lg-1-7 {
    flex: 0 0 auto;
    width: calc(100% / 7); /* 7개 */
}

.col-md-2-4 {
    flex: 0 0 auto;
    width: 20%; /* 5개 */
}

@media (min-width: 576px) {
    .col-sm-4 {
        flex: 0 0 auto;
        width: 33.333%; /* 3개 */
    }
}

@media (max-width: 576px) {
    .col-12 {
        flex: 0 0 auto;
        width: 100%; /* 1개 */
    }
}

/* 카드 스타일링 */
.movie-card {
    height: 100%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    border: none;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    position: relative;
    border-radius: 8px;
    overflow: hidden;
}

.movie-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.poster-wrapper {
    position: relative;
    width: 100%;
    padding-top: 150%;
    overflow: hidden;
}

.poster-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.movie-card:hover .poster-image {
    transform: scale(1.05);
}
</style>