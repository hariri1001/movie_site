<template>
  <div class="signup-page" >
    <div class="signup-container">
      <div class="signup">
        <h1>회원 가입</h1>
      </div>
      
      <form @submit.prevent="signUp" class="signup-form">
        <div class="form-group">
          <input type="text" id="firstName" v-model.trim="firstName" placeholder="이름">
        </div>
        
        <div class="form-group">
          <input type="text" id="username" v-model.trim="username" placeholder="아이디">
        </div>

        <div class="form-group">
          <input type="password" id="password1" v-model.trim="password1" placeholder="패스워드">
        </div>
        

        <div class="form-group">
          <input type="password" id="password2" v-model.trim="password2" placeholder="패스워드 확인">
        </div>
        

        <div class="form-group">
          <div class="email-container">
            <input type="text" id="email" v-model.trim="email" placeholder="이메일" class="email-input">
            <span class="at">@</span>
            <select v-model="emailDomain" class="email-domain">
              <option value="선택">선택</option>
              <option value="gmail.com">gmail.com</option>
              <option value="naver.com">naver.com</option>
            </select>
          </div>
        </div>
        <input type="submit" value="SignUp" class="signup-button">
      </form>
    </div>
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
const emailDomain  = ref('선택')

const store = useCounterStore()


const signUp = function () {
  // 필수 입력값 확인
  if (!firstName.value || !username.value || !password1.value || !password2.value) {
    alert('모든 필드를 입력해주세요.');
    return;
  }

  // 비밀번호 일치 여부 확인
  if (password1.value !== password2.value) {
    alert('비밀번호가 일치하지 않습니다.');
    return;
  }

  const payload = {
    firstName: firstName.value,
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    Email: Email.value,
  };
  console.log('전송할 데이터:', payload);
  store.signUp(payload);
};

// 전체 이메일 주소 계산
const Email = computed(() => {
  if (email.value && emailDomain.value) {
    return `${email.value}@${emailDomain.value}`
  }
  return ''
})

</script>

<style>

/* 전체 화면 배경 설정을 위한 스타일 */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

/* .signup-page {
 
  background-image: 
    linear-gradient(
      rgba(0, 0, 0, 0.4),
      rgba(0, 0, 0, 0.4)
    ),
    url('@/assets/signupimg.jpeg');
  background-size: cover;
  background-position: center; 
  background-repeat: no-repeat;
  background-attachment: fixed;
   
}*/

.signup-container {
  max-width: 460px;
  margin: 100px auto;
  padding: 40px;
  background-color: rgba(0, 0, 0, 0.75); /* 배경색에 투명도 추가 */
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
}


.signup {
 text-align: left;
 color: white;
 margin-bottom: 40px;
 font-size: 28px;
 font-weight: 700;
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


.email-container {
 display: flex;
 align-items: center;
 gap: 10px; /* 요소들 사이 간격 */
 width: 100%;
}

.email-input {
 width: 40%; /* 이메일 입력창 너비 */
 padding: 10px;
 background: rgba(0, 0, 0, 0.5);
 border: 1px solid #333;
 border-radius: 5px;
 color: white;
}

.at {
 color: white;
 font-size: 16px;
}

.email-domain {
 width: 60%; /* select 박스 너비 */
 padding: 15px;
 background: rgba(0, 0, 0, 0.5);
 border: 1px solid #333;
 border-radius: 5px;
 color: white;
}

/* focus 스타일 */
.email-input:focus, .email-domain:focus {
 background: rgba(255, 255, 255, 0.1);
 border: 1px solid #fff;
 box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
 outline: none;
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
