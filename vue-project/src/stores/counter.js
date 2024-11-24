import { ref, computed, watch } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore("counter", () => {
  const articles = ref([]); // 전체 게시글 목록
  const currentArticle = ref(null); // 현재 상세 보기 중인 게시글
  const API_URL = "http://127.0.0.1:8000";
  const token = ref(sessionStorage.getItem('userToken') || null);
  const router = useRouter();


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
    const response = await axios.post(
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
 
    // 새 게시글을 articles 배열에 추가
    articles.value.unshift(response.data);
    // 또는 전체 목록 새로고침
    // await getArticles(); 
    
    router.push({ name: 'ArticleView' });
  } catch (error) {
    console.error('게시글 작성 실패:', error.response?.data || error);
    alert('게시글 작성에 실패했습니다.');
  }
 };
 
 // 게시글 목록 가져오기 
 const getArticles = async () => {
  try {
    console.log('게시글 목록 요청 시작');
    const response = await axios.get(
      `${API_URL}/api/v1/articles/list/`,
      {
        headers: { Authorization: `Token ${token.value}` }
      }
    );
    console.log('받은 응답:', response.data);
    articles.value = response.data;
  } catch (error) {
    console.error('게시글 목록 가져오기 실패:', error.response?.data || error);
  }
 };




  //** 유저 기능 **
  // 회원가입 메서드
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

  // 토큰 변경 감지 및 저장
  watch(() => token.value, (newToken) => {
    if (newToken) {
      sessionStorage.setItem('userToken', newToken);
    } else {
      sessionStorage.removeItem('userToken');
    }
  });

  // 페이지 로드 시 토큰 확인
  const checkAuth = async () => {
    const storedToken = sessionStorage.getItem('userToken');
    if (storedToken) {
      token.value = storedToken;
      try {
        await getProfile();
      } catch (error) {
        clearAllData();
      }
    }
  };


  const isLogin = computed(() => !!token.value);
  // 로그인 메서드
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
      sessionStorage.setItem('userToken', response.data.key);
      await getProfile();
      router.push({ name: "MainView" });
    } catch (error) {
      console.error("로그인 실패:", error);

      // 에러 응답 상태 코드에 따른 메시지 표시
      if (error.response) {
        if (error.response.status === 400) {
          alert("아이디 또는 비밀번호가 올바르지 않습니다.");
        } else if (error.response.status === 404) {
          alert("등록되지 않은 사용자입니다.");
        } else {
          alert("로그인 중 오류가 발생했습니다. 다시 시도해주세요.");
        }
      } else {
        alert("서버와 통신 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
      }


    }
  };

  const clearAllData = () => {
    token.value = null;
    sessionStorage.removeItem('userToken');
    userProfile.value = null;
  };


  // 로그아웃 메서드
  const logOut = function () {
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



  if (typeof window !== 'undefined') {
    // 페이지 닫힐 때
    window.addEventListener('beforeunload', () => {
      if (!document.hidden) {  // 새로고침이 아닌 경우만
        localStorage.removeItem('userToken');
      }
    });
  }


  // **프로필 관련 메서드**
  const userProfile = ref(null);
 // 프로필 조회(생성)
  const getProfile = async () => {
    try {
      const response = await axios({
        method: "get",
        url: `${API_URL}/api/v1/accounts/profile/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      console.log(response.data);
      userProfile.value = response.data; // 사용자 프로필 데이터 저장
    } catch (error) {
      console.error("프로필 조회 실패:", error);
    }
  };

  // 프로필 수정
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

  // 회원탈퇴
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

  // **게시글 수정/삭제/토글 메서드 **
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
      const { liked, likes_count } = response.data;
  
      // articles 배열에서 해당 게시글 상태 업데이트
      const targetArticle = articles.value.find((article) => article.id === articleId);
      if (targetArticle) {
        targetArticle.isLiked = liked;
        targetArticle.likes_count = likes_count;
      }
  
      return { liked, likes_count };
    } catch (error) {
      console.error("좋아요 API 호출 실패:", error);
      throw error;
    }
  };

  const getUserProfile = async (username) => {
    try {
      const response = await axios.get(
        `${API_URL}/api/v1/accounts/profile/${username}/`,
        {
          headers: { Authorization: `Token ${token.value}` },
        }
      );
      return response.data;
    } catch (error) {
      console.error('프로필 조회 실패:', error);
      throw error;
    }
  };



const getUserArticles = async (username) => {
  try {
    const response = await axios.get(
      `${API_URL}/api/v1/articles/user/`,  // 기존 URL 사용
      {
        headers: { Authorization: `Token ${token.value}` },
        params: { username }  // 쿼리 파라미터로 username 전달
      }
    );
    return response.data;
  } catch (error) {
    console.error('사용자 게시글 조회 실패:', error);
    throw error;
  }
};



// 특정 사용자가 좋아요한 영화 목록 가져오기
const getUserLikedMovies = async (username) => {
  try {
    const response = await axios.get(
      `${API_URL}/movies/liked-movies/`,  // 기존 API 사용
      {
        headers: { Authorization: `Token ${token.value}` },
      }
    );
    return response.data;
  } catch (error) {
    console.error('좋아요한 영화 조회 실패:', error);
    throw error;
  }
};

// 팔로우/언팔로우 토글
const toggleFollow = async (username) => {
  try {
    const response = await axios.post(
      `${API_URL}/api/v1/accounts/follow/${username}/`,
      {},
      {
        headers: { Authorization: `Token ${token.value}` },
      }
    );
    return response.data;
  } catch (error) {
    console.error('팔로우 처리 실패:', error);
    throw error;
  }
};


const createComment = async (payload) => {
  try {
    const response = await axios.post(
      `${API_URL}/api/v1/articles/${payload.article_id}/comments/`,
      { content: payload.content },
      {
        headers: { Authorization: `Token ${token.value}` },
      }
    );
    return response.data;
  } catch (error) {
    console.error('댓글 작성 실패:', error);
    throw error;
  }
};

const getComments = async (articleId) => {
  try {
    const response = await axios.get(
      `${API_URL}/api/v1/articles/${articleId}/comments/`,
      {
        headers: { Authorization: `Token ${token.value}` },
      }
    );
    return response.data;
  } catch (error) {
    console.error('댓글 조회 실패:', error);
    throw error;
  }
};

const deleteComment = async (commentId) => {
  try {
    await axios.delete(
      `${API_URL}/api/v1/comments/${commentId}/`,
      {
        headers: { Authorization: `Token ${token.value}` },
      }
    );
  } catch (error) {
    console.error('댓글 삭제 실패:', error);
    throw error;
  }
};






  
  return {
    articles,
    currentArticle,
    API_URL,
    token,
    isLogin,

    // 게시글
    getArticles,
    getArticleById,
    createArticle,
    deleteArticle,
    updateArticle,

    // 회원가입, 로그인/로그아웃
    signUp,
    logIn,
    logOut,

    //프로필
    userProfile,
    updateProfile,
    getProfile,
    clearAllData,
    deleteAccount,
 
    toggleArticleLike,
    checkAuth,
    // 팔로잉, 팔로우 기능
    getUserProfile,
    getUserArticles,
    getUserLikedMovies,
    toggleFollow,

    createComment,
    getComments,
    deleteComment,
  };
});
