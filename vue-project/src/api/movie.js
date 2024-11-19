import axios from 'axios'

// Django URL 구조에 맞춘 기본 URL 설정
const API_URL = 'http://127.0.0.1:8000/api/v1/movies/'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
})

export const movieApi = {
  // 영화 검색
  searchMovies(query) {
    return apiClient.get('search/', {
      params: {
        q: query
      }
    })
  },

  // 영화 저장
  saveMovie(movieData) {
    return apiClient.post('save/', movieData)
  },

  // 장르 목록 조회
  getGenres() {
    return apiClient.get('genres/')
  },

  // 장르별 영화 조회
  getMoviesByGenre(genreId) {
    return apiClient.get(`genres/${genreId}/`)
  },

  // 좋아요 토글
  toggleLike(movieId) {
    return apiClient.post(`${movieId}/likes/`)
  }
}