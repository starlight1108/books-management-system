import { defineStore } from 'pinia'
import api from '@/services/api'

export const useStatisticsStore = defineStore('statistics', {
  state: () => ({
    statistics: {
      total_books: 0,
      total_members: 0,
      borrowed_books: 0,
      available_books: 0,
      overdue_books: 0
    },
    loading: false,
    error: null
  }),

  actions: {
    async fetchStatistics() {
      this.loading = true
      this.error = null
      try {
        const response = await api.getStatistics()
        this.statistics = response.data
      } catch (error) {
        this.error = error.message
        console.error('获取统计信息失败:', error)
      } finally {
        this.loading = false
      }
    }
  }
})