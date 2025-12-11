<template>
  <div class="register-container">
    <div class="register-box">
      <div class="register-header">
        <h2>图书管理系统</h2>
        <p>用户注册</p>
      </div>
      
      <el-form 
        ref="registerForm" 
        :model="registerData" 
        :rules="registerRules" 
        label-width="0"
        class="register-form"
      >
        <el-form-item prop="username">
          <el-input 
            v-model="registerData.username" 
            placeholder="用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="registerData.password" 
            type="password" 
            placeholder="密码"
            prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input 
            v-model="registerData.confirmPassword" 
            type="password" 
            placeholder="确认密码"
            prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="email">
          <el-input 
            v-model="registerData.email" 
            placeholder="电子邮箱"
            prefix-icon="Message"
            size="large"
          />
        </el-form-item>
        
        <el-form-item prop="phone">
          <el-input 
            v-model="registerData.phone" 
            placeholder="手机号码"
            prefix-icon="Phone"
            size="large"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            size="large" 
            style="width: 100%"
            :loading="loading"
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>
        
        <div class="register-footer">
          <span>已有账号？</span>
          <el-link type="primary" @click="goToLogin">立即登录</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message, Phone } from '@element-plus/icons-vue'

const router = useRouter()
const registerForm = ref(null)
const loading = ref(false)

const registerData = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  phone: ''
})

// 验证确认密码是否一致
const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerData.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 验证邮箱格式
const validateEmail = (rule, value, callback) => {
  const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  if (!emailRegex.test(value)) {
    callback(new Error('请输入正确的邮箱格式'))
  } else {
    callback()
  }
}

// 验证手机号格式
const validatePhone = (rule, value, callback) => {
  const phoneRegex = /^1[3456789]\d{9}$/
  if (!phoneRegex.test(value)) {
    callback(new Error('请输入正确的手机号格式'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入电子邮箱', trigger: 'blur' },
    { validator: validateEmail, trigger: 'blur' }
  ],
  phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { validator: validatePhone, trigger: 'blur' }
  ]
}

const handleRegister = () => {
  registerForm.value.validate((valid) => {
    if (valid) {
      loading.value = true
      
      // 这里应该调用API进行注册
      // 模拟注册过程
      setTimeout(() => {
        loading.value = false
        
        // 假设注册成功
        ElMessage.success('注册成功，请登录')
        
        // 跳转到登录页面
        router.push('/login')
      }, 1000)
    } else {
      return false
    }
  })
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-container {
  height: 100vh;
  background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-box {
  width: 400px;
  padding: 30px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 15px 35px rgba(50, 50, 93, 0.1), 0 5px 15px rgba(0, 0, 0, 0.07);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
  color: #303133;
  margin-bottom: 10px;
}

.register-header p {
  color: #909399;
  font-size: 14px;
}

.register-form {
  margin-top: 20px;
}

.register-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #606266;
}
</style>