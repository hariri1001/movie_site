<!-- components/MovieLikeButton.vue -->
<template>
    <button 
      @click="handleLike" 
      class="like-button"
      :class="{ 'liked': movieStore.isLiked }"
    >
      <span class="like-icon">♥</span>
      <span class="like-count">{{ movieStore.likeCount }}</span>
    </button>
</template>
  
<script setup>
  import { useMovieStore } from '@/stores/movie'
  
  const props = defineProps({
    movieId: {
      type: Number,
      required: true
    }
  })
  
  const movieStore = useMovieStore()
  
  const handleLike = async () => {
    await movieStore.toggleLike(props.movieId)
  }
</script>
  
<style scoped>
  .like-button {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border: none;
    border-radius: 20px;
    background: #333;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .like-button.liked {
    background: #ff4444;
  }
  
  .like-icon {
    font-size: 1.2em;
  }
  
  .like-count {
    font-size: 0.9em;
  }
</style>