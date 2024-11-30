import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from './auth';
import { useMovieStore } from './movie';

export const useArticleStore = defineStore("articles", () => {
  const authStore = useAuthStore();
  const movieStore = useMovieStore();
  
  const articles = ref([]);
  const currentArticle = ref(null);

  const getArticles = async () => {
    try {
      console.log('게시글 목록 요청 시작');
      const response = await axios.get(
        `${authStore.API_URL}/api/v1/articles/list/`,
        {
          headers: { Authorization: `Token ${authStore.token}` }
        }
      );
      articles.value = response.data;
    } catch (error) {
      console.error('게시글 목록 가져오기 실패:', error.response?.data || error);
    }
  };

  const getArticleById = async (articleId) => {
    try {
      const response = await axios.get(`${authStore.API_URL}/api/v1/articles/${articleId}/`, {
        headers: { Authorization: `Token ${authStore.token}` },
      });
      currentArticle.value = response.data;
    } catch (error) {
      console.error('게시글 상세 불러오기 실패:', error.response?.data || error);
    }
  };

  const createArticle = async (payload) => {
    try {
      const movieDetails = await movieStore.getMovieDetails(payload.movieId);
      const response = await axios.post(
        `${authStore.API_URL}/api/v1/articles/`,
        {
          title: `${movieDetails.title} 리뷰`,
          content: payload.content,
          rating: payload.rating,
          movie_id: payload.movieId,
          movie_title: movieDetails.title,
          movie_poster_path: movieDetails.poster_path,
          movie_release_date: movieDetails.release_date,
          movie_overview: movieDetails.overview
        },
        {
          headers: { Authorization: `Token ${authStore.token}` },
        }
      );
      articles.value.unshift(response.data);
      return true;
    } catch (error) {
      console.error('리뷰 작성 실패:', error.response?.data || error);
      return false;
    }
  };

  const updateArticle = async (articleId, payload) => {
    try {
      const movieDetails = await movieStore.getMovieDetails(payload.movieId);
      await axios.put(
        `${authStore.API_URL}/api/v1/articles/${articleId}/`,
        {
          title: `${movieDetails.title} 리뷰`,
          content: payload.content,
          rating: payload.rating,
          movieId: payload.movieId,
          movieTitle: movieDetails.title,
          moviePosterPath: movieDetails.poster_path,
          movieReleaseDate: movieDetails.release_date,
          movieOverview: movieDetails.overview
        },
        {
          headers: { Authorization: `Token ${authStore.token}` },
        }
      );
      await getArticles();
      return true;
    } catch (error) {
      console.error('리뷰 수정 실패:', error.response?.data || error);
      return false;
    }
  };

  const deleteArticle = async (articleId) => {
    try {
      await axios.delete(`${authStore.API_URL}/api/v1/articles/${articleId}/`, {
        headers: {
          Authorization: `Token ${authStore.token}`,
        },
      });
      await getArticles();
      return true;
    } catch (error) {
      console.error("게시글 삭제 실패:", error);
      return false;
    }
  };

  const toggleArticleLike = async (articleId) => {
    try {
      const response = await axios.post(
        `${authStore.API_URL}/api/v1/articles/${articleId}/like/`,
        {},
        {
          headers: { Authorization: `Token ${authStore.token}` },
        }
      );
      const { liked, likes_count } = response.data;
  
      const targetArticle = articles.value.find((article) => article.id === articleId);
      if (targetArticle) {
        targetArticle.isLiked = liked;
        targetArticle.likes_count = likes_count;
      }
  
      return { liked, likes_count };
    } catch (error) {
      console.error("좋아요 API 호출 실패:", error);
      throw error;
    }
  };

  const getUserArticles = async (username) => {
    try {
      const response = await axios.get(
        `${authStore.API_URL}/api/v1/articles/user/`,
        {
          headers: { Authorization: `Token ${authStore.token}` },
          params: { username }
        }
      );
      return response.data;
    } catch (error) {
      console.error('사용자 게시글 조회 실패:', error);
      throw error;
    }
  };

  // Computed properties
  const sortedByRating = computed(() => {
    return [...articles.value].sort((a, b) => b.rating - a.rating);
  });

  const sortedByLatest = computed(() => {
    return [...articles.value].sort((a, b) => 
      new Date(b.created_at) - new Date(a.created_at)
    );
  });

  const sortedByLikes = computed(() => {
    return [...articles.value].sort((a, b) => 
      (b.likes_count || 0) - (a.likes_count || 0)
    );
  });

  return {
    articles,
    currentArticle,
    getArticles,
    getArticleById,
    createArticle,
    updateArticle,
    deleteArticle,
    toggleArticleLike,
    getUserArticles,
    sortedByRating,
    sortedByLatest,
    sortedByLikes,
  };
});