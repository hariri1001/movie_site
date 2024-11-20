<template>
    <div class="social-login">
      <button @click="kakaoLogin" class="social-btn kakao">
        <img src="@/assets/kakao.jpg" alt="카카오 로그인">
      </button>
      <!-- <button @click="googleLogin" class="social-btn google">
        <img src="@/assets/google-icon.png" alt="구글 로그인">
      </button>
      <button @click="naverLogin" class="social-btn naver">
        <img src="@/assets/naver-icon.png" alt="네이버 로그인">
      </button> -->
    </div>
</template>
  
<script setup>
  const kakaoLogin = () => {
    window.location.href = 'http://localhost:8000/accounts/social/kakao/login/'
  }
  
//   const googleLogin = () => {
//     window.location.href = '/accounts/google/login/'
//   }
  
//   const naverLogin = () => {
//     window.location.href = '/accounts/naver/login/'
//   }
</script>
  
<style scoped>
  .social-login {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin: 20px 0;
  }
  
  .social-btn {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    padding: 0;
    overflow: hidden;
  }
  
  .social-btn img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .kakao {
    background: #FEE500;
  }
  
  /* .google {
    background: white;
    border: 1px solid #ddd;
  }
  
  .naver {
    background: #03C75A;
  } */
</style>