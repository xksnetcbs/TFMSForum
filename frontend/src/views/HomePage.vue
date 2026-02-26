<template>
  <Layout>
    <div class="home-page">
      <div class="page-header">
        <h1 class="page-title">首页</h1>
        <div class="sort-buttons">
          <button 
            class="btn btn-sm"
            :class="currentSort === 'latest' ? 'btn-primary' : 'btn-secondary'"
            @click="setSort('latest')"
          >
            最新
          </button>
          <button 
            class="btn btn-sm"
            :class="currentSort === 'hot' ? 'btn-primary' : 'btn-secondary'"
            @click="setSort('hot')"
          >
            热门
          </button>
        </div>
      </div>
      
      <div class="post-list">
        <div class="post-card" v-for="post in posts" :key="post.id">
          <div class="post-content-wrapper">
            <div class="post-main">
              <div class="post-meta-top">
                <span class="badge badge-secondary">{{ post.category_name }}</span>
                <span class="post-date">{{ formatDate(post.created_at) }}</span>
              </div>
              <h2 class="post-title">
                <router-link :to="`/post/${post.id}`">{{ post.title }}</router-link>
              </h2>
              <div class="post-excerpt">{{ post.content_excerpt }}</div>
            </div>
            
            <div class="post-footer">
              <div class="author-info">
                <span class="author-avatar">{{ post.author_username.charAt(0).toUpperCase() }}</span>
                <span class="author-name">{{ post.author_username }}</span>
              </div>
              <div class="post-stats">
                <span class="stat-item">
                  <span class="icon">👁️</span> {{ post.views || 0 }}
                </span>
                <span class="stat-item">
                  <span class="icon">💬</span> {{ post.comments_count || 0 }}
                </span>
                <span class="stat-item">
                  <span class="icon">👍</span> {{ post.likes_count || 0 }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="pagination" v-if="total > pageSize">
        <button 
          class="btn btn-secondary btn-sm"
          :disabled="currentPage === 1" 
          @click="setPage(currentPage - 1)"
        >
          上一页
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button 
          class="btn btn-secondary btn-sm"
          :disabled="currentPage === totalPages" 
          @click="setPage(currentPage + 1)"
        >
          下一页
        </button>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Layout from '../components/Layout/Layout.vue';
import { postApi } from '../api';

const posts = ref([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const currentSort = ref('latest');

const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value);
});

const loadPosts = async () => {
  try {
    const response = await postApi.getList({
      page: currentPage.value,
      page_size: pageSize.value,
      sort: currentSort.value,
      status: 'approved'
    });
    posts.value = response.data.items;
    total.value = response.data.total;
  } catch (error) {
    console.error('加载帖子失败:', error);
  }
};

const setSort = (sort) => {
  currentSort.value = sort;
  currentPage.value = 1;
  loadPosts();
};

const setPage = (page) => {
  currentPage.value = page;
  loadPosts();
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

onMounted(() => {
  loadPosts();
});
</script>

<style scoped>
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem; /* Reduced margin */
  padding-bottom: 0.75rem; /* Reduced padding */
  border-bottom: 1px solid var(--border-color);
}

.page-title {
  font-size: 1.25rem; /* Reduced font size */
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.sort-buttons {
  display: flex;
  gap: 0.5rem;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem; /* Reduced gap */
}

.post-card {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 1rem; /* Reduced padding */
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.post-card:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
  border-color: var(--primary-color);
}

.post-content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.75rem; /* Reduced gap */
}

.post-meta-top {
  display: flex;
  align-items: center;
  gap: 0.5rem; /* Reduced gap */
  margin-bottom: 0.25rem; /* Reduced margin */
  font-size: 0.75rem;
  color: var(--text-light);
}

.post-title {
  font-size: 1.125rem; /* Reduced font size */
  font-weight: 600;
  line-height: 1.3;
  margin: 0 0 0.25rem 0; /* Reduced margin */
}

.post-title a {
  color: var(--text-primary);
  text-decoration: none;
  transition: color var(--transition-fast);
}

.post-title a:hover {
  color: var(--primary-color);
}

.post-excerpt {
  color: var(--text-secondary);
  line-height: 1.5;
  font-size: 0.875rem; /* Reduced font size */
  display: -webkit-box;
  -webkit-line-clamp: 2; /* Reduced lines */
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem; /* Reduced padding */
  border-top: 1px solid var(--border-color);
}

.author-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.author-avatar {
  width: 20px; /* Reduced size */
  height: 20px; /* Reduced size */
  background-color: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.625rem; /* Reduced font size */
  font-weight: 600;
}

.author-name {
  font-size: 0.75rem; /* Reduced font size */
  font-weight: 500;
  color: var(--text-primary);
}

.post-stats {
  display: flex;
  gap: 0.75rem; /* Reduced gap */
  font-size: 0.75rem; /* Reduced font size */
  color: var(--text-light);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.75rem; /* Reduced gap */
  margin-top: 1.5rem; /* Reduced margin */
}

.page-info {
  font-size: 0.8125rem; /* Reduced font size */
  color: var(--text-secondary);
  font-weight: 500;
}
</style>
