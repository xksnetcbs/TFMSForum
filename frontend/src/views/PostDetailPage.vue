<template>
  <Layout>
    <div class="post-detail-page" v-if="post">
      <h1>{{ post.title }}</h1>
      <div class="post-meta">
        <span class="author">{{ post.author_username }}</span>
        <span class="category">{{ post.category_name }}</span>
        <span class="date">{{ formatDate(post.created_at) }}</span>
        <span class="status" :class="post.status">{{ statusText }}</span>
        <span class="views">👁️ {{ post.views || 0 }}</span>
        <span class="comments-count">💬 {{ post.comments_count || 0 }}</span>
        <button 
          v-if="isAuthenticated" 
          @click="togglePostLike" 
          class="like-btn"
          :class="{ 'liked': post.is_liked }"
        >
          {{ post.is_liked ? '❤️' : '🤍' }} {{ post.likes_count || 0 }}
        </button>
        <div v-if="isAdmin" class="admin-actions">
          <button @click="editPost" class="admin-btn edit-btn">编辑</button>
          <button @click="deletePost" class="admin-btn delete-btn">删除</button>
        </div>
      </div>
      
      <div class="post-content" v-html="renderedContent"></div>
      
      <div class="comments-section">
        <h2>评论</h2>
        
        <div class="comment-form" v-if="isAuthenticated">
          <textarea 
            class="comment-input"
            v-model="commentContent" 
            placeholder="写下你的评论..."
            rows="4"
          ></textarea>
          <button @click="submitComment" class="submit-btn">提交评论</button>
        </div>
        
        <div class="comment-list">
          <div class="comment-item" v-for="comment in comments" :key="comment.id">
            <div class="comment-header">
              <span class="comment-author">{{ comment.author_username }}</span>
              <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
              <button 
                v-if="isAuthenticated" 
                @click="toggleCommentLike(comment.id)" 
                class="comment-like-btn"
                :class="{ 'liked': comment.is_liked }"
              >
                {{ comment.is_liked ? '❤️' : '🤍' }} {{ comment.likes_count || 0 }}
              </button>
            </div>
            <div class="comment-content">{{ comment.content }}</div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 编辑帖子模态框 -->
    <div v-if="isEditing" class="modal-overlay">
      <div class="modal-content">
        <h2>编辑帖子</h2>
        <div class="form-group">
          <label>标题</label>
          <input type="text" v-model="editForm.title" class="form-input">
        </div>
        <div class="form-group">
          <label>内容 (Markdown)</label>
          <textarea v-model="editForm.content_markdown" class="form-textarea" rows="10"></textarea>
        </div>
        <div class="form-group">
          <label>分类</label>
          <input type="number" v-model="editForm.category_id" class="form-input">
        </div>
        <div class="form-group">
          <label>状态</label>
          <select v-model="editForm.status" class="form-select">
            <option value="pending">待审核</option>
            <option value="approved">已通过</option>
            <option value="rejected">已拒绝</option>
          </select>
        </div>
        <div class="modal-actions">
          <button @click="saveEdit" class="btn save-btn">保存</button>
          <button @click="cancelEdit" class="btn cancel-btn">取消</button>
        </div>
      </div>
    </div>
    
    <div class="loading" v-else>加载中...</div>
  </Layout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { marked } from 'marked';
import Layout from '../components/Layout/Layout.vue';
import { postApi, commentApi, likesApi } from '../api';
import store from '../store';

const route = useRoute();
const post = ref(null);
const comments = ref([]);
const commentContent = ref('');

const isAuthenticated = computed(() => store.getters.isAuthenticated());
const isAdmin = computed(() => store.getters.isAdmin());

const statusText = computed(() => {
  if (!post.value) return '';
  switch (post.value.status) {
    case 'pending': return '待审核';
    case 'approved': return '已通过';
    case 'rejected': return '已拒绝';
    default: return '';
  }
});

const renderedContent = computed(() => {
  if (!post.value) return '';
  return marked(post.value.content_markdown);
});

const loadPost = async () => {
  const postId = route.params.id;
  try {
    const response = await postApi.getDetail(postId);
    post.value = response.data;
  } catch (error) {
    console.error('加载帖子失败:', error);
  }
};

const loadComments = async () => {
  const postId = route.params.id;
  try {
    const response = await commentApi.getList(postId);
    comments.value = response.data;
  } catch (error) {
    console.error('加载评论失败:', error);
  }
};

const submitComment = async () => {
  if (!commentContent.value.trim()) return;
  
  const postId = route.params.id;
  try {
    await commentApi.create(postId, { content: commentContent.value });
    commentContent.value = '';
    await loadComments();
  } catch (error) {
    console.error('提交评论失败:', error);
  }
};

