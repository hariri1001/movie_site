<template>
  <header>
    <div class="wrapper">
      <AppNavbar/>

    </div>
  </header>

  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import AppNavbar from './components/Common/AppNavbar.vue';


</script>

<style>
/* 전역 스타일 설정 (scoped 속성 제거) */
html, 
body {
  margin: 0;
  padding: 0;
  background-color: #1a1a1a !important; /* 더 어두운 검은색으로 통일 */
  color: white;
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  background-color: #1a1a1a;
  color: white;
}

/* 모든 라우터 뷰에 대한 기본 스타일 */
.router-view-container {
  background-color: #1a1a1a;
  min-height: 100vh;
}

/* 스크롤바 스타일링 (선택사항) */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #1a1a1a;
}

::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #444;
}
</style>