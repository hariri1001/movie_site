import { defineStore } from 'pinia'
import axios from 'axios'

export const useMovieStore = defineStore('movie', {
  state: () => ({
    movie: null,
    likeCount: 0,
    isLiked: false
  }),

  actions: {
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
    }
  }
})