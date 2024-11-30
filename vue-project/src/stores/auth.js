import { ref, computed, watch } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";
import { useProfileStore } from './profile';


export const useAuthStore = defineStore("auth", () => {
  const API_URL = "http://127.0.0.1:8000";
  const token = ref(sessionStorage.getItem('userToken') || null);
  const router = useRouter();
  
  const isLogin = computed(() => !!token.value);

  watch(() => token.value, (newToken) => {
    if (newToken) {
      sessionStorage.setItem('userToken', newToken);
    } else {
      sessionStorage.removeItem('userToken');
    }
  });

  const signUp = async (payload) => {
    try {
      const signupResponse = await axios({
        method: "post",
        url: `${API_URL}/api/v1/accounts/signup/`,
        data: {
          username: payload.username,
          first_name: payload.firstName,
          password1: payload.password1,
          password2: payload.password2,
          email: payload.Email,
        },
      });
      console.log("회원가입 성공:", signupResponse.data);
      await logIn({
        username: payload.username,
        password: payload.password1,
      });
    } catch (error) {
      console.error("회원가입 실패:", error.response?.data);
      alert("회원가입에 실패했습니다.");
    }
  };

  const logIn = async (payload) => {
    try {
      const response = await axios({
        method: "post",
        url: `${API_URL}/api/v1/auth/login/`,
        data: {
          username: payload.username,
          password: payload.password,
        },
      });
      token.value = response.data.key;
      sessionStorage.setItem('userToken', response.data.key);

      // 프로필 정보 가져오기
      const profileStore = useProfileStore();
      await profileStore.getProfile();

      router.push({ name: "MainView" });
    } catch (error) {
      console.error("로그인 실패:", error);
      if (error.response) {
        if (error.response.status === 400) {
          alert("아이디 또는 비밀번호가 올바르지 않습니다.");
        } else if (error.response.status === 404) {
          alert("등록되지 않은 사용자입니다.");
        } else {
          alert("로그인 중 오류가 발생했습니다. 다시 시도해주세요.");
        }
      } else {
        alert("서버와 통신 중 오류가 발생했습니다.");
      }
    }
  };

  const checkAuth = async () => {
    const storedToken = sessionStorage.getItem('userToken');
    if (storedToken) {
      token.value = storedToken;
    }
  };


  const logOut = () => {
    if (!token.value) {
      clearAllData();
      router.push({ name: "MainView" });
      return;
    }

    axios({
      method: "post",
      url: `${API_URL}/api/v1/auth/logout/`,
      headers: {
        Authorization: `Token ${token.value}`,
      },
    })
      .then(() => {
        clearAllData();
        router.push({ name: "MainView" }, { replace: true });
      })
      .catch((err) => {
        console.error("로그아웃 실패:", err);
        clearAllData();
        router.push({ name: "MainView" }, { replace: true });
      });
  };

  const clearAllData = () => {
    token.value = null;
    sessionStorage.removeItem('userToken');
  };

  

  return {
    token,
    isLogin,
    signUp,
    logIn,
    logOut,
    checkAuth,
    clearAllData,
    API_URL
  };
});