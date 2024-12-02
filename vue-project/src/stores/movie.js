// src/stores/movies.js
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from './auth';
import { api } from '@/api';

export const useMovieStore = defineStore("movies", () => {
  const authStore = useAuthStore();
  
  // 상태 관리
  const searchResults = ref([]);
  const isLoading = ref(false);
  const error = ref(null);
  const movie = ref(null);
  const likeCount = ref(0);
  const isLiked = ref(false);
  const recommendations = ref([]);
  const userTags = ref([]);
  const currentPage = ref(1);

  // TMDB API 설정
  const TMDB_API_KEY = import.meta.env.VITE_TMDB_API_KEY;
  const TMDB_BASE_URL = 'https://api.themoviedb.org/3';

  // computed
  const sortedTags = computed(() => {
    if (!userTags.value) return [];
    return Object.entries(userTags.value).sort((a, b) => b[1] - a[1]);
  });

  // 영화 검색
  const searchMovies = async (query) => {
    if (!query || query.length < 2) {
      searchResults.value = [];
      return;
    }

    try {
      isLoading.value = true;
      error.value = null;

      const response = await axios.get(`${TMDB_BASE_URL}/search/movie`, {
        headers: {
          'Authorization': `Bearer ${TMDB_API_KEY}`,
          'Content-Type': 'application/json'
        },
        params: {
          query: query,
          language: 'ko-KR'
        }
      });

      searchResults.value = response.data.results.map(movie => ({
        id: movie.id,
        title: movie.title,
        releaseDate: movie.release_date,
        posterPath: movie.poster_path ? `https://image.tmdb.org/t/p/w500${movie.poster_path}` : null,
        overview: movie.overview
      }));
    } catch (err) {
      console.error('영화 검색 실패:', err);
      error.value = '영화를 검색하는 중 오류가 발생했습니다.';
      searchResults.value = [];
    } finally {
      isLoading.value = false;
    }
  };

  // 영화 상세 정보
  const getMovieDetails = async (movieId) => {
    try {
      const response = await axios.get(`${TMDB_BASE_URL}/movie/${movieId}`, {
        headers: {
          'Authorization': `Bearer ${TMDB_API_KEY}`,
          'Content-Type': 'application/json'
        },
        params: {
          language: 'ko-KR'
        }
      });
      return response.data;
    } catch (err) {
      console.error('영화 상세 정보 조회 실패:', err);
      throw err;
    }
  };

  // 좋아요 기능
  const toggleLike = async (movieId) => {
    try {
      const response = await axios.post(
        `${authStore.API_URL}/api/v1/movies/${movieId}/likes/`,
        {},
        {
          headers: { Authorization: `Token ${authStore.token}` },
        }
      );
      isLiked.value = response.data.liked;
      likeCount.value = response.data.like_count;
      return true;
    } catch (error) {
      console.error('좋아요 처리 중 에러 발생:', error);
      return false;
    }
  };

  // 좋아요 상태 확인
  const checkLikeStatus = async (movieId) => {
    try {
      const response = await axios.get(
        `${authStore.API_URL}/api/v1/movies/${movieId}/`,
        {
          headers: { Authorization: `Token ${authStore.token}` },
        }
      );
      isLiked.value = response.data.is_liked;
      likeCount.value = response.data.like_count;
    } catch (error) {
      console.error('좋아요 상태 확인 중 에러 발생:', error);
    }
  };

  // 사용자가 좋아요한 영화 목록
  const getUserLikedMovies = async (username) => {
    try {
      const response = await axios.get(
        `${authStore.API_URL}/movies/liked-movies/${username}/`,
        {
          headers: { Authorization: `Token ${authStore.token}` },
        }
      );
      console.log('좋아요한 영화 응답:', response.data);
      return response.data;
    } catch (error) {
      console.error('좋아요한 영화 조회 실패:', error);
      throw error;
    }
  };

  return {
    // 상태
    searchResults,
    isLoading,
    error,
    movie,
    likeCount,
    isLiked,
    recommendations,
    userTags,
    currentPage,
    
    // computed
    sortedTags,
    
    // 메서드
    searchMovies,
    getMovieDetails,
    toggleLike,
    checkLikeStatus,
    getUserLikedMovies
  };
});