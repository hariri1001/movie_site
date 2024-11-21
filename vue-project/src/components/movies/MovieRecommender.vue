<template>
    <div class="movie-recommender">
      <div v-if="!showResults" class="question-container">
        <h2>{{ currentQuestion.text }}</h2>
        <div class="options">
          <button
            v-for="option in currentQuestion.options"
            :key="option"
            @click="handleAnswer(option)"
            class="option-button"
          >
            {{ option }}
          </button>
        </div>
      </div>
      
      <div v-else class="results-container">
        <h2>추천 영화 목록</h2>
        <div class="movie-list">
          <div v-for="movie in recommendations" :key="movie.title" class="movie-card">
            <h3>{{ movie.title }}</h3>
            <p>{{ movie.genre }}</p>
            <p>평점: {{ movie.rating }}</p>
          </div>
        </div>
        <button @click="resetQuiz" class="reset-button">다시 시작하기</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        currentQuestionIndex: 0,
        answers: {},
        recommendations: [],
        showResults: false,
        questions: [
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
      }
    },
    computed: {
      currentQuestion() {
        return this.questions[this.currentQuestionIndex]
      }
    },
    methods: {
      async handleAnswer(answer) {
        this.answers[this.currentQuestionIndex] = answer
        
        if (this.currentQuestionIndex < this.questions.length - 1) {
          this.currentQuestionIndex++
        } else {
          await this.getRecommendations()
        }
      },
      async getRecommendations() {
        try {
          const response = await fetch('http://localhost:8000/movies/api/recommend/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.answers)
          })
          this.recommendations = await response.json()
          this.showResults = true
        } catch (error) {
          console.error('Error:', error)
        }
      },
      resetQuiz() {
        this.currentQuestionIndex = 0
        this.answers = {}
        this.recommendations = []
        this.showResults = false
      }
    }
  }
  </script>
  
  <style scoped>
  .movie-recommender {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .question-container, .results-container {
    background: rgb(175, 175, 175);
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  
  .options {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
    color: black;
  }
  
  .option-button {
    padding: 12px;
    border: 1px solid #6d6d6d;
    border-radius: 4px;
    background: rgb(104, 104, 104);
    cursor: pointer;
    transition: all 0.3s;
  }
  
  .option-button:hover {
    background: #f5f5f5;
  }
  
  .movie-list {
    display: grid;
    gap: 15px;
    margin-top: 20px;
  }
  
  .movie-card {
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .reset-button {
    margin-top: 20px;
    padding: 12px;
    width: 100%;
    background: #4a5568;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  </style>