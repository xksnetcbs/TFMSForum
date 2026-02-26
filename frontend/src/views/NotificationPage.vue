<template>
  <Layout>
    <div class="notification-page">
      <h1>通知中心</h1>
      
      <div class="notification-actions">
        <button @click="markAllAsRead" class="mark-all-btn">全部标记已读</button>
      </div>
      
      <div class="notification-list">
        <div 
          class="notification-item" 
          v-for="notification in notifications" 
          :key="notification.id"
          :class="{ unread: !notification.is_read }"
        >
          <div class="notification-header">
            <h3>{{ notification.title }}</h3>
            <span class="notification-date">{{ formatDate(notification.created_at) }}</span>
          </div>
          <div class="notification-content">{{ notification.content }}</div>
          <div class="notification-actions">
            <button 
              v-if="!notification.is_read" 
              @click="markAsRead(notification.id)"
              class="mark-read-btn"
            >
              标记已读
            </button>
          </div>
        </div>
      </div>
      
      <div class="empty-message" v-if="notifications.length === 0">
        暂无通知
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Layout from '../components/Layout/Layout.vue';
import { notificationApi } from '../api';

const notifications = ref([]);

const loadNotifications = async () => {
  try {
    const response = await notificationApi.getList();
    notifications.value = response.data;
  } catch (error) {
    console.error('加载通知失败:', error);
  }
};

const markAsRead = async (notificationId) => {
  try {
    await notificationApi.markAsRead(notificationId);
    // 更新本地通知状态
    const notification = notifications.value.find(n => n.id === notificationId);
    if (notification) {
      notification.is_read = true;
    }
  } catch (error) {
    console.error('标记已读失败:', error);
  }
};

const markAllAsRead = async () => {
  try {
    await notificationApi.markAllAsRead();
    // 更新本地所有通知状态
    notifications.value.forEach(notification => {
      notification.is_read = true;
    });
  } catch (error) {
    console.error('全部标记已读失败:', error);
  }
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString();
};

onMounted(() => {
  loadNotifications();
});
</script>

<style scoped>
.notification-page {
  padding: 1rem;
}

.notification-actions {
  margin-bottom: 1.5rem;
}

.mark-all-btn {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.notification-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.notification-item {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.notification-item.unread {
  background-color: #f9f9f9;
  border-left: 4px solid #2196F3;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.notification-header h3 {
  margin: 0;
  font-size: 1.125rem;
  color: #333;
}

.notification-date {
  font-size: 0.875rem;
  color: #666;
}

.notification-content {
  margin-bottom: 1rem;
  line-height: 1.5;
  color: #555;
}

.notification-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.mark-read-btn {
  background-color: #2196F3;
  color: white;
  border: none;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
}

.empty-message {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.125rem;
}
</style>
