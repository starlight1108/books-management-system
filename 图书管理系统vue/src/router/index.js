import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BookList from '@/components/BookList.vue'
import MemberList from '@/components/MemberList.vue'
import BorrowList from '@/components/BorrowList.vue'
import Statistics from '@/components/Statistics.vue'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/books',
      name: 'Books',
      component: BookList,
      meta: { requiresAuth: true }
    },
    {
      path: '/members',
      name: 'Members',
      component: MemberList,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/borrows',
      name: 'Borrows',
      component: BorrowList,
      meta: { requiresAuth: true }
    },
    {
      path: '/statistics',
      name: 'Statistics',
      component: Statistics,
      meta: { requiresAuth: true, requiresAdmin: true }
    }
  ],
})

// 添加路由守卫，检查用户是否已登录
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 检查是否需要管理员权限的路由
  const requiresAdmin = to.meta.requiresAdmin || false

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // 如果需要登录但用户未登录，重定向到登录页
    next('/login')
  } else if (requiresAdmin && !authStore.isAdmin) {
    // 如果需要管理员权限但用户不是管理员，重定向到首页
    next('/books')
  } else if ((to.path === '/login' || to.path === '/register') && authStore.isAuthenticated) {
    // 如果用户已登录但访问登录/注册页，重定向到首页
    next('/books')
  } else {
    // 其他情况正常导航
    next()
  }
})

export default router
