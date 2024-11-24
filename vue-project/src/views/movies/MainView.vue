<template>
    <div>
        <MovieVideo/>
        <MovieListView/>
        <GenreMovies/>
        <LatestArticles />
    </div>
    <!-- <router-view /> -->
    <!-- 챗봇 버튼 추가 -->
    <ChatbotButton />
</template>

<script setup>

import MovieListView from './MovieListView.vue';
import MovieVideo from '@/components/movies/MovieVideo.vue';
import GenreMovies from '@/components/movies/GenreMovies.vue';
import ChatbotButton from '@/components/ChatbotButton.vue';
import LatestArticles from '@/components/Articles/LatestArticles.vue';



</script>

<style scoped>

</style>