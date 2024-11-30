import { createRouter, createWebHistory } from "vue-router";
import MainView from "@/views/movies/MainView.vue";
import ArticleView from "@/views/articles/ArticleView.vue";
import DetailView from "@/views/articles/DetailView.vue";
import CreateView from "@/views/articles/CreateView.vue";
import { useAuthStore } from "@/stores/auth";


// Auth
import SignUpView from "@/views/auth/SignUpView.vue";
import LogInView from "@/views/auth/LogInView.vue";
import ProfileView from "@/views/auth/ProfileView.vue";
import UserProfileView from "@/views/auth/UserProfileView.vue";

// 영화
import SearchView from "@/views/movies/SearchView.vue";
import MovieListView from "@/views/movies/MovieListView.vue";
import MovieDetailView from "@/views/movies/MovieDetailView.vue";
import MovieRandomView from "@/views/movies/MovieRandomView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "MainView",
      component: MainView,
    },
    {
      path: "/articles",
      name: "ArticleView",
      component: ArticleView,
    },
    {
      path: "/articles/:id",
      name: "DetailView",
      component: DetailView,
    },
    {
      path: "/articles/create",
      name: "CreateView",
      component: CreateView,
    },
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "LogInView",
      component: LogInView,
    },
    {
      path: "/profile",
      name: "ProfileView",
      component: ProfileView,
    },

    // 영화
    {
      path: "/movies",
      name: "MovieList",
      component: MovieListView,
    },
    {
      path: "/:movieId",
      name: "MovieDetail",
      component: MovieDetailView,
      
    },

    {
      path: "/search", // 검색 라우트 추가
      name: "SearchView",
      component: SearchView,
    },
    {
      path: '/random',
      name: 'MovieRandom',
      component: MovieRandomView,
    },
    // 다른 사용자의 프로필
    {
      path: '/profile/:username',
      name: 'UserProfile',
      component: UserProfileView,
    }
  ],
  // 스크롤 동작 설정 추가
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 } // 항상 페이지 상단으로 스크롤
  }
});

router.beforeEach((to, from) => {
  const authStore = useAuthStore();
  // 만약 이동하는 목적지가 메인 페이지이면서
  // 현재 로그인 상태가 아니라면 로그인 페이지로 보냄
  if (to.name === "ArticleView" && !authStore.isLogin) {
    window.alert("로그인이 필요합니다.");
    return { name: "LogInView" };
  }

  // 만약 로그인 사용자가 회원가입 또는 로그인 페이지로 이동하려고 하면
  // 메인 페이지로 보냄
  if ((to.name === "SignUpView" || to.name === "LogInView") && authStore.isLogin) {
    window.alert("이미 로그인 되어있습니다.");
    return { name: "ArticleView" };
  }
});

export default router;


