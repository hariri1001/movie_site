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
                     
                     @error="e => e.target.src = '/default-movie-poster.jpg'">
                <div class="card-body">
                  <h5 class="card-title">{{ movie.title }}
                    <p class="card-text" v-if="movie.originalTitle">
                      {{ movie.originalTitle }}
                    </p>
                  </h5>
                  <div class="d-flex flex-wrap gap-2 mb-2">
                    <span class="badge bg-primary" v-if="movie.genres">{{ movie.genres }}</span>
                    <span class="badge bg-success">평점: {{ movie.rating }}</span>
                    <span v-if="movie.tmdbRating" class="badge bg-info">
                      TMDB: {{ movie.tmdbRating.toFixed(1) }}
                    </span>
                  </div>
                  <p class="card-text small" v-if="movie.releaseDate || movie.runtime">
                    <span v-if="movie.releaseDate">
                      개봉: {{ new Date(movie.releaseDate).toLocaleDateString('ko-KR') }}
                    </span>
                    <!-- <span v-if="movie.runtime" class="ms-2">
                      {{ Math.floor(movie.runtime / 60) }}시간 {{ movie.runtime % 60 }}분
                    </span> -->
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
  background-color: #030303;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.modal-content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.question-section {
  flex: 1;
  text-align: center;
  padding: 1.5rem;
  background-color: black;
}

.question-text {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #ffffff;
}

/* 옵션 버튼 스타일링 */
.option-btn {
  width: 100%;
  padding: 15px;
  margin: 8px 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: rgb(228, 225, 225);
  background-color: rgb(39, 39, 39);
  border: none;
  border-radius: 10px;
  text-align: center;
  transition: all 0.3s ease;
}

.option-btn:hover {
  background-color: #ead200;
  color: rgb(3, 3, 3);
  transform: translateY(-2px);
}

/* 추천 결과 섹션 */
.results-section {
  background-color: rgb(3, 3, 3);
  border-radius: 15px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.results-title {
  font-size: 1.75rem;
  font-weight: 500;
  text-align: center;
  color: #dad9d9;
  margin-bottom: 2rem;
}

/* 그리드 레이아웃 수정 */
.row-cols-1.row-cols-md-2 {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
}

.col {
  width: 100%;
}

/* 카드 스타일링 */
.card {
  height: 220px !important;
  border: none;
  border-radius: 15px;
  overflow: hidden;
  transition: transform 0.3s ease;
  width: 100%;
  display: flex;
  flex-direction: row;
  background-color: #1f1f1f;
}

.card-img-top {
  width: 150px;
  height: 220px;
  object-fit: cover;
  flex-shrink: 0;
  background-color: #000;
  border-radius: 0;
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
}

.card-body {
  padding: 1rem;
  background-color: #1f1f1f;
  color: #dad9d9;
  display: flex;
  flex-direction: column;
  justify-content: start;
  flex: 1;
  overflow: visible; /* hidden에서 visible로 변경 */
}

.card-title {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  white-space: normal; /* nowrap에서 normal로 변경 */
  overflow: visible; /* hidden에서 visible로 변경 */
  text-overflow: unset; /* ellipsis 제거 */
  word-break: keep-all; /* 한글 단어 단위 줄바꿈 */
  line-height: 1.3;
}

.card-text {
  margin: 3px;
}

.badge {
  font-size: 0.75rem;
  padding: 0.35em 0.65em;
  white-space: nowrap;
  border: none;
}

/* 설명 텍스트 */
.description {
  margin-top: 0;
  font-size: 0.9rem;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

/* 카드 호버 효과 */
.card:hover {
  transform: translateY(-3px);
}

/* 모달 푸터 */
.modal-footer {
  background-color: rgb(0, 0, 0) !important;
  border: none;
  padding: 1rem;
  display: flex;
  justify-content: center;
}

.modal-footer .btn-primary {
  width: 100%;
  max-width: 800px;
  background: none;
  border: 1px solid #ead200;
  padding: 12px;
  font-size: 1.1rem;
  border-radius: 10px;
}

.modal-footer .btn-primary:hover {
  background-color: #ead200;
  color: rgb(3, 3, 3);
}

/* 로딩 스피너 */
.spinner-border {
  color: #90C88C !important;
}

/* 알림 메시지 */
.alert {
  border-radius: 10px;
}

/* 챗봇 아이콘 스타일 */
.logo-icon {
  margin-bottom: 1.5rem;
}

.logo-icon-text {
  font-size: 2rem;
}
</style>