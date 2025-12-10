import { createRouter, createWebHistory } from 'vue-router'
import BookList from '@/components/BookList.vue'
import MemberList from '@/components/MemberList.vue'
import BorrowList from '@/components/BorrowList.vue'
import Statistics from '@/components/Statistics.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/books'
    },
    {
      path: '/books',
      name: 'Books',
      component: BookList
    },
    {
      path: '/members',
      name: 'Members',
      component: MemberList
    },
    {
      path: '/borrows',
      name: 'Borrows',
      component: BorrowList
    },
    {
      path: '/statistics',
      name: 'Statistics',
      component: Statistics
    }
  ],
})

export default router