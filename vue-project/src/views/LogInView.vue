<template>
  <div class="login-container">
    <h1>LogIn Page</h1>
    <form @submit.prevent="logIn" class="login-form">
      <div class="form-group">
        <label for="username">username : </label>
        <input type="text" id="username" v-model.trim="username">
      </div>
      
      <div class="form-group">
        <label for="password">password : </label>
        <input type="password" id="password" v-model.trim="password">
      </div>


      <input type="submit" value="logIn" class="login-button">
      <div class="signup-link">
        계정이 없으신가요? 
        <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink>
     </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

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
.login-container {
 max-width: 460px;
 margin: 50px auto;
 padding: 40px;
 background-color: #1a1a1a;
 border-radius: 8px;
 box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
}

h1 {
 text-align: center;
 color: white;
 margin-bottom: 40px;
 font-size: 28px;
 font-weight: 600;
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
 border-color: #00b318;
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
