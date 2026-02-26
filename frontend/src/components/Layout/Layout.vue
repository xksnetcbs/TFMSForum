<template>
  <div class="layout">
    <header class="header">
      <!-- 注意：如果你希望头部也左右顶到头，请同样移除这里的 container 类 -->
      <div class="container header-container">
        <div class="logo">
          <router-link to="/">TFMS Forum</router-link>
        </div>

        <div class="header-actions">
          <button @click="toggleTheme" class="theme-toggle-btn" title="切换主题">
            {{ isDarkTheme ? '☀️' : '🌙' }}
          </button>
          <div class="user-info" v-if="isAuthenticated">
            <router-link to="/profile" class="username" title="个人信息">
              {{ user?.username }}
            </router-link>
            <router-link to="/notifications" class="notification-link" title="通知">
              <span class="icon">🔔</span>
            </router-link>
            <button @click="logout" class="btn btn-secondary btn-sm">登出</button>
          </div>
          <div class="auth-links" v-else>
            <router-link to="/login" class="btn btn-secondary btn-sm">登录</router-link>
            <router-link to="/register" class="btn btn-primary btn-sm">注册</router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- 修改点1：移除了 'container' 类，只保留 main-container -->
    <div class="main-container">
      <aside class="left-sidebar">
        <div class="sidebar-card">
          <h3 class="sidebar-title">分类</h3>
          <ul class="category-list">
            <li>
              <router-link to="/" exact-active-class="active" class="category-link">
                <span class="icon">🏠</span> 全部
              </router-link>
            </li>
            <li v-for="category in categories" :key="category.id">
              <router-link :to="`/category/${category.id}`" active-class="active" class="category-link">
                <span class="icon">📂</span> {{ category.name }}
              </router-link>
            </li>
          </ul>
        </div>

        <div class="user-actions" v-if="isAuthenticated">
          <router-link to="/create" class="btn btn-primary btn-block">
            <span class="icon">✏️</span> 发布帖子
          </router-link>
          <router-link to="/admin/review" class="btn btn-secondary btn-block mt-2" v-if="isAdmin">
            <span class="icon">🛡️</span> 审核管理
          </router-link>
          <router-link to="/admin/users" class="btn btn-secondary btn-block mt-2" v-if="isAdmin">
            <span class="icon">👥</span> 用户管理
          </router-link>
        </div>
      </aside>

      <main class="content">
        <slot></slot>
      </main>

      <aside class="right-sidebar">
        <div class="sidebar-card">
          <h3 class="sidebar-title">🔥 热门帖子</h3>
          <ul class="sidebar-post-list">
            <li v-for="post in hotPosts" :key="post.id" class="sidebar-post-item">
              <router-link :to="`/post/${post.id}`" class="sidebar-post-link">
                {{ post.title }}
              </router-link>
            </li>
          </ul>
        </div>

        <div class="sidebar-card mt-3">
          <h3 class="sidebar-title">🆕 最新发布</h3>
          <ul class="sidebar-post-list">
            <li v-for="post in latestPosts" :key="post.id" class="sidebar-post-item">
              <router-link :to="`/post/${post.id}`" class="sidebar-post-link">
                {{ post.title }}
              </router-link>
            </li>
          </ul>
        </div>
      </aside>
    </div>

    <footer class="footer">
      <div class="container">
        <p>&copy; {{ new Date().getFullYear() }} TFMS Forum. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import store from '../../store';
import { categoryApi, postApi } from '../../api';

const router = useRouter();
const categories = ref([]);
const hotPosts = ref([]);
const latestPosts = ref([]);

const isAuthenticated = ref(false);
const user = ref(null);
const isAdmin = ref(false);
const isDarkTheme = ref(false);

const logout = async () => {
  await store.actions.logout();
  router.push('/');
};

const toggleTheme = () => {
  isDarkTheme.value = !isDarkTheme.value;
  if (isDarkTheme.value) {
    document.body.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  } else {
    document.body.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  }
};

const initTheme = () => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDarkTheme.value = true;
    document.body.classList.add('dark');
  } else {
    isDarkTheme.value = false;
    document.body.classList.remove('dark');
  }
};

