<template>
  <div id="app">
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
          <el-menu-item index="/members">
            <el-icon><User /></el-icon>
            <span>会员管理</span>
          </el-menu-item>
          <el-menu-item index="/borrows">
            <el-icon><Document /></el-icon>
            <span>借阅管理</span>
          </el-menu-item>
          <el-menu-item index="/statistics">
            <el-icon><TrendCharts /></el-icon>
            <span>统计概览</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header class="header">
          <div class="header-content">
            <h1>{{ $route.name }}</h1>
          </div>
        </el-header>
        
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { Reading, User, Document, TrendCharts } from '@element-plus/icons-vue'
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

.header-content h1 {
  margin: 0;
  color: #303133;
  font-size: 24px;
}

.main-content {
  background-color: #f5f5f5;
  padding: 0;
}
</style>