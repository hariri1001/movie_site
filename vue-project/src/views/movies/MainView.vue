<template>
    <div>
        <MovieVideo/>
        <MovieListView/>
        <GenreMovies/>
    </div>
    
</template>

<script setup>

import MovieListView from './MovieListView.vue';
import MovieVideo from '@/components/movies/MovieVideo.vue';
import GenreMovies from '@/components/movies/GenreMovies.vue';

</script>

<style scoped>

</style>