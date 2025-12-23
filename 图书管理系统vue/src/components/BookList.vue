<template>
  <div class="book-list">
    <div class="header">
      <h2>{{ authStore.isAdmin ? '图书管理' : '图书' }}</h2>
      <!-- 只有管理员可以添加图书 -->
      <el-button v-if="authStore.isAdmin" type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        添加图书
      </el-button>
    </div>

    <div class="search-bar">
      <el-input
        v-model="searchQuery"
        placeholder="搜索图书标题或作者"
        style="width: 300px; margin-right: 10px"
        @keyup.enter="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      <el-select
        v-model="categoryFilter"
        placeholder="选择分类"
        style="width: 150px; margin-right: 10px"
        clearable
      >
        <el-option label="文学" value="文学" />
        <el-option label="科技" value="科技" />
        <el-option label="历史" value="历史" />
        <el-option label="教育" value="教育" />
        <el-option label="其他" value="其他" />
      </el-select>
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button @click="resetSearch">重置</el-button>
    </div>

    <el-table :data="bookStore.books" style="width: 100%" v-loading="bookStore.loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="书名" min-width="200" show-overflow-tooltip>
        <template #default="{ row }">
          <el-button type="primary" link @click="viewBookDetail(row)">{{ row.title }}</el-button>
        </template>
      </el-table-column>
      <el-table-column prop="author" label="作者" width="120" />
      <el-table-column prop="isbn" label="ISBN" width="130" />
      <el-table-column prop="category" label="分类" width="80" />
      <el-table-column prop="total_copies" label="总册数" width="80" align="center" />
      <el-table-column prop="available_copies" label="可借册数" width="90" align="center" />
      <el-table-column prop="publisher" label="出版社" width="150" show-overflow-tooltip />
      <!-- 操作列 -->
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="viewBookDetail(row)">查看详情</el-button>
          <!-- 只有管理员才能看到编辑和删除按钮 -->
          <el-button v-if="authStore.isAdmin" type="primary" link @click="editBook(row)">编辑</el-button>
          <el-button v-if="authStore.isAdmin" type="danger" link @click="deleteBook(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="bookStore.totalBooks"
        layout="total, prev, pager, next"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 添加/编辑图书对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="editingBook ? '编辑图书' : '添加图书'"
      width="600px"
    >
      <el-form :model="bookForm" :rules="rules" ref="bookFormRef" label-width="80px">
        <el-form-item label="书名" prop="title">
          <el-input v-model="bookForm.title" placeholder="请输入书名" />
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="bookForm.author" placeholder="请输入作者" />
        </el-form-item>
        <el-form-item label="ISBN">
          <el-input v-model="bookForm.isbn" placeholder="请输入ISBN" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="bookForm.category" placeholder="请选择分类">
            <el-option label="文学" value="文学" />
            <el-option label="科技" value="科技" />
            <el-option label="历史" value="历史" />
            <el-option label="教育" value="教育" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="出版社">
          <el-input v-model="bookForm.publisher" placeholder="请输入出版社" />
        </el-form-item>
        <el-form-item label="总册数" prop="total_copies">
          <el-input-number v-model="bookForm.total_copies" :min="1" :max="999" />
        </el-form-item>
        <el-form-item label="位置信息">
          <el-input v-model="bookForm.location" placeholder="请输入图书位置信息（如：A区3排2号架）" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="bookForm.description"
            type="textarea"
            placeholder="请输入图书描述"
            :rows="4"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确认</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { useBookStore } from '@/stores/book'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const bookStore = useBookStore()
const authStore = useAuthStore()

const searchQuery = ref('')
const categoryFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const showAddDialog = ref(false)
const editingBook = ref(null)
const bookFormRef = ref(null)

const bookForm = reactive({
  title: '',
  author: '',
  isbn: '',
  category: '',
  publisher: '',
  total_copies: 1,
  location: '',
  description: ''
})

const rules = {
  title: [{ required: true, message: '请输入书名', trigger: 'blur' }],
  author: [{ required: true, message: '请输入作者', trigger: 'blur' }],
  total_copies: [{ required: true, message: '请输入总册数', trigger: 'blur' }]
}

const fetchBooks = async () => {
  const params = {
    page: currentPage.value,
    per_page: pageSize.value
  }
  if (searchQuery.value) {
    params.search = searchQuery.value
  }
  if (categoryFilter.value) {
    params.category = categoryFilter.value
  }
  await bookStore.fetchBooks(params)
}

const handleSearch = () => {
  currentPage.value = 1
  fetchBooks()
}

const resetSearch = () => {
  searchQuery.value = ''
  categoryFilter.value = ''
  currentPage.value = 1
  fetchBooks()
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchBooks()
}

const editBook = (book) => {
  editingBook.value = book
  Object.assign(bookForm, {
    title: book.title,
    author: book.author,
    isbn: book.isbn || '',
    category: book.category || '',
    publisher: book.publisher || '',
    total_copies: book.total_copies,
    location: book.location || '',
    description: book.description || ''
  })
  showAddDialog.value = true
}

const viewBookDetail = (book) => {
  router.push(`/books/${book.id}`)
}

const deleteBook = async (book) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除图书《${book.title}》吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await bookStore.deleteBook(book.id)
    ElMessage.success('删除成功')
    fetchBooks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const submitForm = async () => {
  if (!bookFormRef.value) return
  
  await bookFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (editingBook.value) {
          // 更新图书
          await bookStore.updateBook(editingBook.value.id, bookForm)
          ElMessage.success('更新成功')
        } else {
          // 添加图书
          await bookStore.addBook(bookForm)
          ElMessage.success('添加成功')
        }
        showAddDialog.value = false
        fetchBooks()
        
        // 重置表单
        Object.assign(bookForm, {
          title: '',
          author: '',
          isbn: '',
          category: '',
          publisher: '',
          total_copies: 1,
          location: '',
          description: ''
        })
        editingBook.value = null
      } catch (error) {
        ElMessage.error(editingBook.value ? '更新失败' : '添加失败')
      }
    }
  })
}

// 初始化时加载数据
onMounted(() => {
  fetchBooks()
})
</script>

<style scoped>
.book-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  margin-bottom: 20px;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>