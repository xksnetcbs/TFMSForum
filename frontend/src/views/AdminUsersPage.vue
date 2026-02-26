<template>
  <div class="container">
    <h1 class="page-title">用户管理</h1>
    
    <div v-if="isLoading" class="loading">
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>
    
    <div v-else class="user-management">
      <table class="user-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>邮箱</th>
            <th>真实姓名</th>
            <th>学号</th>
            <th>入学年份</th>
            <th>是否管理员</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.real_name || '-' }}</td>
            <td>{{ user.student_id || '-' }}</td>
            <td>{{ user.admission_year || '-' }}</td>
            <td>
              <input 
                type="checkbox" 
                v-model="user.is_admin" 
                @change="updateUser(user)"
              >
            </td>
            <td>{{ formatDate(user.created_at) }}</td>
            <td>
              <button 
                class="btn btn-primary btn-sm" 
                @click="openEditModal(user)"
              >
                编辑
              </button>
              <button 
                class="btn btn-danger btn-sm" 
                @click="confirmDelete(user)"
              >
                删除
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 编辑用户模态框 -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal" @click.stop>
        <h2>编辑用户</h2>
        <form @submit.prevent="saveUserChanges">
          <div class="form-group">
            <label for="real_name">真实姓名</label>
            <input 
              type="text" 
              id="real_name" 
              v-model="editingUser.real_name" 
              class="input-field"
            >
          </div>
          <div class="form-group">
            <label for="student_id">学号</label>
            <input 
              type="text" 
              id="student_id" 
              v-model="editingUser.student_id" 
              class="input-field"
            >
          </div>
          <div class="form-group">
            <label for="admission_year">入学年份</label>
            <input 
              type="number" 
              id="admission_year" 
              v-model="editingUser.admission_year" 
              class="input-field"
            >
          </div>
          <div class="form-group">
            <label for="is_admin">是否管理员</label>
            <input 
              type="checkbox" 
              id="is_admin" 
              v-model="editingUser.is_admin"
            >
          </div>
          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="closeEditModal">取消</button>
            <button type="submit" class="btn btn-primary">保存</button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- 删除确认模态框 -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal" @click.stop>
        <h2>确认删除</h2>
        <p>确定要删除用户 {{ deletingUser?.username }} 吗？</p>
        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" @click="closeDeleteModal">取消</button>
          <button type="button" class="btn btn-danger" @click="deleteUser">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { authApi, adminApi } from '../api';

export default {
  name: 'AdminUsersPage',
  setup() {
    const users = ref([]);
    const isLoading = ref(true);
    const error = ref('');
    const showEditModal = ref(false);
    const showDeleteModal = ref(false);
    const editingUser = ref({});
    const deletingUser = ref(null);
    
    const loadUsers = async () => {
      try {
        isLoading.value = true;
        error.value = '';
        const response = await adminApi.getUsers();
        users.value = response.data;
      } catch (err) {
        error.value = '加载用户列表失败';
        console.error(err);
      } finally {
        isLoading.value = false;
      }
    };
    
    const updateUser = async (user) => {
      try {
        await adminApi.updateUser(user.id, {
          is_admin: user.is_admin
        });
      } catch (err) {
        console.error('更新用户失败', err);
        // 恢复原来的状态
        loadUsers();
      }
    };
    
    const openEditModal = (user) => {
      editingUser.value = { ...user };
      showEditModal.value = true;
    };
    
    const closeEditModal = () => {
      showEditModal.value = false;
      editingUser.value = {};
    };
    
    const saveUserChanges = async () => {
      try {
        await adminApi.updateUser(editingUser.value.id, {
          real_name: editingUser.value.real_name,
          student_id: editingUser.value.student_id,
          admission_year: editingUser.value.admission_year,
          is_admin: editingUser.value.is_admin
        });
        closeEditModal();
        loadUsers();
      } catch (err) {
        console.error('保存用户信息失败', err);
      }
    };
    
    const confirmDelete = (user) => {
      deletingUser.value = user;
      showDeleteModal.value = true;
    };
    
    const closeDeleteModal = () => {
      showDeleteModal.value = false;
      deletingUser.value = null;
    };
    
    const deleteUser = async () => {
      if (!deletingUser.value) return;
      
      try {
        await adminApi.deleteUser(deletingUser.value.id);
        closeDeleteModal();
        loadUsers();
      } catch (err) {
        console.error('删除用户失败', err);
      }
    };
    
    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleString();
    };
    
    onMounted(() => {
      loadUsers();
    });
    
    return {
      users,
      isLoading,
      error,
      showEditModal,
      showDeleteModal,
      editingUser,
      deletingUser,
      updateUser,
      openEditModal,
      closeEditModal,
      saveUserChanges,
      confirmDelete,
      closeDeleteModal,
      deleteUser,
      formatDate
    };
  }
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  margin-bottom: 20px;
  text-align: center;
}

.loading, .error {
  text-align: center;
  padding: 40px;
}

.user-management {
  background-color: var(--bg-card);
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.user-table {
  width: 100%;
  border-collapse: collapse;
}

.user-table th, .user-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.user-table th {
  background-color: var(--bg-card);
  font-weight: bold;
}

.user-table tr:hover {
  background-color: var(--hover-color);
}

.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-right: 5px;
}

.btn-primary {
  background-color: #4CAF50;
  color: var(--text-color);
}

.btn-primary:hover {
  background-color: #45a049;
}

.btn-danger {
  background-color: #f44336;
  color: var(--text-color);
}

.btn-danger:hover {
  background-color: #da190b;
}

.btn-secondary {
  background-color: var(--bg-button);
  color: var(--text-color);
}

.btn-secondary:hover {
  background-color: var(--hover-color);
}

.btn-sm {
  font-size: 12px;
  padding: 4px 8px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background-color: var(--bg-card);
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-field {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.modal-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>