const loadCategories = async () => {
  try {
    const response = await categoryApi.getList();
    categories.value = response.data;
  } catch (error) {
    console.error('加载分类失败:', error);
  }
};

const loadHotPosts = async () => {
  try {
    const response = await postApi.getList({ sort: 'hot', status: 'approved', page_size: 5 });
    hotPosts.value = response.data.items;
  } catch (error) {
    console.error('加载热门帖子失败:', error);
  }
};

const loadLatestPosts = async () => {
  try {
    const response = await postApi.getList({ sort: 'latest', status: 'approved', page_size: 5 });
    latestPosts.value = response.data.items;
  } catch (error) {
    console.error('加载最新帖子失败:', error);
  }
};

onMounted(async () => {
  // 初始化主题
  initTheme();
  
  // 加载用户信息
  const userData = await store.actions.getCurrentUser();
  isAuthenticated.value = store.getters.isAuthenticated();
  user.value = store.getters.user();
  isAdmin.value = store.getters.isAdmin();

  // 加载分类和帖子
  await loadCategories();
  await loadHotPosts();
  await loadLatestPosts();
});
</script>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: var(--bg-body);
}

.header {
  background-color: var(--bg-header);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-sm);
  height: 56px;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.logo a {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
  text-decoration: none;
  letter-spacing: -0.5px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.theme-toggle-btn {
  background: none;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  padding: 0.25rem;
  cursor: pointer;
  font-size: 1rem;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
}

.theme-toggle-btn:hover {
  background-color: var(--bg-body);
  border-color: var(--text-secondary);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.username {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.notification-link {
  font-size: 1.125rem;
  color: var(--text-secondary);
  transition: color var(--transition-fast);
}

.notification-link:hover {
  color: var(--primary-color);
}

.auth-links {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  padding: 0.25rem 0.625rem;
  font-size: 0.8125rem;
}

/* 修改点2：更新 main-container 样式，确保撑满宽度 */
.main-container {
  display: flex;
  flex: 1;
  width: 100%; /* 强制宽度 100% */
  padding: 1.25rem; /* 添加统一的内边距，防止内容紧贴屏幕边缘 */
  gap: 1.25rem;
  box-sizing: border-box; /* 确保 padding 包含在 width 内 */
}

.left-sidebar {
  width: 200px;
  flex-shrink: 0;
}

.sidebar-card {
  background-color: var(--bg-card);
  border-radius: var(--border-radius);
  padding: 1rem;
  border: 1px solid var(--border-color);
}

.sidebar-title {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-light);
  margin-bottom: 0.75rem;
  font-weight: 600;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.category-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.5rem;
  border-radius: var(--border-radius);
  color: var(--text-secondary);
  font-weight: 500;
  transition: all var(--transition-fast);
  font-size: 0.875rem;
}

.category-link:hover {
  background-color: var(--bg-body);
  color: var(--text-primary);
}

.category-link.active {
  background-color: rgba(59, 130, 246, 0.1);
  color: var(--primary-color);
}

.category-link .icon {
  font-size: 1rem;
}

.user-actions {
  margin-top: 1rem;
}

.btn-block {
  display: flex;
  width: 100%;
  justify-content: center;
}

.mt-2 {
  margin-top: 0.5rem;
}

.mt-3 {
  margin-top: 1rem;
}

.content {
  flex: 1;
  min-width: 0;
}

.right-sidebar {
  width: 240px;
  flex-shrink: 0;
}

.sidebar-post-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.sidebar-post-item {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
}

.sidebar-post-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.sidebar-post-link {
  color: var(--text-primary);
  font-size: 0.8125rem;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  font-weight: 500;
}

.sidebar-post-link:hover {
  color: var(--primary-color);
}

.footer {
  background-color: var(--bg-card);
  border-top: 1px solid var(--border-color);
  padding: 1rem 0;
  margin-top: auto;
  text-align: center;
  color: var(--text-light);
  font-size: 0.75rem;
}

@media (max-width: 1024px) {
  .main-container {
    flex-direction: column;
  }
  
  .left-sidebar, .right-sidebar {
    width: 100%;
  }
  
  .right-sidebar {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .right-sidebar {
    grid-template-columns: 1fr;
  }
  
  .header-container {
    padding: 0 1rem;
  }
}
</style>
