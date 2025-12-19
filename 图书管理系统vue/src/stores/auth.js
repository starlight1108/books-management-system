import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: false
  }),

  getters: {
    isAdmin: (state) => state.user && state.user.role === 'admin',
    currentUser: (state) => state.user
  },

  actions: {
    async login(credentials) {
      try {
        const response = await api.login(credentials)
        const { access_token, user } = response.data

        this.token = access_token
        this.user = user
        this.isAuthenticated = true

        // 保存到本地存储
        localStorage.setItem('token', access_token)
        localStorage.setItem('user', JSON.stringify(user))

        return { success: true }
      } catch (error) {
        console.error('登录失败:', error)
        return { 
          success: false, 
          message: error.response?.data?.error || '登录失败，请检查用户名和密码' 
        }
      }
    },

    async register(userData) {
      try {
        const response = await api.register(userData)
        const { access_token, user } = response.data

        this.token = access_token
        this.user = user
        this.isAuthenticated = true

        // 保存到本地存储
        localStorage.setItem('token', access_token)
        localStorage.setItem('user', JSON.stringify(user))

        return { success: true }
      } catch (error) {
        console.error('注册失败:', error)
        return { 
          success: false, 
          message: error.response?.data?.error || '注册失败，请稍后再试' 
        }
      }
    },

    logout() {
      this.token = null
      this.user = null
      this.isAuthenticated = false

      // 清除本地存储
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    // 初始化认证状态
    initAuth() {
      const token = localStorage.getItem('token')
      const userStr = localStorage.getItem('user')

      if (token && userStr) {
        try {
          this.token = token
          this.user = JSON.parse(userStr)
          this.isAuthenticated = true
        } catch (error) {
          console.error('解析用户信息失败:', error)
          this.logout()
        }
      }
    },

    // 获取用户资料
    async fetchProfile() {
      try {
        const response = await api.getProfile()
        this.user = response.data.user
        localStorage.setItem('user', JSON.stringify(this.user))
        return { success: true }
      } catch (error) {
        console.error('获取用户资料失败:', error)
        return { 
          success: false, 
          message: error.response?.data?.error || '获取用户资料失败' 
        }
      }
    },

    // 修改密码
    async changePassword(passwordData) {
      try {
        await api.changePassword(passwordData)
        return { success: true }
      } catch (error) {
        console.error('修改密码失败:', error)
        return { 
          success: false, 
          message: error.response?.data?.error || '修改密码失败' 
        }
      }
    }
  }
})
