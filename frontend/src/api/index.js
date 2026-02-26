import axios from 'axios';

// 创建 axios 实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  withCredentials: true // 允许携带 Cookie
});

// 认证相关接口
export const authApi = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  getCurrentUser: () => api.get('/auth/me'),
  updateUserInfo: (data) => api.put('/auth/me', data)
};

// 帖子相关接口
export const postApi = {
  create: (data) => api.post('/posts', data),
  getList: (params) => api.get('/posts', { params }),
  getDetail: (id) => api.get(`/posts/${id}`),
  getPending: () => api.get('/admin/posts/pending'),
  approve: (id) => api.post(`/admin/posts/${id}/approve`),
  reject: (id, reason) => api.post(`/admin/posts/${id}/reject`, { reason })
};

// 评论相关接口
export const commentApi = {
  getList: (postId) => api.get(`/posts/${postId}/comments`),
  create: (postId, data) => api.post(`/posts/${postId}/comments`, data),
  delete: (id) => api.delete(`/comments/${id}`)
};

// 通知相关接口
export const notificationApi = {
  getList: (params) => api.get('/notifications', { params }),
  markAsRead: (id) => api.post(`/notifications/${id}/read`),
  markAllAsRead: () => api.post('/notifications/read_all')
};

// 分类相关接口
export const categoryApi = {
  getList: () => api.get('/categories'),
  create: (data) => api.post('/categories', data),
  update: (id, data) => api.put(`/categories/${id}`, data),
  delete: (id) => api.delete(`/categories/${id}`)
};

// 管理员相关接口
export const adminApi = {
  getPendingPosts: () => api.get('/admin/posts/pending'),
  approvePost: (postId) => api.post(`/admin/posts/${postId}/approve`),
  rejectPost: (postId, reason) => api.post(`/admin/posts/${postId}/reject`, { reason }),
  getUsers: () => api.get('/admin/users'),
  updateUser: (userId, data) => api.put(`/admin/users/${userId}`, data),
  deleteUser: (userId) => api.delete(`/admin/users/${userId}`)
};

// 点赞相关接口
export const likesApi = {
  likePost: (postId) => api.post(`/posts/${postId}/like`),
  unlikePost: (postId) => api.delete(`/posts/${postId}/like`),
  likeComment: (commentId) => api.post(`/comments/${commentId}/like`),
  unlikeComment: (commentId) => api.delete(`/comments/${commentId}/like`)
};

export default api;
