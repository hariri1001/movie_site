<template>
  <div class="login-container">
    <div class="login">
      <h1>로그인</h1>
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
    <SocialLogin />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'
import SocialLogin from '@/components/Auth/SocialLogIn.vue'

const username = ref(null)
const password = ref(null)

const store = useCounterStore()
const router = useRouter()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}

</script>

<style>

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

.login-container {
 max-width: 460px;
 margin: 50px auto;
 padding: 40px;
 background-color: rgba(0, 0, 0, 0.75);
 border-radius: 8px;
 box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}

.login {
 text-align: left;
 color: white;
 margin-bottom: 40px;
 font-size: 28px;
 font-weight: 800;
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
 border: 1px solid #008612;
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
 border-color: #00ba19;
 background-color: #404040;
}

.login-button {
 margin-top: 16px;
 padding: 16px;
 background-color: #008612;
 color: white;
 border: none;
 border-radius: 4px;
 font-size: 16px;
 font-weight: 600;
 cursor: pointer;
 transition: background-color 0.3s ease;
}

.login-button:hover {
 background-color: #00b318;
}

.signup-link {
 text-align: center;
 color: #808080;
 font-size: 14px;
}

.signup-link a {
 color: #00b318;
 text-decoration: none;
 margin-left: 8px;
}

.signup-link a:hover {
 text-decoration: underline;
}
</style>