const togglePostLike = async () => {
  const postId = route.params.id;
  try {
    if (post.value.is_liked) {
      await likesApi.unlikePost(postId);
      post.value.is_liked = false;
      post.value.likes_count = Math.max(0, (post.value.likes_count || 0) - 1);
    } else {
      await likesApi.likePost(postId);
      post.value.is_liked = true;
      post.value.likes_count = (post.value.likes_count || 0) + 1;
    }
  } catch (error) {
    console.error('点赞操作失败:', error);
  }
};

const toggleCommentLike = async (commentId) => {
  try {
    const comment = comments.value.find(c => c.id === commentId);
    if (!comment) return;
    
    if (comment.is_liked) {
      await likesApi.unlikeComment(commentId);
      comment.is_liked = false;
      comment.likes_count = Math.max(0, (comment.likes_count || 0) - 1);
    } else {
      await likesApi.likeComment(commentId);
      comment.is_liked = true;
      comment.likes_count = (comment.likes_count || 0) + 1;
    }
  } catch (error) {
    console.error('点赞操作失败:', error);
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};

// 编辑帖子相关
const isEditing = ref(false);
const editForm = ref({
  title: '',
  content_markdown: '',
  category_id: '',
  status: ''
});

const deletePost = async () => {
  if (!confirm('确定要删除这篇帖子吗？')) return;
  
  const postId = route.params.id;
  try {
    await postApi.delete(postId);
    alert('帖子删除成功');
    // 跳转到首页
    window.location.href = '/';
  } catch (error) {
    console.error('删除帖子失败:', error);
    alert('删除帖子失败');
  }
};

const editPost = () => {
  if (post.value) {
    editForm.value = {
      title: post.value.title,
      content_markdown: post.value.content_markdown,
      category_id: post.value.category_id,
      status: post.value.status
    };
    isEditing.value = true;
  }
};

const saveEdit = async () => {
  const postId = route.params.id;
  try {
    await postApi.update(postId, editForm.value);
    alert('帖子更新成功');
    isEditing.value = false;
    await loadPost();
  } catch (error) {
    console.error('更新帖子失败:', error);
    alert('更新帖子失败');
  }
};

const cancelEdit = () => {
  isEditing.value = false;
};

onMounted(async () => {
  await loadPost();
  await loadComments();
});

watch(() => route.params.id, async (newId) => {
  if (newId) {
    await loadPost();
    await loadComments();
  }
});
</script>

<style scoped>

.post-detail-page {
  padding: 1rem;
}

.post-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.admin-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: auto;
}

.admin-btn {
  padding: 0.25rem 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.edit-btn {
  background-color: #4CAF50;
  color: var(--bg-card);
}

.delete-btn {
  background-color: #f44336;
  color: var(--bg-card);
}

.admin-btn:hover {
  opacity: 0.8;
}

/* 模态框样式 */
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
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--bg-card);
  color: var(--text-primary);
}

.form-textarea {
  resize: vertical;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn {
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
}

.save-btn {
  background-color: #4CAF50;
  color: var(--bg-card);
}

.cancel-btn {
  background-color: #9e9e9e;
  color: var(--bg-card);
}

.btn:hover {
  opacity: 0.8;
}

.like-btn {
  background: none;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.like-btn:hover {
  background-color: var(--bg-card);
}

.like-btn.liked {
  background-color: var(--bg-card);
  border-color: var(--primary-color);
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.status.pending {
  background-color: #ffc107;
  color: var(--text-primary);
}

.status.approved {
  background-color: #28a745;
  color: var(--text-primary);
}

.status.rejected {
  background-color: #dc3545;
  color: var(--text-primary);
}

.post-content {
  margin-bottom: 2rem;
  line-height: 1.6;
}

.post-content h2 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

.post-content p {
  margin-bottom: 1rem;
}

.post-content code {
  background-color: var(--bg-card);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.post-content pre {
  background-color: var(--bg-card);
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  margin-bottom: 1rem;
}

.post-content pre code {
  background-color: transparent;
  padding: 0;
}

.comments-section {
  margin-top: 2rem;
}

.comment-form {
  margin-bottom: 2rem;
}

.comment-form textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  resize: vertical;
  margin-bottom: 1rem;
}

.submit-btn {
  background-color: #4CAF50;
  color: var(--bg-card);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comment-item {
  padding: 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

.comment-input {
  color: var(--text-primary);
  background-color: var(--bg-card);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.comment-like-btn {
  background: none;
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  border-radius: 4px;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.comment-like-btn:hover {
  background-color: var(--bg-card);
}

.comment-like-btn.liked {
  background-color: var(--bg-card);
  border-color: var(--primary-color);
}

.comment-content {
  line-height: 1.5;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.125rem;
  color: var(--text-secondary);
}
</style>
