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
        <el-form-item prop="name">
          <el-input 
            v-model="registerData.name" 
            placeholder="姓名"
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
          <div class="password-tip">
            密码必须至少6位数字
          </div>
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
import { User, Lock, Phone } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const registerForm = ref(null)
const loading = ref(false)

const registerData = reactive({
  name: '',
  password: '',
  confirmPassword: '',
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

// 验证密码强度
const validatePassword = (rule, value, callback) => {
  // 至少6位数字
  const passwordRegex = /^\d{6,}$/
  if (!passwordRegex.test(value)) {
    callback(new Error('密码必须至少6位数字'))
  } else {
    callback()
  }
}

// 验证手机号格式
const validatePhone = (rule, value, callback) => {
  if (!value) {
    callback() // 手机号不是必填项
  } else {
    const phoneRegex = /^1[3456789]\d{9}$/
    if (!phoneRegex.test(value)) {
      callback(new Error('请输入正确的手机号格式'))
    } else {
      callback()
    }
  }
}

const registerRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ],
  phone: [
    { validator: validatePhone, trigger: 'blur' }
  ]
}

const authStore = useAuthStore()

const handleRegister = () => {
  registerForm.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      
      // 使用auth store进行注册
      const result = await authStore.register({
        name: registerData.name,
        password: registerData.password,
        phone: registerData.phone
      })
      
      loading.value = false
      
      if (result.success) {
        // 注册成功
        ElMessage.success('注册成功')
        
        // 跳转到主页
        router.push('/books')
      } else {
        // 注册失败
        ElMessage.error(result.message)
      }
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
  padding: 40px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
  color: #333;
  margin-bottom: 10px;
}

.register-header p {
  color: #666;
  font-size: 14px;
}

.register-form {
  margin-top: 20px;
}

.register-form .el-form-item {
  margin-bottom: 20px;
}

.password-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
  line-height: 1.2;
}

.register-footer {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.register-footer .el-link {
  margin-left: 5px;
}
</style>