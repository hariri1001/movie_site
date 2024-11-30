import { ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from './auth';
import { api } from '@/api';

export const useProfileStore = defineStore("profile", () => {
  const authStore = useAuthStore();
  const userProfile = ref(null);

  const getProfile = async () => {
    try {
      const response = await axios({
        method: "get",
        url: `${authStore.API_URL}/api/v1/accounts/profile/`,
        headers: {
          Authorization: `Token ${authStore.token}`,
        },
      });
      userProfile.value = response.data;
    } catch (error) {
      console.error("프로필 조회 실패:", error);
    }
  };

  const updateProfile = async (profileData) => {
    try {
      const response = await axios({
        method: "put",
        url: `${authStore.API_URL}/api/v1/accounts/profile/update/`,
        headers: {
          Authorization: `Token ${authStore.token}`,
        },
        data: {
          first_name: profileData.first_name,
          email: profileData.email,
          password: profileData.newPassword,
        },
      });
      userProfile.value = response.data;
      return true;
    } catch (error) {
      console.error("프로필 업데이트 실패:", error);
      return false;
    }
  };

  const updateProfileImage = async (imageFile) => {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const response = await axios.post(
        `${authStore.API_URL}/api/v1/accounts/profile/image/`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Token ${authStore.token}`,
          },
        }
      );

      if (response.data) {
        userProfile.value = {
          ...response.data,
          profile_image: response.data.profile_image
        };
        return true;
      }
      return false;
    } catch (error) {
      console.error('프로필 이미지 업로드 실패:', error.response?.data);
      return false;
    }
  };

  const getUserProfile = async (username) => {
    try {
      const response = await axios.get(
        `${authStore.API_URL}/api/v1/accounts/profile/${username}/`,
        {
          headers: { Authorization: `Token ${authStore.token}` },
        }
      );
      return response.data;
    } catch (error) {
      console.error('프로필 조회 실패:', error);
      throw error;
    }
  };

  const toggleFollow = async (username) => {
    try {
      const response = await axios.post(
        `${authStore.API_URL}/api/v1/accounts/follow/${username}/`,
        {},
        {
          headers: { Authorization: `Token ${authStore.token}` },
        }
      );
      return response.data;
    } catch (error) {
      console.error('팔로우 처리 실패:', error);
      throw error;
    }
  };

  const deleteAccount = async () => {
    try {
      await axios({
        method: "delete",
        url: `${authStore.API_URL}/api/v1/accounts/delete/`,
        headers: {
          Authorization: `Token ${authStore.token}`,
        },
      });
      return true;
    } catch (error) {
      console.error("회원탈퇴 실패:", error);
      return false;
    }
  };

  const getUserArticles = async (username) => {
    try {
      const response = await api.get('/api/v1/articles/user/', {
        params: { username }
      });
      return response.data;
    } catch (error) {
      console.error('사용자 게시글 조회 실패:', error);
      throw error;
    }
  };



  return {
    userProfile,
    getProfile,
    updateProfile,
    updateProfileImage,
    getUserProfile,
    toggleFollow,
    deleteAccount,
    getUserArticles,
  };
});