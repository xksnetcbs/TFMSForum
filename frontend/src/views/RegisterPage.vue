<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h1 class="auth-title">创建账号</h1>
        <p class="auth-subtitle">加入 TFMS Forum 社区</p>
      </div>
      
      <form @submit.prevent="register" class="auth-form">
        <div class="form-group">
          <label for="username" class="form-label">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="formData.username"
            class="input-field"
            placeholder="请输入用户名"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="email" class="form-label">邮箱</label>
          <input 
            type="email" 
            id="email" 
            v-model="formData.email"
            class="input-field"
            placeholder="请输入邮箱"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="real_name" class="form-label">真实姓名</label>
          <input 
            type="text" 
            id="real_name" 
            v-model="formData.real_name"
            class="input-field"
            placeholder="请输入真实姓名"
          >
        </div>
        
        <div class="form-group">
          <label for="student_id" class="form-label">学号</label>
          <input 
            type="text" 
            id="student_id" 
            v-model="formData.student_id"
            class="input-field"
            placeholder="请输入学号"
          >
        </div>
        
        <div class="form-group">
          <label for="admission_year" class="form-label">入学年份</label>
          <input 
            type="number" 
            id="admission_year" 
            v-model="formData.admission_year"
            class="input-field"
            placeholder="请输入入学年份"
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
          {{ loading ? '注册中...' : '注册' }}
        </button>
        
        <div class="auth-footer">
          已有账号？<router-link to="/login" class="auth-link">立即登录</router-link>
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
  username: '',
  email: '',
  real_name: '',
  student_id: '',
  admission_year: null,
  password: ''
});

const register = async () => {
  if (!formData.value.username || !formData.value.email || !formData.value.password) {
    return;
  }
  
  loading.value = true;
  error.value = '';
  
  try {
    await store.actions.register(formData.value);
    router.push('/');
  } catch (err) {
    error.value = store.state.error || '注册失败，请检查输入信息';
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
