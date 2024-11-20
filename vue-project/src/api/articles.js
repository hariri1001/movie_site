import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/v1/articles/';

export default {
  getArticles() {
    return axios.get(API_URL);
  },
  getArticle(id) {
    return axios.get(`${API_URL}${id}/`);
  },
  createArticle(data, token) {
    return axios.post(API_URL, data, {
      headers: { Authorization: `Token ${token}` },
    });
  },
};
