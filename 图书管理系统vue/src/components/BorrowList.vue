<template>
  <div class="borrow-list">
    <div class="header">
      <h2>{{ authStore.isAdmin ? '借阅管理' : '借阅历史' }}</h2>
      <!-- 只有管理员可以新增借阅 -->
      <el-button v-if="authStore.isAdmin" type="primary" @click="showBorrowDialog = true">
        <el-icon><Plus /></el-icon>
        新增借阅
      </el-button>
    </div>

    <el-table :data="borrowStore.borrows" style="width: 100%" v-loading="borrowStore.loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="book_title" label="书名" min-width="200" show-overflow-tooltip />
      <el-table-column prop="member_name" label="借阅人" width="120" />
      <el-table-column prop="borrow_date" label="借阅日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.borrow_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="due_date" label="应还日期" width="120">
        <template #default="{ row }">
          <span :class="{ 'overdue': isOverdue(row.due_date) && row.status === 'borrowed' }">
            {{ formatDate(row.due_date) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="return_date" label="归还日期" width="120">
        <template #default="{ row }">
          {{ row.return_date ? formatDate(row.return_date) : '-' }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'borrowed' ? 'warning' : 'success'">
            {{ row.status === 'borrowed' ? '借阅中' : '已归还' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-button
            v-if="row.status === 'borrowed'"
            type="primary"
            link
            @click="returnBook(row)"
          >
            归还
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增借阅对话框 -->
    <el-dialog
      v-model="showBorrowDialog"
      title="新增借阅"
      width="500px"
    >
      <el-form :model="borrowForm" :rules="rules" ref="borrowFormRef" label-width="100px">
        <el-form-item label="选择图书" prop="book_id">
          <el-select
            v-model="borrowForm.book_id"
            placeholder="请选择图书"
            filterable
            remote
            :remote-method="searchBooks"
            :loading="bookLoading"
          >
            <el-option
              v-for="book in availableBooks"
              :key="book.id"
              :label="`${book.title} - ${book.author}`"
              :value="book.id"
              :disabled="book.available_copies === 0"
            >
              <span style="float: left">{{ book.title }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">
                可借: {{ book.available_copies }}
              </span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="选择会员" prop="member_id">
          <el-select
            v-model="borrowForm.member_id"
            placeholder="请选择会员"
            filterable
            remote
            :remote-method="searchMembers"
            :loading="memberLoading"
          >
            <el-option
              v-for="member in members"
              :key="member.id"
              :label="member.name"
              :value="member.id"
              :disabled="member.status !== 'active'"
            >
              <span style="float: left">{{ member.name }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">
                {{ member.status === 'active' ? '正常' : '停用' }}
              </span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="应还日期" prop="due_date">
          <el-date-picker
            v-model="borrowForm.due_date"
            type="date"
            placeholder="选择应还日期"
            :disabled-date="disabledDate"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showBorrowDialog = false">取消</el-button>
        <el-button type="primary" @click="submitBorrow">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useBorrowStore } from '@/stores/borrow'
import { useBookStore } from '@/stores/book'
import { useMemberStore } from '@/stores/member'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const borrowStore = useBorrowStore()
const bookStore = useBookStore()
const memberStore = useMemberStore()
const authStore = useAuthStore()

const showBorrowDialog = ref(false)
const borrowFormRef = ref(null)
const bookLoading = ref(false)
const memberLoading = ref(false)
const availableBooks = ref([])
const members = ref([])

const borrowForm = reactive({
  book_id: '',
  member_id: '',
  due_date: ''
})

const rules = {
  book_id: [{ required: true, message: '请选择图书', trigger: 'change' }],
  member_id: [{ required: true, message: '请选择会员', trigger: 'change' }],
  due_date: [{ required: true, message: '请选择应还日期', trigger: 'change' }]
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const isOverdue = (dueDate) => {
  return new Date(dueDate) < new Date()
}

const disabledDate = (date) => {
  return date < new Date()
}

const searchBooks = async (query) => {
  if (!query) {
    availableBooks.value = []
    return
  }
  
  bookLoading.value = true
  try {
    const response = await api.getBooks({ search: query })
    availableBooks.value = response.data.books.filter(book => book.available_copies > 0)
  } catch (error) {
    console.error('搜索图书失败:', error)
  } finally {
    bookLoading.value = false
  }
}

const searchMembers = async (query) => {
  if (!query) {
    members.value = []
    return
  }
  
  memberLoading.value = true
  try {
    const response = await api.getMembers()
    members.value = response.data.filter(member => 
      member.name.toLowerCase().includes(query.toLowerCase())
    )
  } catch (error) {
    console.error('搜索会员失败:', error)
  } finally {
    memberLoading.value = false
  }
}

const returnBook = async (borrow) => {
  try {
    await borrowStore.returnBook(borrow.id)
    ElMessage.success('归还成功')
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '归还失败')
  }
}

const submitBorrow = async () => {
  try {
    await borrowFormRef.value.validate()
    
    const borrowData = {
      book_id: borrowForm.book_id,
      member_id: borrowForm.member_id,
      due_date: borrowForm.due_date.toISOString().split('T')[0]
    }
    
    await borrowStore.borrowBook(borrowData)
    ElMessage.success('借阅成功')
    showBorrowDialog.value = false
    resetForm()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '借阅失败')
  }
}

const resetForm = () => {
  Object.assign(borrowForm, {
    book_id: '',
    member_id: '',
    due_date: ''
  })
  availableBooks.value = []
  members.value = []
  borrowFormRef.value?.clearValidate()
}

onMounted(() => {
  borrowStore.fetchBorrows()
})
</script>

<style scoped>
.borrow-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.overdue {
  color: #f56c6c;
  font-weight: bold;
}
</style>