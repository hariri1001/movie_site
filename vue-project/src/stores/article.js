// stores/article.js
export const useArticleStore = defineStore('article', {
    state: () => ({
      articles: [],
    }),
    actions: {
      async getArticles() {
        try {
          const response = await axios.get(`${API_URL}/api/v1/articles/list/`, {
            headers: { Authorization: `Token ${token.value}` }
          });
          this.articles = response.data;
        } catch (error) {
          console.error('게시글 목록 가져오기 실패:', error);
        }
      }
    }
  });
  