import { reactive, readonly, ref } from 'vue';
import { authApi } from '../api';

const state = reactive({
  user: null,
  loading: false,
  error: null
});

const isAuthenticated = ref(false);

const actions = {
  async login(credentials) {
    state.loading = true;
    state.error = null;
    try {
      const response = await authApi.login(credentials);
      state.user = response.data;
      isAuthenticated.value = true;
      return response.data;
    } catch (error) {
      state.error = error.response?.data?.error || '登录失败';
      throw error;
    } finally {
      state.loading = false;
    }
  },

  async register(userData) {
    state.loading = true;
    state.error = null;
    try {
      const response = await authApi.register(userData);
      state.user = response.data;
      isAuthenticated.value = true;
      return response.data;
    } catch (error) {
      state.error = error.response?.data?.error || '注册失败';
      throw error;
    } finally {
      state.loading = false;
    }
  },

  async logout() {
    try {
      await authApi.logout();
      state.user = null;
      isAuthenticated.value = false;
    } catch (error) {
      console.error('登出失败:', error);
    }
  },

  async getCurrentUser() {
    state.loading = true;
    try {
      const response = await authApi.getCurrentUser();
      state.user = response.data;
      isAuthenticated.value = true;
      return response.data;
    } catch (error) {
      state.user = null;
      isAuthenticated.value = false;
      return null;
    } finally {
      state.loading = false;
    }
  }
};

const getters = {
  user: () => state.user,
  loading: () => state.loading,
  error: () => state.error,
  isAuthenticated: () => isAuthenticated.value,
  isAdmin: () => state.user?.is_admin || false
};

export default {
  state: readonly(state),
  getters,
  actions
};
