<template>
  <div class="fixed-chat">
    <!-- 챗봇 버튼 -->
    <button 
      @click="showModal = !showModal"
      class="chat-button"
    >
      <span class="chat-button-text">💬</span>
    </button>

    <!-- 부트스트랩 모달 -->
    <div 
      class="modal fade" 
      id="chatModal" 
      tabindex="-1"
      :class="{ 'show': showModal }"
      :style="{ display: showModal ? 'block' : 'none' }"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content" style="background-color: rgb(247, 218, 125);">
          <!-- 모달 헤더 -->
          <div class="modal-header border-0">
            <div class="header-logo d-flex align-items-center gap-2">
              <div class="logo-icon">
                <span class="logo-icon-text">🎬</span>
              </div>
              <h5 class="modal-title">영화 추천을 도와드립니다.</h5>
            </div>
            <button 
              type="button" 
              class="btn-close" 
              @click="showModal = false"
            ></button>
          </div>

          <!-- 모달 바디 -->
          <div class="modal-body p-0">
            <MovieRecommender />
          </div>
        </div>
      </div>
    </div>

    <!-- 배경 오버레이 -->
    <div 
      v-if="showModal" 
      class="modal-backdrop fade show"
      @click="showModal = false"
    ></div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import MovieRecommender from '@/components/movies/MovieRecommender.vue'

const showModal = ref(false)
</script>

<style scoped>
.fixed-chat {
  background-color: #000000;
}

.chat-button {
  position: fixed;
  bottom: 6rem;
  right: 6rem;
  width: 3rem;
  height: 3rem;
  background-color: #ead200;
  border-radius: 50%;
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease;
  z-index: 1040;
}

.chat-button:hover {
  background-color: #5a5a5a;
}

.chat-button-text {
  color: white;
  font-size: 1.25rem;
}

/* 모달 커스터마이징 */
.modal-dialog {
  max-width: 800px;
  margin: 1.75rem auto;
}

.modal-content {
  border-radius: 1.5rem;
  overflow: hidden;
  background-color: #141414;
}

.modal-header {
  background-color: #000000;
  padding: 1rem 1.5rem;
}

.logo-icon {
  width: 2rem;
  height: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.25rem;
}

.modal-title {
  margin: 0;
  font-weight: 600;
  color: #F8F9FA;

}

.btn-close {
  filter: invert(1);
  opacity: 0.8;
}

.btn-close:hover {
  opacity: 1;
}

.modal-body {
  background-color: #1a1a1a;
  min-height: 400px;
}

/* 모달이 표시될 때 스크롤바 방지 */
:deep(body.modal-open) {
  overflow: hidden;
}

/* MovieRecommender 컴포넌트 스타일 오버라이드 */
:deep(.movie-recommender) {
  height: 100%;
  background-color: #000000;
}
</style>