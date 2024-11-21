<template>
  <div>
    <!-- 왼쪽 상단 고정 아이콘 (스크롤에 따라 이동) -->
    <button 
      @click="isOpen = !isOpen"
      class="fixed top-4 left-4 p-2 text-gray-600 hover:text-gray-800 transition-all duration-300 z-50"
      :style="{ top: `${buttonTop}px` }"
    >
      <span class="text-xl">💬</span>
    </button>
 
    <!-- 모달 오버레이 -->
    <div 
      v-if="isOpen"
      class="fixed inset-0 bg-black bg-opacity-50 z-40"
      @click="isOpen = false"
    ></div>
 
    <!-- 챗봇 모달 -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 translate-y-4"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-4"
    >
      <div 
        v-if="isOpen"
        class="fixed z-50 top-20 left-4 w-96 max-h-[600px] bg-white rounded-lg shadow-xl overflow-hidden"
        :style="{ top: `${modalTop}px` }"
      >
        <div class="flex justify-between items-center p-4 border-b">
          <h3 class="font-semibold">영화 추천 봇</h3>
          <button @click="isOpen = false" class="text-gray-500 hover:text-gray-700">✖</button>
        </div>
        <div class="p-4">
          <MovieRecommender />
        </div>
      </div>
    </Transition>
  </div>
 </template>
 
 <script setup>
 import { ref, onMounted, onUnmounted } from 'vue'
 import MovieRecommender from '@/components/movies/MovieRecommender.vue'
 
 const isOpen = ref(false)
 const buttonTop = ref(16)
 const modalTop = ref(80)
 
 const handleScroll = () => {
  const scrollY = window.scrollY
  buttonTop.value = Math.max(16, scrollY + 16)
  modalTop.value = Math.max(80, scrollY + 80)
 }
 
 onMounted(() => {
  window.addEventListener('scroll', handleScroll)
 })
 
 onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
 })
 </script>