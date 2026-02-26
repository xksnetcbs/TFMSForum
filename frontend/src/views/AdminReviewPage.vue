<template>
  <Layout>
    <div class="admin-review-page">
      <h1>帖子审核</h1>
      
      <div class="post-list">
        <div class="post-item" v-for="post in pendingPosts" :key="post.id">
          <h2>{{ post.title }}</h2>
          <div class="post-meta">
            <span class="author">{{ post.author_username }}</span>
            <span class="category">{{ post.category_name }}</span>
            <span class="date">{{ formatDate(post.created_at) }}</span>
          </div>
          <div class="post-excerpt">{{ post.content_excerpt }}</div>
          <div class="review-actions">
            <button @click="approvePost(post.id)" class="approve-btn">通过</button>
            <button @click="rejectPost(post.id)" class="reject-btn">拒绝</button>
          </div>
        </div>
      </div>
      
      <div class="modal" v-if="showRejectModal">
        <div class="modal-content">
          <h3>拒绝原因</h3>
          <textarea v-model="rejectReason" placeholder="请输入拒绝原因" rows="4"></textarea>
          <div class="modal-actions">
            <button @click="showRejectModal = false" class="cancel-btn">取消</button>
            <button @click="confirmReject" class="confirm-btn">确认拒绝</button>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Layout from '../components/Layout/Layout.vue';
import { postApi } from '../api';

const pendingPosts = ref([]);
const showRejectModal = ref(false);
const rejectReason = ref('');
const currentPostId = ref(null);

const loadPendingPosts = async () => {
  try {
    const response = await postApi.getPending();
    pendingPosts.value = response.data;
  } catch (error) {
    console.error('加载待审核帖子失败:', error);
  }
};

const approvePost = async (postId) => {
  try {
    await postApi.approve(postId);
    // 重新加载待审核帖子
    await loadPendingPosts();
  } catch (error) {
    console.error('审核通过失败:', error);
  }
};

const rejectPost = (postId) => {
  currentPostId.value = postId;
  rejectReason.value = '';
  showRejectModal.value = true;
};

const confirmReject = async () => {
  if (!currentPostId.value) return;
  
  try {
    await postApi.reject(currentPostId.value, rejectReason.value);
    showRejectModal.value = false;
    // 重新加载待审核帖子
    await loadPendingPosts();
  } catch (error) {
    console.error('审核拒绝失败:', error);
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};

onMounted(() => {
  loadPendingPosts();
});
</script>

<style scoped>
.admin-review-page {
  padding: 1rem;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.post-item {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.post-item:hover {
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.post-item h2 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.post-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.post-excerpt {
  color: #555;
  line-height: 1.5;
  margin-bottom: 1rem;
}

.review-actions {
  display: flex;
  gap: 1rem;
}

.approve-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.reject-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.modal {
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
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 1rem;
}

.modal-content textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  margin-bottom: 1rem;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.cancel-btn {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.confirm-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
</style>
