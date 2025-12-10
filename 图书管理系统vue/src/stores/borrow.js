import { defineStore } from 'pinia'
import api from '@/services/api'

export const useBorrowStore = defineStore('borrow', {
  state: () => ({
    borrows: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchBorrows() {
      this.loading = true
      this.error = null
      try {
        const response = await api.getBorrows()
        // 后端返回的是包含分页信息的对象，需要提取borrows数组
        this.borrows = response.data.borrows || []
      } catch (error) {
        this.error = error.message
        console.error('获取借阅记录失败:', error)
      } finally {
        this.loading = false
      }
    },

    async borrowBook(borrowData) {
      try {
        const response = await api.borrowBook(borrowData)
        await this.fetchBorrows()
        return response.data
      } catch (error) {
        console.error('借阅图书失败:', error)
        throw error
      }
    },

    async returnBook(borrowId) {
      try {
        const response = await api.returnBook(borrowId)
        await this.fetchBorrows()
        return response.data
      } catch (error) {
        console.error('归还图书失败:', error)
        throw error
      }
    }
  }
})