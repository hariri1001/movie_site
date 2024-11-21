// src/stores/movies.js
import { defineStore } from 'pinia'
import axios from 'axios'



export const useMovieStore = defineStore('movie', {
  state: () => ({
    // 기존 상태
    movie: null,
    likeCount: 0,
    isLiked: false,
    
    // 추천 시스템 관련 상태 추가
    recommendations: [],
    userTags: [],
    currentPage: 1,
    loading: false
  }),

  getters: {
    // 태그 정렬을 위한 getter
    sortedTags: (state) => {
      if (!state.userTags) return []
      return Object.entries(state.userTags).sort((a, b) => b[1] - a[1])
    }
  },

  actions: {
    // 기존 액션들
    async toggleLike(movieId) {
      try {
        const response = await axios.post(`/api/v1/movies/${movieId}/likes/`)
        this.isLiked = response.data.liked
        this.likeCount = response.data.like_count
        return true
      } catch (error) {
        console.error('좋아요 처리 중 에러 발생:', error)
        return false
      }
    },

    async checkLikeStatus(movieId) {
      try {
        const response = await axios.get(`/api/v1/movies/${movieId}/`)
        this.isLiked = response.data.is_liked
        this.likeCount = response.data.like_count
      } catch (error) {
        console.error('좋아요 상태 확인 중 에러 발생:', error)
      }
    },
   
  }
})