<template>
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-btn" @click="closeModal">X</button>
        
        <div class="modal-body">
          <!-- 왼쪽: 포스터 -->
          <div class="poster-container">
            <img :src="posterUrl" alt="Movie Poster" class="poster" />
          </div>
  
          <!-- 오른쪽: 영화 정보 -->
          <div class="movie-info">
            <h2>{{ movie.title }}</h2>
            <p>{{ truncatedOverview }}<span v-if="isTruncated" @click="toggleOverview" class="more-link">... 더보기</span></p>
            <p><strong>개봉일:</strong> {{ movie.release_date }}</p>
            <p><strong>평점:</strong> {{ movie.vote_average }}</p>
          </div>
        </div>
      </div>
    </div>
</template>
  
<script>
  export default {
    props: {
      movie: Object, // 영화 정보
      showModal: Boolean // 모달을 보여줄지 말지 결정하는 flag
    },
    data() {
      return {
        isTruncated: true // 줄거리를 두 줄로 제한할지 여부
      };
    },
    computed: {
      posterUrl() {
        return this.movie.poster_path
          ? `https://image.tmdb.org/t/p/w500${this.movie.poster_path}`
          : "https://via.placeholder.com/200x300?text=No+Image";
      },
      truncatedOverview() {
        // 줄거리가 100자 이상이면 100자까지만 표시하고, 아닐 경우 전체를 표시
        if (this.isTruncated && this.movie.overview) {
          return this.movie.overview.length > 100 ? this.movie.overview.slice(0, 100) : this.movie.overview;
        } else {
          return this.movie.overview; // '더보기'를 클릭했을 때 전체 내용 반환
        }
      }
    },
    methods: {
      closeModal() {
        this.$emit('close'); // 모달을 닫는 이벤트를 부모에게 전달
      },
      toggleOverview() {
        this.isTruncated = !this.isTruncated; // '더보기' 클릭 시 줄거리를 전환
      }
    }
  }
</script>
  
<style scoped>
    .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    }

    .modal-content {
    background: rgba(5, 5, 5, 0.701);
    padding: 20px;
    border-radius: 10px;
    width: 80%;
    height: 70%;
    max-width: 800px; /* 화면 크기에 따라 모달 크기 조정 */
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    position: relative;
    display: flex; /* Flexbox로 레이아웃 배치 */
    flex-direction: row; /* 좌우 배치 */
    }

    .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 20px;
    color: #333;
    cursor: pointer;
    }

    .modal-body {
    display: flex;
    flex-direction: row; /* 왼쪽(포스터)와 오른쪽(정보) 배치 */
    align-items: flex-start;
    justify-content: space-between;
    width: 100%;
    }

    .poster-container {
    flex: 1; /* 포스터가 화면의 일정 비율을 차지하도록 설정 */
    padding-right: 20px; /* 포스터와 정보 사이의 간격 */
    }

    .poster {
    width: 100%; /* 포스터가 가로로 꽉 차도록 */
    height: auto;
    border-radius: 10px;
    }

    .movie-info {
    flex: 2; /* 영화 정보가 나머지 공간을 차지하도록 설정 */
    text-align: left;
    padding-left: 20px; /* 영화 정보와 포스터 사이의 간격 */
    max-width: 60%; /* 영화 정보 영역의 최대 너비 */
    }

    .movie-info p {
    margin-bottom: 10px;
    }

    .more-link {
    color: #007bff;
    cursor: pointer;
    text-decoration: underline;
    }

    h2 {
    font-size: 24px;
    margin-bottom: 10px;
    text-align: center;
    }
</style>
  