<template>
  <div class="login-container">
    <div class="login">
      <img src="@/assets/post-relog.png" alt="Logo" height="40" class="d-inline-block align-text-top">
      <h3>로그인</h3>
    </div>
    <form @submit.prevent="logIn" class="login-form">
      <div class="form-group">
        <input type="text" id="username" v-model.trim="username" placeholder="아이디" class="input-field">
      </div>
      
      <div class="form-group">
        <input type="password" id="password" v-model.trim="password" placeholder="패스워드" class="input-field">
      </div>


      <input type="submit" value="로그인" class="login-button">
      <div class="signup-link">
        POST 회원이 아닌가요? 
        <RouterLink :to="{ name: 'SignUpView' }">지금 가입하세요.</RouterLink>
     </div>
    </form>
    <!-- <SocialLogin /> -->
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const username = ref(null)
const password = ref(null)

const authStore = useAuthStore()
const router = useRouter()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  authStore.logIn(payload)
}

</script>

<style>
.login-container {
 max-width: 400px;
 margin: 70px auto;
 padding: 40px;
 background-color: rgba(0, 0, 0, 0.75);
 border-radius: 8px;
 box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}


.input-field {
 width: 100%;
 padding: 15px;
 background: rgba(0, 0, 0, 0.5);
 border: 1px solid #333;
 border-radius: 5px;
 color: white;
 transition: all 0.3s ease;
}

.input-field:focus {
 background: rgba(255, 255, 255, 0.1);
 border: 1px solid #fff;
 box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
 outline: none;
}



.login {
  display: flex;
  flex-direction: column;  /* 세로 방향으로 배치 */
  align-items: center;     /* 가운데 정렬 */
  text-align: center;
  color: white;
  margin-bottom: 20px;
}

.login img {
  margin-bottom: 15px;    /* 이미지 아래 여백 추가 */
}

.login-form {
 display: flex;
 flex-direction: column;
 gap: 24px;
}

.form-group {
 display: flex;
 flex-direction: column;
 gap: 8px;
 margin-bottom: 15px;
}

label {
 color: #e5e5e5;
 font-size: 16px;
 font-weight: 500;
}

input {
 padding: 16px;
 background-color: #333;
 border-radius: 4px;
 color: white;
 font-size: 16px;
 transition: all 0.3s ease;
}

input::placeholder {
 color: #808080;
}

input:focus {
 outline: none;
 border-color: #ead200;
 background-color: #404040;
}

.login-button {
 margin-top: 16px;
 padding: 16px;
 background-color:  #ead200;
 color: white;
 border: none;
 border-radius: 4px;
 font-size: 16px;
 font-weight: 600;
 cursor: pointer;
 transition: background-color 0.3s ease;
}

.login-button:hover {
 background-color:  #dcc703eb;
}

.signup-link {
 text-align: center;
 color: #808080;
 font-size: 14px;
}

.signup-link a {
 color: #dcc703eb;
 text-decoration: none;
 margin-left: 8px;
}

.signup-link a:hover {
 text-decoration: underline;
}
</style>
