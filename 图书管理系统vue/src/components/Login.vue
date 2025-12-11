<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>图书管理系统</h2>
        <p>用户登录</p>
      </div>
      
      <el-form 
        ref="loginForm" 
        :model="loginData" 
        :rules="loginRules" 
        label-width="0"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input 
            v-model="loginData.username" 
            placeholder="用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="loginData.password" 
            type="password" 
            placeholder="密码"
            prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            size="large" 
            style="width: 100%"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
        
        <div class="login-footer">
          <span>还没有账号？</span>
          <el-link type="primary" @click="goToRegister">立即注册</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const loginForm = ref(null)
const loading = ref(false)

const loginData = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

const handleLogin = () => {
  loginForm.value.validate((valid) => {
    if (valid) {
      loading.value = true
      
      // 这里应该调用API进行登录验证
      // 模拟登录过程
      setTimeout(() => {
        loading.value = false
        
        // 假设登录成功
        ElMessage.success('登录成功')
        
        // 保存登录状态到localStorage
        localStorage.setItem('isLogin', 'true')
        localStorage.setItem('username', loginData.username)
        
        // 跳转到主页
        router.push('/books')
      }, 1000)
    } else {
      return false
    }
  })
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-box {
  width: 400px;
  padding: 30px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 15px 35px rgba(50, 50, 93, 0.1), 0 5px 15px rgba(0, 0, 0, 0.07);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  color: #303133;
  margin-bottom: 10px;
}

.login-header p {
  color: #909399;
  font-size: 14px;
}

.login-form {
  margin-top: 20px;
}

.login-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #606266;
}
</style>