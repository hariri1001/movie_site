<template>
  <div class="fixed-chat">
    <button 
      @click="showModal = !showModal"
      class="chat-button"
    >
      <span class="chat-button-text">💬</span>
    </button>

    <div 
      class="modal fade" 
      id="chatModal" 
      tabindex="-1"
      :class="{ 'show': showModal }"
      :style="{ display: showModal ? 'block' : 'none' }"
    >
      <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content custom-modal">
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

          <div class="modal-body">
            <MovieRecommender />
          </div>
        </div>
      </div>
    </div>

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
  max-width: 600px !important;
  height: 90vh !important;
  margin: 1.75rem auto !important;
}

.custom-modal {
  border-radius: 1.5rem !important;
  background-color: #141414 !important;
  height: 85vh !important;
  max-height: 85vh !important;
}

.modal-header {
  background-color: #000000;
  padding: 1rem 1.5rem;
}

.modal-body {
  background-color: #1a1a1a;
  padding: 0 !important;
  height: calc(100% - 70px) !important; /* 헤더 높이 제외 */
  overflow-y: auto !important;
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

/* 스크롤바 스타일링 */
.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: #1a1a1a;
}

.modal-body::-webkit-scrollbar-thumb {
  background: #ead200;
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: #cbb700;
}

/* MovieRecommender 컴포넌트 스타일 오버라이드 */
:deep(.movie-recommender) {
  height: 100%;
  background-color: #000000;
}

/* 모달 오버레이 스타일링 */
.modal-backdrop {
  background-color: rgba(0, 0, 0, 0.7) !important;
}
</style>