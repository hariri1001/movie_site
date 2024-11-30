import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from './auth';

export const useCommentStore = defineStore("comments", () => {
  const authStore = useAuthStore();

  const createComment = async (payload) => {
    try {
      const response = await axios.post(
        `${authStore.API_URL}/api/v1/articles/${payload.article_id}/comments/`,
        { content: payload.content },
        {
          headers: { Authorization: `Token ${authStore.token}` },
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
        `${authStore.API_URL}/api/v1/articles/${articleId}/comments/`,
        {
          headers: { Authorization: `Token ${authStore.token}` },
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
        `${authStore.API_URL}/api/v1/comments/${commentId}/`,
        {
          headers: { Authorization: `Token ${authStore.token}` },
        }
      );
      return true;
    } catch (error) {
      console.error('댓글 삭제 실패:', error);
      throw error;
    }
  };

  return {
    createComment,
    getComments,
    deleteComment
  };
});