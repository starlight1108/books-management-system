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
        <el-form-item prop="name">
          <el-input
            v-model="loginData.name"
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
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const loginForm = ref(null)
const loading = ref(false)

const loginData = reactive({
  name: '',
  password: ''
})

const loginRules = {
  name: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

const handleLogin = () => {
  if (!loginForm.value) {
    console.error('Login form reference is null')
    return
  }

  loginForm.value.validate(async (valid) => {
    if (valid) {
      loading.value = true

      // 使用auth store进行登录
      const result = await authStore.login(loginData)
      loading.value = false

      if (result.success) {
        // 登录成功
        ElMessage.success('登录成功')

        // 根据用户角色跳转到不同页面
        if (authStore.isAdmin) {
          router.push('/members')  // 管理员跳转到会员管理
        } else {
          router.push('/books')    // 普通用户跳转到图书列表
        }
      } else {
        // 登录失败
        ElMessage.error(result.message)
      }
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
  padding: 40px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  color: #333;
  margin-bottom: 10px;
}

.login-header p {
  color: #666;
  font-size: 14px;
}

.login-form {
  margin-top: 20px;
}

.login-form .el-form-item {
  margin-bottom: 20px;
}

.login-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.login-footer .el-link {
  margin-left: 5px;
}
</style>