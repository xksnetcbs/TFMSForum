<template>
  <Layout>
    <div class="user-profile-page">
      <h1>个人信息</h1>
      
      <form @submit.prevent="updateProfile" class="profile-form">
        <div class="form-group">
          <label for="username" class="form-label">用户名</label>
          <input 
            type="text" 
            id="username" 
            v-model="formData.username"
            class="input-field"
            disabled
          >
        </div>
        
        <div class="form-group">
          <label for="email" class="form-label">邮箱</label>
          <input 
            type="email" 
            id="email" 
            v-model="formData.email"
            class="input-field"
            disabled
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
        
        <div class="error-message" v-if="error">
          <span class="icon">⚠️</span> {{ error }}
        </div>
        
        <div class="success-message" v-if="success">
          <span class="icon">✅</span> 个人信息更新成功
        </div>
        
        <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
          {{ loading ? '更新中...' : '更新信息' }}
        </button>
      </form>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Layout from '../components/Layout/Layout.vue';
import { authApi } from '../api';
import store from '../store';

const router = useRouter();
const loading = ref(false);
const error = ref('');
const success = ref(false);

const formData = ref({
  username: '',
  email: '',
  real_name: '',
  student_id: '',
  admission_year: null
});

const loadUserInfo = async () => {
  try {
    const userData = await store.actions.getCurrentUser();
    if (userData) {
      formData.value = {
        username: userData.username,
        email: userData.email,
        real_name: userData.real_name || '',
        student_id: userData.student_id || '',
        admission_year: userData.admission_year || null
      };
    }
  } catch (error) {
    console.error('加载用户信息失败:', error);
  }
};

const updateProfile = async () => {
  loading.value = true;
  error.value = '';
  success.value = false;
  
  try {
    await authApi.updateUserInfo(formData.value);
    success.value = true;
    // 重新加载用户信息
    await store.actions.getCurrentUser();
  } catch (err) {
    error.value = err.response?.data?.error || '更新失败，请检查输入信息';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadUserInfo();
});
</script>

<style scoped>
.user-profile-page {
  padding: 1rem;
}

.profile-form {
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  color: var(--text-primary);
}

.input-field {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 1rem;
}

.input-field:disabled {
  background-color: var(--bg-muted);
  cursor: not-allowed;
}

.error-message {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 0.75rem;
  border-radius: var(--border-radius);
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.success-message {
  background-color: #dcfce7;
  color: #166534;
  padding: 0.75rem;
  border-radius: var(--border-radius);
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-block {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
}
</style>
