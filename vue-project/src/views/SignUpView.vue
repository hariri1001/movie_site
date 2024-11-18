<template>
  <div class="signup-container">
    <h1>Sign Up Page</h1>
    <form @submit.prevent="signUp" class="signup-form">
      <div class="form-group">
        <label for="firstName">name : </label>
        <input type="text" id="firstName" v-model.trim="firstName">
      </div>
      
      <div class="form-group">
        <label for="username">userID : </label>
        <input type="text" id="username" v-model.trim="username">
      </div>

      <div class="form-group">
        <label for="password1">Password : </label>
        <input type="password" id="password1" v-model.trim="password1">
      </div>
      

      <div class="form-group">
        <label for="password2">Password confirmation : </label>
        <input type="password" id="password2" v-model.trim="password2">
      </div>
      

      <div class="form-group">
        <label for="email">email : </label>
        <div>
          <input type="text" id="email" v-model.trim="email" placeholder="이메일">
          <span class="at">@</span>
          <select v-model="emailDomain" class="email-domain">
            <option value="gmail.com">gmail.com</option>
            <option value="naver.com">naver.com</option>
          </select>
        </div>
      </div>
      <input type="submit" value="SignUp" class="signup-button">
    </form>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { ref, computed } from 'vue'

const firstName = ref(null)
const username = ref(null)
const password1 = ref(null)
const password2  = ref(null)
const email  = ref(null)
const emailDomain  = ref(null)

const store = useCounterStore()


const signUp = function () {
  // 필수 입력값 확인
  if ( !firstName.value || !firstName.value || !password1.value || !password2.value) {
    alert('모든 필드를 입력해주세요.')
    return
  }

  // 비밀번호 일치 여부 확인
  if (password1.value !== password2.value) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  const payload = {
    firstName: firstName.value,
    username: username.value,
    password1: password1.value,
    password2 : password2 .value,
    Email: Email.value,
  }
  store.signUp(payload)
}

// 전체 이메일 주소 계산
const Email = computed(() => {
  if (email.value && emailDomain.value) {
    return `${email.value}@${emailDomain.value}`
  }
  return ''
})

</script>

<style>
.signup-container {
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

.signup-form {
 display: flex;
 flex-direction: column;
 gap: 24px;  /* 입력 필드 사이 간격 */
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

input, select {
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

input:focus, select:focus {
 outline: none;
 border-color: #00b318;
 background-color: #404040;
}

.email-input-group {
 display: flex;
 align-items: center;
 gap: 8px;
}

.email-input-group input {
 flex: 1;
}

.email-input-group select {
 width: 130px;
}

.at {
 color: white;
 font-size: 16px;
}

.signup-button {
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

.signup-button:hover {
 background-color: #00b318;
}

/* 선택 옵션 스타일링 */
select option {
 background-color: #333;
 color: white;
}
</style>
