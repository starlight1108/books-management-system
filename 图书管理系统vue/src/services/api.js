import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default {
  // 图书管理
  getBooks(params = {}) {
    return api.get('/books', { params })
  },
  
  addBook(bookData) {
    return api.post('/books', bookData)
  },
  
  updateBook(bookId, bookData) {
    return api.put(`/books/${bookId}`, bookData)
  },
  
  deleteBook(bookId) {
    return api.delete(`/books/${bookId}`)
  },
  
  // 会员管理
  getMembers() {
    return api.get('/members')
  },
  
  addMember(memberData) {
    return api.post('/members', memberData)
  },
  
  // 借阅管理
  getBorrows() {
    return api.get('/borrows')
  },
  
  borrowBook(borrowData) {
    return api.post('/borrows', borrowData)
  },
  
  returnBook(borrowId) {
    return api.put(`/borrows/${borrowId}/return`)
  },
  
  // 统计信息
  getStatistics() {
    return api.get('/statistics')
  }
}