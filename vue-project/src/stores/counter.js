import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore("counter", () => {
  const articles = ref([]); // 전체 게시글 목록
  const currentArticle = ref(null); // 현재 상세 보기 중인 게시글
  const API_URL = "http://127.0.0.1:8000";
  const token = ref(null);
  const router = useRouter();

  const isLogin = computed(() => !!token.value);

  // **게시글 관련 메서드**
  const getArticles = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/articles/`, {
        headers: { Authorization: `Token ${token.value}` },
      });
      articles.value = response.data;
    } catch (error) {
      console.error('게시글 목록 불러오기 실패:', error.response?.data || error);
    }
  };

  const getArticleById = async (articleId) => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/articles/${articleId}/`, {
        headers: { Authorization: `Token ${token.value}` },
      });
      currentArticle.value = response.data;
    } catch (error) {
      console.error('게시글 상세 불러오기 실패:', error.response?.data || error);
    }
  };


  // 새 게시글 작성
  const createArticle = async (payload) => {
    try {
      await axios.post(
        `${API_URL}/api/v1/articles/`,
        {
          title: payload.title,
          content: payload.content,
          rating: payload.rating,
        },
        {
          headers: { Authorization: `Token ${token.value}` },
        }
      );
      await getArticles();
      router.push({ name: 'ArticleView' });
    } catch (error) {
      console.error('게시글 작성 실패:', error.response?.data || error);
      alert('게시글 작성에 실패했습니다.');
    }
  };

  // **인증 관련 메서드**
  const signUp = async function (payload) {
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

  const logIn = async function (payload) {
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
      console.log("로그인 성공:", token.value);
      router.push({ name: "MainView" });
    } catch (error) {
      console.error("로그인 실패:", error);
      alert("로그인에 실패했습니다.");
    }
  };

  const logOut = function () {
    if (!token.value) {
      clearAllData();
      router.push({ name: "ArticleView" });
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
        router.push({ name: "ArticleView" });
      })
      .catch((err) => {
        console.error("로그아웃 실패:", err);
        clearAllData();
        router.push({ name: "ArticleView" });
      });
  };

  const clearAllData = () => {
    token.value = null;
    localStorage.clear();
    document.cookie.split(";").forEach((c) => {
      document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
    });
  };

  // **프로필 관련 메서드**
  const userProfile = ref(null);

  const getProfile = async () => {
    try {
      const response = await axios({
        method: "get",
        url: `${API_URL}/api/v1/accounts/profile/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      userProfile.value = response.data; // 사용자 프로필 데이터 저장
    } catch (error) {
      console.error("프로필 조회 실패:", error);
    }
  };

  const updateProfile = async (profileData) => {
    try {
      const response = await axios({
        method: "put",
        url: `${API_URL}/api/v1/accounts/profile/update/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
        data: {
          first_name: profileData.first_name,
          email: profileData.email,
        },
      });
      userProfile.value = response.data;
      return true;
    } catch (error) {
      console.error("프로필 업데이트 실패:", error);
      return false;
    }
  };

  const deleteAccount = async () => {
    try {
      await axios({
        method: "delete",
        url: `${API_URL}/api/v1/accounts/delete/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      clearAllData();
      router.push({ name: "LogInView" });
      return true;
    } catch (error) {
      console.error("회원탈퇴 실패:", error);
      return false;
    }
  };
  const deleteArticle = async function (articleId) {
    try {
      await axios.delete(`${API_URL}/api/v1/articles/${articleId}/`, {
        headers: {
          Authorization: `Token ${token.value}`, // 인증 토큰
        },
      });
      // 게시글 목록 새로고침
      await getArticles();
    } catch (error) {
      console.error("게시글 삭제 실패:", error);
      alert("게시글 삭제에 실패했습니다.");
    }
  };

  const updateArticle = async (articleId, payload) => {
    try {
      await axios.put(
        `${API_URL}/api/v1/articles/${articleId}/`,
        {
          title: payload.title,
          content: payload.content,
          rating: payload.rating,
        },
        {
          headers: { Authorization: `Token ${token.value}` },
        }
      );
      await getArticles();
      alert('게시글 수정 성공!');
    } catch (error) {
      console.error('게시글 수정 실패:', error.response?.data || error);
      alert('게시글 수정에 실패했습니다.');
    }
  };

  const toggleArticleLike = async (articleId) => {
    try {
      const response = await axios.post(
        `${API_URL}/api/v1/articles/${articleId}/like/`,
        {},
        {
          headers: { Authorization: `Token ${token.value}` },
        }
      );
      return {
        liked: response.data.liked,
        likesCount: response.data.likes_count,
      };
    } catch (error) {
      console.error("좋아요 API 호출 실패:", error);
      throw error;
    }
  };
  
  return {
    articles,
    currentArticle,
    API_URL,
    token,
    isLogin,
    getArticles,
    getArticleById,
    createArticle,
    deleteArticle,
    updateArticle,
    signUp,
    logIn,
    logOut,
    userProfile,
    updateProfile,
    getProfile,
    clearAllData,
    deleteAccount,
    // 수정본
    userProfile,
    getProfile,
    toggleArticleLike,
  };
});
