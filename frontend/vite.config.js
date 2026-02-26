import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'https://tfms.forum.dcpstudios.top',
        changeOrigin: true,
        secure: false
      }
    },
    host: '0.0.0.0',  // 监听所有网络接口
    port: 5175,
    // 添加允许访问的主机名列表
    allowedHosts: [
      'tfms.forum.dcpstudios.top', // 允许的域名
      // 可以添加多个域名或IP地址
      'localhost',
      '127.0.0.1',
      '192.168.89.12',
      '115.190.63.33' // 你的公网IP，如果需要通过IP访问也可以加上
    ]
  }
})
