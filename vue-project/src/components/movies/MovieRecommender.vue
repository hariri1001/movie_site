<template>
  <div class="movie-recommender">
    <!-- 로딩 상태 표시 -->
    <div v-if="isLoading" class="text-center p-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- 에러 메시지 표시 -->
    <div v-else-if="errorMessage" class="alert alert-danger m-4" role="alert">
      {{ errorMessage }}
    </div>

    <!-- 메인 콘텐츠 -->
    <div v-else class="modal-content-wrapper">
      <!-- 질문 섹션 -->
      <div v-if="!showResults" class="question-section p-4">
        <h2 class="question-text">{{ currentQuestion?.text || '질문을 불러오는 중...' }}</h2>
        <div class="d-grid gap-3" v-if="currentQuestion?.options">
          <button 
            v-for="option in currentQuestion.options" 
            :key="option" 
            @click="handleAnswer(option)" 
            class="btn option-btn"
          >
            {{ option }}
          </button>
        </div>
      </div>
      
      <!-- 결과 섹션 -->
      <div v-else>
        <div class="results-section p-4">
          <h2 class="results-title mb-4">추천 영화 목록</h2>
          <div class="row row-cols-1 row-cols-md-2 g-4">
            <div v-for="movie in recommendations.slice(0, 4)" 
                 :key="movie.title" 
                 class="col">
              <div class="card h-100 shadow-sm">
                <img :src="movie.posterUrl" 
                     class="card-img-top" 
                     :alt="movie.title"
                     style="height: 300px; object-fit: cover;"
                     @error="e => e.target.src = '/default-movie-poster.jpg'">
                <div class="card-body">
                  <h5 class="card-title mb-2">{{ movie.title }}</h5>
                  <p class="card-text small text-muted" v-if="movie.originalTitle">
                    {{ movie.originalTitle }}
                  </p>
                  <div class="d-flex flex-wrap gap-2 mb-2">
                    <span class="badge bg-primary" v-if="movie.genres">{{ movie.genres }}</span>
                    <span class="badge bg-success">평점: {{ movie.rating }}</span>
                    <span v-if="movie.tmdbRating" class="badge bg-info">
                      TMDB: {{ movie.tmdbRating.toFixed(1) }}
                    </span>
                  </div>
                  <p class="card-text small text-muted" v-if="movie.releaseDate || movie.runtime">
                    <span v-if="movie.releaseDate">
                      개봉: {{ new Date(movie.releaseDate).toLocaleDateString('ko-KR') }}
                    </span>
                    <span v-if="movie.runtime" class="ms-2">
                      {{ Math.floor(movie.runtime / 60) }}시간 {{ movie.runtime % 60 }}분
                    </span>
                  </p>
                  <p class="card-text description" v-if="movie.description">
                    {{ movie.description.length > 50 ? movie.description.slice(0, 50) + '...' : movie.description }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- 푸터 영역 -->
        <div class="modal-footer border-0" style="background-color: rgb(247, 218, 125);">
          <button @click="resetQuiz" class="btn btn-primary w-100">
            다시 시작하기
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'MovieRecommender',
  setup() {
    // 상태 관리
    const isLoading = ref(false)
    const errorMessage = ref('')
    const currentQuestionIndex = ref(0)
    const answers = ref({})
    const recommendations = ref([])
    const showResults = ref(false)

    // TMDB API 설정
    const TMDB_ACCESS_TOKEN = import.meta.env.VITE_TMDB_API_KEY
    const TMDB_BASE_URL = 'https://api.themoviedb.org/3'
    const TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

    // 질문 목록
    const questions = [
      {
        id: 1,
        text: "선호하는 영화 장르를 선택해주세요.",
        options: ["액션", "로맨스", "공포", "코미디", "SF"]
      },
      {
        id: 2,
        text: "영화 관람 시 가장 중요하게 생각하는 요소는?",
        options: ["스토리", "연기력", "시각효과", "음악", "메시지"]
      },
      {
        id: 3,
        text: "어떤 분위기의 영화를 선호하시나요?",
        options: ["밝고 유쾌한", "진지한", "감동적인", "스릴있는", "몽환적인"]
      }
    ]

    const currentQuestion = computed(() => {
      return questions[currentQuestionIndex.value]
    })

    // TMDB API 설정 확인
    onMounted(() => {
      if (!TMDB_ACCESS_TOKEN) {
        errorMessage.value = 'TMDB Access Token이 설정되지 않았습니다. .env 파일을 확인해주세요.'
        console.error('TMDB Access Token이 없습니다!')
        return
      }
      console.log('Token check:', TMDB_ACCESS_TOKEN.substring(0, 10) + '...')
    })

    // TMDB API 호출을 위한 기본 설정
    const options = {
      method: 'GET',
      headers: {
        accept: 'application/json',
        Authorization: `Bearer ${TMDB_ACCESS_TOKEN}`
      }
    }

    // TMDB API를 통해 영화 정보를 검색하는 함수
    const searchMovieInTMDB = async (movieTitle) => {
      try {
        isLoading.value = true
        if (!TMDB_ACCESS_TOKEN) {
          throw new Error('TMDB Access Token이 설정되지 않았습니다.')
        }

        const searchUrl = `${TMDB_BASE_URL}/search/movie?query=${encodeURIComponent(movieTitle)}&language=ko-KR&include_adult=false`
        console.log('Making request to:', searchUrl)

        const searchResponse = await fetch(searchUrl, options)

        if (!searchResponse.ok) {
          const errorData = await searchResponse.json()
          console.error('TMDB API Error:', {
            status: searchResponse.status,
            statusText: searchResponse.statusText,
            error: errorData
          })
          throw new Error(`TMDB API Error: ${searchResponse.status}`)
        }

        const searchData = await searchResponse.json()
        
        if (!searchData.results || searchData.results.length === 0) {
          console.log(`No results found for: ${movieTitle}`)
          return null
        }

        const movie = searchData.results[0]
        
        const detailsUrl = `${TMDB_BASE_URL}/movie/${movie.id}?language=ko-KR`
        const detailsResponse = await fetch(detailsUrl, options)

        if (!detailsResponse.ok) {
          throw new Error('Failed to fetch movie details')
        }

        const details = await detailsResponse.json()

        return {
          posterUrl: movie.poster_path ? `${TMDB_IMAGE_BASE_URL}${movie.poster_path}` : '/default-movie-poster.jpg',
          description: movie.overview || details.overview || '',
          releaseDate: movie.release_date || '',
          tmdbRating: movie.vote_average || null,
          runtime: details.runtime || null,
          genres: details.genres?.map(genre => genre.name).join(', ') || '',
          originalTitle: movie.original_title || ''
        }
      } catch (error) {
        console.error('TMDB API Error:', error)
        errorMessage.value = '영화 정보를 가져오는데 실패했습니다.'
        return null
      } finally {
        isLoading.value = false
      }
    }

    // 답변 처리 함수
    const handleAnswer = async (answer) => {
      try {
        answers.value[currentQuestionIndex.value] = answer
        
        if (currentQuestionIndex.value < questions.length - 1) {
          currentQuestionIndex.value++
        } else {
          await getRecommendations()
        }
      } catch (error) {
        console.error('Error handling answer:', error)
        errorMessage.value = '답변 처리 중 오류가 발생했습니다.'
      }
    }

    // 영화 추천을 가져오고 TMDB 정보를 추가하는 함수
    const getRecommendations = async () => {
      try {
        isLoading.value = true
        errorMessage.value = ''

        const response = await fetch('http://localhost:8000/movies/api/recommend/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(answers.value)
        })
        
        if (!response.ok) {
          throw new Error('추천 API 호출 실패')
        }
        
        const initialRecommendations = await response.json()

        const enhancedRecommendations = await Promise.all(
          initialRecommendations.map(async (movie) => {
            try {
              const tmdbInfo = await searchMovieInTMDB(movie.title)
              return {
                ...movie,
                posterUrl: tmdbInfo?.posterUrl || '/default-movie-poster.jpg',
                description: tmdbInfo?.description || '',
                releaseDate: tmdbInfo?.releaseDate || '',
                tmdbRating: tmdbInfo?.tmdbRating || null,
                runtime: tmdbInfo?.runtime || null,
                genres: tmdbInfo?.genres || '',
                originalTitle: tmdbInfo?.originalTitle || ''
              }
            } catch (error) {
              console.error(`영화 '${movie.title}' 정보 가져오기 실패:`, error)
              return movie
            }
          })
        )
        
        recommendations.value = enhancedRecommendations
        showResults.value = true
      } catch (error) {
        console.error('Error:', error)
        errorMessage.value = '영화 추천 정보를 가져오는데 실패했습니다.'
      } finally {
        isLoading.value = false
      }
    }

    // 퀴즈 초기화
    const resetQuiz = () => {
      currentQuestionIndex.value = 0
      answers.value = {}
      recommendations.value = []
      showResults.value = false
      errorMessage.value = ''
    }

    return {
      isLoading,
      errorMessage,
      currentQuestion,
      questions,
      currentQuestionIndex,
      answers,
      recommendations,
      showResults,
      handleAnswer,
      resetQuiz
    }
  }
}
</script>

<style scoped>
.movie-recommender {
  background-color: white;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.modal-content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.question-section {
  flex: 1;
  background-color: white;
}

.results-section {
  background-color: white;
  overflow-y: auto;
}

.question-text {
  font-size: 1.75rem;
  font-weight: 500;
  margin-bottom: 2rem;
  color: #333;
}

.option-btn {
  height: 60px;
  font-size: 1.2rem;
  color: #000000;
  background-color: #fcaaff;
  border: none;
  text-align: left;
  transition: all 0.3s ease;
}

.option-btn:hover {
  background-color: #f3f4f6;
  transform: translateY(-2px);
}

.results-title {
  font-size: 1.75rem;
  font-weight: 500;
  text-align: center;
  color: #333;
}

.description {
  font-size: 0.875rem;
  line-height: 1.4;
  color: #666;
}

.card {
  transition: transform 0.3s ease;
  background-color: white;
}

.card:hover {
  transform: translateY(-5px);
}

.modal-footer {
  padding: 1rem;
}

/* 스크롤바 스타일링 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}
</style>