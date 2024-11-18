<!-- ProfileView.vue -->
<template>
  <div class="profile-container" v-if="profile">
    <div class="user-info">
      <h2>{{ profile.user?.username }}</h2>
      <p>Email: {{ profile.user?.email }}</p>
      
      <!-- <div class="stats">
        <div>팔로워: {{ profile.followers_count }}</div>
        <div>팔로잉: {{ profile.following_count }}</div>
      </div>
      
      <div class="password-change">
        <input v-model="oldPassword" type="password" placeholder="현재 비밀번호">
        <input v-model="newPassword" type="password" placeholder="새 비밀번호">
        <button @click="changePassword">비밀번호 변경</button>
      </div> -->
    </div>
    
    <div class="liked-movies" v-if="likedMovies.length">
      <h3>좋아요한 영화</h3>
      <div class="movie-grid">
        <div v-for="movie in likedMovies" :key="movie.id" class="movie-card">
          <h4>{{ movie.title }}</h4>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      profile: null,
      likedMovies: [],
      oldPassword: '',
      newPassword: ''
    }
  },
  
  async created() {
    await this.fetchProfile();
  },
  
  methods: {
    async fetchProfile() {
      try {
        const response = await axios.get('/api/v1/accounts/profile/');
        this.profile = response.data.profile;
        this.likedMovies = response.data.liked_movies;
      } catch (error) {
        console.error('프로필 로딩 실패:', error);
      }
    },
    
    // async changePassword() {
    //   try {
    //     await axios.post('/api/v1/accounts/profile/password/', {
    //       old_password: this.oldPassword,
    //       new_password: this.newPassword
    //     });
    //     alert('비밀번호가 변경되었습니다.');
    //     this.oldPassword = '';
    //     this.newPassword = '';
    //   } catch (error) {
    //     alert(error.response?.data?.error || '비밀번호 변경 실패');
    //   }
    // }
  }
}
</script>