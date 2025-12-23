import { defineStore } from 'pinia'
import api from '@/services/api'

export const useBookStore = defineStore('book', {
  state: () => ({
    books: [],
    currentBook: null,
    currentPage: 1,
    totalPages: 1,
    totalBooks: 0,
    loading: false,
    error: null
  }),

  actions: {
    async fetchBooks(params = {}) {
      this.loading = true
      this.error = null
      try {
        const response = await api.getBooks(params)
        const data = response.data
        this.books = data.books
        this.currentPage = data.current_page
        this.totalPages = data.pages
        this.totalBooks = data.total
      } catch (error) {
        this.error = error.message
        console.error('获取图书列表失败:', error)
      } finally {
        this.loading = false
      }
    },

    async addBook(bookData) {
      try {
        const response = await api.addBook(bookData)
        await this.fetchBooks()
        return response.data
      } catch (error) {
        console.error('添加图书失败:', error)
        throw error
      }
    },

    async updateBook(bookId, bookData) {
      try {
        const response = await api.updateBook(bookId, bookData)
        await this.fetchBooks()
        return response.data
      } catch (error) {
        console.error('更新图书失败:', error)
        throw error
      }
    },

    async deleteBook(bookId) {
      try {
        const response = await api.deleteBook(bookId)
        await this.fetchBooks()
        return response.data
      } catch (error) {
        console.error('删除图书失败:', error)
        throw error
      }
    },

    async fetchBookDetail(bookId) {
      this.loading = true
      this.error = null
      try {
        const response = await api.getBookDetail(bookId)
        this.currentBook = response.data
        return response.data
      } catch (error) {
        this.error = error.message
        console.error('获取图书详情失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})