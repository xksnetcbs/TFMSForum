<template>
  <Layout>
    <div class="create-post-page">
      <h1>发布帖子</h1>
      
      <form @submit.prevent="submitPost" class="post-form">
        <div class="form-group text-primary">
          <label for="title">标题</label>
          <input 
            type="text" 
            id="title" 
            v-model="formData.title"
            placeholder="请输入标题"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="category">分类</label>
          <select 
            id="category" 
            v-model="formData.category_id"
            required
          >
            <option value="">请选择分类</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="content">内容</label>
          <div class="markdown-editor">
            <textarea 
              id="content" 
              v-model="formData.content_markdown"
              placeholder="请输入内容（支持 Markdown 格式）"
              rows="10"
              required
            ></textarea>
            <div class="preview" v-if="showPreview">
              <h3>预览</h3>
              <div v-html="renderedContent"></div>
            </div>
          </div>
          <div class="editor-toggle">
            <button type="button" @click="showPreview = !showPreview">
              {{ showPreview ? '编辑' : '预览' }}
            </button>
          </div>
        </div>
        
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? '提交中...' : '提交' }}
        </button>
      </form>
      
      <div class="success-message" v-if="success">
        帖子已提交，等待审核！
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { marked } from 'marked';
import Layout from '../components/Layout/Layout.vue';
import { postApi, categoryApi } from '../api';

const router = useRouter();
const categories = ref([]);
const showPreview = ref(false);
const loading = ref(false);
const success = ref(false);

const formData = ref({
  title: '',
  content_markdown: '',
  category_id: ''
});

const renderedContent = computed(() => {
  return marked(formData.value.content_markdown);
});

const loadCategories = async () => {
  try {
    const response = await categoryApi.getList();
    categories.value = response.data;
  } catch (error) {
    console.error('加载分类失败:', error);
  }
};

const submitPost = async () => {
  if (!formData.value.title || !formData.value.content_markdown || !formData.value.category_id) {
    return;
  }
  
  loading.value = true;
  try {
    await postApi.create(formData.value);
    success.value = true;
    
    // 3秒后跳转到首页
    setTimeout(() => {
      router.push('/');
    }, 3000);
  } catch (error) {
    console.error('提交帖子失败:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadCategories();
});
</script>

<style scoped>
.create-post-page {
  padding: 1rem;
}

.post-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: var(--text-primary);
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: 1rem;
  background-color: var(--bg-card);
  color: var(--text-primary);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
}

.markdown-editor {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.markdown-editor textarea {
  flex: 1;
  min-height: 300px;
}

.preview {
  flex: 1;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  background-color: var(--bg-card);
  min-height: 300px;
}

.preview h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: var(--text-primary);
}

.editor-toggle {
  margin-top: 0.5rem;
}

.editor-toggle button {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 0.5rem 1rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  color: var(--text-primary);
  transition: all var(--transition-fast);
}

.editor-toggle button:hover {
  background-color: var(--bg-body);
  border-color: var(--text-secondary);
}

.submit-btn {
  background-color: var(--success-color);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  font-size: 1rem;
  cursor: pointer;
  transition: background-color var(--transition-fast);
}

.submit-btn:hover {
  opacity: 0.9;
}

.submit-btn:disabled {
  background-color: var(--text-light);
  cursor: not-allowed;
}

.success-message {
  margin-top: 1rem;
  padding: 1rem;
  background-color: rgba(16, 185, 129, 0.1);
  color: var(--success-color);
  border: 1px solid rgba(16, 185, 129, 0.3);
  border-radius: var(--border-radius);
  text-align: center;
}
</style>
