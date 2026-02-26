<template>
  <div class="admin-categories-page">
    <h1>分类管理</h1>
    
    <!-- 添加分类表单 -->
    <div class="add-category-form">
      <h2>添加新分类</h2>
      <form @submit.prevent="addCategory">
        <div class="form-group">
          <label for="name">分类名称</label>
          <input 
            type="text" 
            id="name" 
            v-model="newCategory.name" 
            required
            placeholder="请输入分类名称"
          />
        </div>
        <div class="form-group">
          <label for="slug">Slug</label>
          <input 
            type="text" 
            id="slug" 
            v-model="newCategory.slug" 
            required
            placeholder="请输入slug（小写字母和连字符）"
          />
        </div>
        <div class="form-group">
          <label for="order">排序</label>
          <input 
            type="number" 
            id="order" 
            v-model="newCategory.order" 
            min="0"
            placeholder="请输入排序值"
          />
        </div>
        <button type="submit" class="btn btn-primary">添加分类</button>
      </form>
    </div>
    
    <!-- 分类列表 -->
    <div class="categories-list">
      <h2>分类列表</h2>
      <table class="categories-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>名称</th>
            <th>Slug</th>
            <th>排序</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="category in categories" :key="category.id">
            <td>{{ category.id }}</td>
            <td>{{ category.name }}</td>
            <td>{{ category.slug }}</td>
            <td>{{ category.order }}</td>
            <td class="actions">
              <button @click="editCategory(category)" class="btn btn-secondary">编辑</button>
              <button @click="deleteCategory(category.id)" class="btn btn-danger">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 编辑分类模态框 -->
    <div v-if="editingCategory" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <h3>编辑分类</h3>
        <form @submit.prevent="updateCategory">
          <div class="form-group">
            <label for="edit-name">分类名称</label>
            <input 
              type="text" 
              id="edit-name" 
              v-model="editingCategory.name" 
              required
            />
          </div>
          <div class="form-group">
            <label for="edit-slug">Slug</label>
            <input 
              type="text" 
              id="edit-slug" 
              v-model="editingCategory.slug" 
              required
            />
          </div>
          <div class="form-group">
            <label for="edit-order">排序</label>
            <input 
              type="number" 
              id="edit-order" 
              v-model="editingCategory.order" 
              min="0"
            />
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeEditModal" class="btn btn-secondary">取消</button>
            <button type="submit" class="btn btn-primary">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { categoryApi } from '../api';

export default {
  name: 'AdminCategoriesPage',
  setup() {
    const categories = ref([]);
    const newCategory = ref({ name: '', slug: '', order: 0 });
    const editingCategory = ref(null);
    
    // 加载分类列表
    const loadCategories = async () => {
      try {
        const response = await categoryApi.getList();
        categories.value = response.data;
      } catch (error) {
        console.error('加载分类失败:', error);
      }
    };
    
    // 添加分类
    const addCategory = async () => {
      try {
        await categoryApi.create(newCategory.value);
        await loadCategories();
        // 重置表单
        newCategory.value = { name: '', slug: '', order: 0 };
      } catch (error) {
        console.error('添加分类失败:', error);
        alert('添加分类失败: ' + (error.response?.data?.error || '未知错误'));
      }
    };
    
    // 编辑分类
    const editCategory = (category) => {
      editingCategory.value = { ...category };
    };
    
    // 关闭编辑模态框
    const closeEditModal = () => {
      editingCategory.value = null;
    };
    
    // 更新分类
    const updateCategory = async () => {
      try {
        await categoryApi.update(editingCategory.value.id, editingCategory.value);
        await loadCategories();
        closeEditModal();
      } catch (error) {
        console.error('更新分类失败:', error);
        alert('更新分类失败: ' + (error.response?.data?.error || '未知错误'));
      }
    };
    
    // 删除分类
    const deleteCategory = async (categoryId) => {
      if (!confirm('确定要删除这个分类吗？')) return;
      
      try {
        await categoryApi.delete(categoryId);
        await loadCategories();
      } catch (error) {
        console.error('删除分类失败:', error);
        alert('删除分类失败: ' + (error.response?.data?.error || '未知错误'));
      }
    };
    
    // 页面加载时获取分类列表
    onMounted(() => {
      loadCategories();
    });
    
    return {
      categories,
      newCategory,
      editingCategory,
      addCategory,
      editCategory,
      closeEditModal,
      updateCategory,
      deleteCategory
    };
  }
};
</script>

<style scoped>
.admin-categories-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.add-category-form {
  background-color: var(--bg-card);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.add-category-form h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: var(--text-color);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: var(--text-color);
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--bg-input);
  color: var(--text-color);
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-hover);
}

.btn-secondary {
  background-color: var(--secondary-color);
  color: var(--text-color);
}

.btn-secondary:hover {
  background-color: var(--secondary-hover);
}

.btn-danger {
  background-color: var(--danger-color);
  color: white;
}

.btn-danger:hover {
  background-color: var(--danger-hover);
}

.categories-list {
  background-color: var(--bg-card);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.categories-list h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: var(--text-color);
}

.categories-table {
  width: 100%;
  border-collapse: collapse;
}

.categories-table th,
.categories-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-color);
}

.categories-table th {
  background-color: var(--bg-light);
  font-weight: bold;
}

.categories-table tr:hover {
  background-color: var(--bg-hover);
}

.actions {
  display: flex;
  gap: 10px;
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

.modal-content {
  background-color: var(--bg-card);
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: var(--text-color);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}
</style>
