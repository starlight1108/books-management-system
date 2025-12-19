<template>
  <div id="app">
    <!-- 登录和注册页面不显示侧边栏和头部 -->
    <template v-if="!isAuthPage">
      <el-container style="height: 100vh">
        <el-aside width="200px" class="sidebar">
          <div class="logo">
            <h3>图书管理系统</h3>
          </div>
          <el-menu
            :default-active="$route.path"
            class="el-menu-vertical"
            router
            background-color="#304156"
            text-color="#fff"
            active-text-color="#409EFF"
          >
            <el-menu-item index="/books">
              <el-icon><Reading /></el-icon>
              <span>图书管理</span>
            </el-menu-item>
            <el-menu-item v-if="isAdmin" index="/members">
              <el-icon><User /></el-icon>
              <span>会员管理</span>
            </el-menu-item>
            <el-menu-item index="/borrows">
              <el-icon><Document /></el-icon>
              <span>借阅管理</span>
            </el-menu-item>
            <el-menu-item v-if="isAdmin" index="/statistics">
              <el-icon><TrendCharts /></el-icon>
              <span>统计概览</span>
            </el-menu-item>
          </el-menu>
        </el-aside>

        <el-container>
          <el-header class="header">
            <div class="header-content">
              <h1>{{ $route.name }}</h1>
              <div class="user-info">
                <el-dropdown @command="handleCommand">
                  <span class="el-dropdown-link">
                    {{ username }}
                    <el-icon class="el-icon--right"><arrow-down /></el-icon>
                  </span>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
          </el-header>

          <el-main class="main-content">
            <router-view />
          </el-main>
        </el-container>
      </el-container>
    </template>

    <!-- 登录和注册页面直接显示路由内容 -->
    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Reading, User, Document, TrendCharts, ArrowDown } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const username = ref('')

// 判断是否是登录或注册页面
const isAuthPage = computed(() => {
  return route.path === '/login' || route.path === '/register'
})

// 判断是否为管理员
const isAdmin = computed(() => {
  return authStore.isAdmin
})

// 处理下拉菜单命令
const handleCommand = (command) => {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      // 使用auth store登出
      authStore.logout()
      ElMessage.success('已退出登录')

      // 跳转到登录页
      router.push('/login')
    }).catch(() => {
      // 用户取消操作
    })
  }
}

// 页面加载时检查登录状态并获取用户名
onMounted(() => {
  if (authStore.isAuthenticated && authStore.user) {
    username.value = authStore.user.name
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.sidebar {
  background-color: #304156;
}

.logo {
  padding: 20px;
  text-align: center;
  background-color: #263445;
  border-bottom: 1px solid #434a50;
}

.logo h3 {
  color: #fff;
  margin: 0;
}

.el-menu-vertical {
  border-right: none;
}

.el-menu-vertical .el-menu-item:hover {
  background-color: #434a50 !important;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 20px;
  display: flex;
  align-items: center;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.header-content h1 {
  margin: 0;
  color: #303133;
  font-size: 24px;
}

.user-info {
  display: flex;
  align-items: center;
}

.el-dropdown-link {
  cursor: pointer;
  color: #606266;
  display: flex;
  align-items: center;
}

.main-content {
  background-color: #f5f5f5;
  padding: 0;
}
</style>
