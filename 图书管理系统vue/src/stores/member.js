import { defineStore } from 'pinia'
import api from '@/services/api'

export const useMemberStore = defineStore('member', {
  state: () => ({
    members: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchMembers() {
      this.loading = true
      this.error = null
      try {
        const response = await api.getMembers()
        // 后端返回的是包含分页信息的对象，需要提取members数组
        this.members = response.data.members || []
      } catch (error) {
        this.error = error.message
        console.error('获取会员列表失败:', error)
      } finally {
        this.loading = false
      }
    },

    async addMember(memberData) {
      try {
        const response = await api.addMember(memberData)
        await this.fetchMembers()
        return response.data
      } catch (error) {
        console.error('添加会员失败:', error)
        throw error
      }
    }
  }
})