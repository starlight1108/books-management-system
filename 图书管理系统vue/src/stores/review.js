import { defineStore } from 'pinia'
import api from '@/services/api'

export const useReviewStore = defineStore('review', {
  state: () => ({
    reviews: [],
    currentBookReviews: [],
    myReviews: [],
    loading: false,
    totalReviews: 0,
    currentPage: 1,
    pageSize: 10,
    averageRating: 0,
    ratingCounts: {}
  }),

  actions: {
    // 获取书籍评论列表
    async fetchBookReviews(bookId, params = {}) {
      try {
        this.loading = true
        const response = await api.getBookReviews(bookId, params)
        this.currentBookReviews = response.data.reviews
        this.totalReviews = response.data.total
        this.averageRating = response.data.average_rating
        this.ratingCounts = response.data.rating_counts
        return response.data
      } catch (error) {
        console.error('获取评论失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 添加评论
    async addReview(bookId, reviewData) {
      try {
        const response = await api.addReview(bookId, reviewData)
        // 添加成功后，重新获取评论列表
        await this.fetchBookReviews(bookId)
        return response.data
      } catch (error) {
        console.error('添加评论失败:', error)
        throw error
      }
    },

    // 更新评论
    async updateReview(reviewId, reviewData) {
      try {
        const response = await api.updateReview(reviewId, reviewData)
        return response.data
      } catch (error) {
        console.error('更新评论失败:', error)
        throw error
      }
    },

    // 删除评论
    async deleteReview(reviewId) {
      try {
        await api.deleteReview(reviewId)
        // 从当前评论列表中移除
        this.currentBookReviews = this.currentBookReviews.filter(review => review.id !== reviewId)
        this.myReviews = this.myReviews.filter(review => review.id !== reviewId)
        this.totalReviews -= 1
      } catch (error) {
        console.error('删除评论失败:', error)
        throw error
      }
    },

    // 获取我的评论
    async fetchMyReviews(params = {}) {
      try {
        this.loading = true
        const response = await api.getMyReviews(params)
        this.myReviews = response.data.reviews
        this.totalReviews = response.data.total
        return response.data
      } catch (error) {
        console.error('获取我的评论失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 清空当前书籍评论
    clearCurrentBookReviews() {
      this.currentBookReviews = []
      this.averageRating = 0
      this.ratingCounts = {}
    }
  }
})