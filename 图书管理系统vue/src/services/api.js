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
    // 从localStorage获取token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
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

    // 如果是401错误，可能是token过期，清除本地存储并跳转到登录页
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }

    return Promise.reject(error)
  }
)

export default {
  // 认证
  login(credentials) {
    return api.post('/auth/login', credentials)
  },

  register(userData) {
    return api.post('/auth/register', userData)
  },

  getProfile() {
    return api.get('/auth/profile')
  },

  changePassword(passwordData) {
    return api.post('/auth/change-password', passwordData)
  },

  // 图书管理
  getBooks(params = {}) {
    return api.get('/books', { params })
  },
  
  getBookDetail(bookId) {
    return api.get(`/books/${bookId}`)
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
  
  updateMember(memberId, memberData) {
    return api.put(`/members/${memberId}`, memberData)
  },
  
  deleteMember(memberId) {
    return api.delete(`/members/${memberId}`)
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
  },

  // 评论管理
  getBookReviews(bookId, params = {}) {
    return api.get(`/books/${bookId}/reviews`, { params })
  },
  
  addReview(bookId, reviewData) {
    return api.post(`/books/${bookId}/reviews`, reviewData)
  },
  
  updateReview(reviewId, reviewData) {
    return api.put(`/reviews/${reviewId}`, reviewData)
  },
  
  deleteReview(reviewId) {
    return api.delete(`/reviews/${reviewId}`)
  },
  
  getMyReviews(params = {}) {
    return api.get('/reviews/my-reviews', { params })
  },
  
  // 预约管理
  createReservation(reservationData) {
    return api.post('/reservations', reservationData)
  },
  
  getMyReservations(params = {}) {
    return api.get('/reservations/my-reservations', { params })
  },
  
  getReservations(params = {}) {
    return api.get('/reservations', { params })
  },
  
  approveReservation(reservationId) {
    return api.put(`/reservations/${reservationId}/approve`)
  },
  
  cancelReservation(reservationId) {
    return api.put(`/reservations/${reservationId}/cancel`)
  }
}