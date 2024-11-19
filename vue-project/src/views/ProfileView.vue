<!-- ProfileView.vue -->
<template>
  <div class="profile-container">
    <h1>Profile Page</h1>
    
    <div v-if="!isEditing" class="profile-info">
      <p><strong>안녕하세요</strong> {{ store.userProfile?.first_name }}님!</p>
      <p><strong>아이디:</strong> {{ store.userProfile?.username }}</p>
      <p><strong>이메일:</strong> {{ store.userProfile?.email }}</p>
      
      <button @click="startEditing" class="edit-button">
        프로필 수정
      </button>
    </div>

    <form v-else @submit.prevent="submitUpdate" class="profile-form">
      <div class="form-group">
        <label for="editFirstName">이름:</label>
        <input 
          type="text" 
          id="editFirstName" 
          v-model="editForm.first_name"
        >
      </div>
      
      <div class="form-group">
        <label for="editEmail">이메일:</label>
        <input 
          type="email" 
          id="editEmail" 
          v-model="editForm.email"
        >
      </div>

      <div class="button-group">
        <button type="submit" class="save-button">저장</button>
        <button type="button" @click="cancelEditing" class="cancel-button">
          취소
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const isEditing = ref(false)
const editForm = ref({
  first_name: '',
  email: ''
})

onMounted(() => {
  store.getProfile()
  
})

const startEditing = () => {
  editForm.value = {
    first_name: store.userProfile?.first_name || '',
    email: store.userProfile?.email || ''
  }
  isEditing.value = true
}

const cancelEditing = () => {
  isEditing.value = false
}

const submitUpdate = async () => {
  // 입력값 검증
  if (!editForm.value.email) {
    alert('이메일은 필수 입력값입니다.')
    return
  }

  // store의 updateProfile 함수 호출 시 editForm 데이터 전달
  const success = await store.updateProfile(editForm.value)
  
  if (success) {
    isEditing.value = false
    alert('프로필이 성공적으로 업데이트되었습니다.')
  } else {
    alert('프로필 업데이트에 실패했습니다.')
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 460px;
  margin: 50px auto;
  padding: 40px;
  background-color: #1a1a1a;
  border-radius: 8px;
}

.profile-info {
  color: white;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  color: white;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #4CAF50;
  border-radius: 4px;
  background-color: #333;
  color: white;
}

.button-group {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-button {
  background-color: #4CAF50;
  color: white;
}

.cancel-button {
  background-color: #f44336;
  color: white;
}
</style>