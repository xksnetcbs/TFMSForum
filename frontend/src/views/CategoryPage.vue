<template>
  <Layout>
    <div class="category-page">
      <h1>{{ categoryName }}</h1>
      
      <div class="post-list">
        <div class="post-item" v-for="post in posts" :key="post.id">
          <h2>
            <router-link :to="`/post/${post.id}`">{{ post.title }}</router-link>
          </h2>
          <div class="post-meta">
            <span class="author">{{ post.author_username }}</span>
            <span class="date">{{ formatDate(post.created_at) }}</span>
          </div>
          <div class="post-excerpt">{{ post.content_excerpt }}</div>
        </div>
      </div>
      
      <div class="pagination" v-if="total > pageSize">
        <button 
          :disabled="currentPage === 1" 
          @click="setPage(currentPage - 1)"
        >
          上一页
        </button>
        <span>{{ currentPage }} / {{ totalPages }}</span>
        <button 
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
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import Layout from '../components/Layout/Layout.vue';
import { postApi, categoryApi } from '../api';

const route = useRoute();
const posts = ref([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const categoryName = ref('');

const totalPages = computed(() => {
  return Math.ceil(total.value / pageSize.value);
});

const loadPosts = async () => {
  const categoryId = route.params.id;
  try {
    const response = await postApi.getList({
      page: currentPage.value,
      page_size: pageSize.value,
      category: categoryId,
      status: 'approved'
    });
    posts.value = response.data.items;
    total.value = response.data.total;
  } catch (error) {
    console.error('加载帖子失败:', error);
  }
};

const loadCategoryName = async () => {
  const categoryId = route.params.id;
  try {
    const response = await categoryApi.getList();
    const category = response.data.find(c => c.id == categoryId);
    if (category) {
      categoryName.value = category.name;
    } else {
      categoryName.value = '分类不存在';
    }
  } catch (error) {
    console.error('加载分类失败:', error);
  }
};

const setPage = (page) => {
  currentPage.value = page;
  loadPosts();
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};

watch(() => route.params.id, () => {
  currentPage.value = 1;
  loadCategoryName();
  loadPosts();
});

onMounted(() => {
  loadCategoryName();
  loadPosts();
});
</script>

<style scoped>
.category-page {
  padding: 1rem;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.post-item {
  padding: 1rem;
  border: 1px solid var(--border-color);
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

.post-item h2 a {
  color: var(--text-primary);
  text-decoration: none;
}

.post-item h2 a:hover {
  color: #2196F3;
}

.post-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.post-excerpt {
  color: var(--text-secondary);
  line-height: 1.5;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination button {
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-color);
  background-color: var(--bg-card);
  border-radius: 4px;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination span {
  font-size: 0.875rem;
  color: #666;
}
</style>
