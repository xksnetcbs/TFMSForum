<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h1 class="auth-title">欢迎回来</h1>
        <p class="auth-subtitle">登录您的 TFMS Forum 账号</p>
      </div>
      
      <form @submit.prevent="login" class="auth-form">
        <div class="form-group">
          <label for="identifier" class="form-label">用户名或邮箱</label>
          <input 
            type="text" 
            id="identifier" 
            v-model="formData.identifier"
            class="input-field"
            placeholder="请输入用户名或邮箱"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="password" class="form-label">密码</label>
          <input 
            type="password" 
            id="password" 
            v-model="formData.password"
            class="input-field"
            placeholder="请输入密码"
            required
          >
        </div>
        
        <div class="error-message" v-if="error">
          <span class="icon">⚠️</span> {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
        
        <div class="auth-footer">
          还没有账号？<router-link to="/register" class="auth-link">立即注册</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import store from '../store';

const router = useRouter();
const loading = ref(false);
const error = ref('');

const formData = ref({
  identifier: '',
  password: ''
});

const login = async () => {
  if (!formData.value.identifier || !formData.value.password) {
    return;
  }
  
  loading.value = true;
  error.value = '';
  
  try {
    await store.actions.login(formData.value);
    router.push('/');
  } catch (err) {
    error.value = store.state.error || '登录失败，请检查用户名/邮箱和密码';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--bg-body);
  padding: 1rem;
}

.auth-card {
  background-color: var(--bg-card);
  padding: 1.5rem; /* Reduced padding */
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  width: 100%;
  max-width: 360px; /* Reduced max-width */
  border: 1px solid var(--border-color);
}

.auth-header {
  text-align: center;
  margin-bottom: 1.25rem; /* Reduced margin */
}

.auth-title {
  font-size: 1.25rem; /* Reduced font size */
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem; /* Reduced margin */
}

.auth-subtitle {
  color: var(--text-secondary);
  font-size: 0.8125rem; /* Reduced font size */
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1rem; /* Reduced gap */
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.375rem; /* Reduced gap */
}

.form-label {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.8125rem; /* Reduced font size */
}

.error-message {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 0.5rem; /* Reduced padding */
  border-radius: var(--border-radius);
  font-size: 0.75rem; /* Reduced font size */
  display: flex;
  align-items: center;
  gap: 0.375rem; /* Reduced gap */
}

.btn-block {
  width: 100%;
  padding: 0.5rem; /* Reduced padding */
  font-size: 0.875rem; /* Reduced font size */
}

.auth-footer {
  text-align: center;
  margin-top: 1rem; /* Reduced margin */
  font-size: 0.75rem; /* Reduced font size */
  color: var(--text-secondary);
}

.auth-link {
  color: var(--primary-color);
  font-weight: 500;
  text-decoration: none;
}

.auth-link:hover {
  text-decoration: underline;
}
</style>
