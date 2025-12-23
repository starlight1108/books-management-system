<template>
  <div class="my-reviews">
    <div class="header">
      <h2>我的评论</h2>
    </div>

    <div class="reviews-list">
      <el-card>
        <div v-if="reviewStore.myReviews.length === 0" class="empty-reviews">
          <el-empty description="暂无评论" />
        </div>
        
        <div v-else>
          <div class="review-item" v-for="review in reviewStore.myReviews" :key="review.id">
            <div class="review-header">
              <div class="book-info">
                <h4 class="book-title">{{ review.book_title }}</h4>
                <span class="book-author">作者：{{ review.book_author }}</span>
              </div>
              <div class="review-meta">
                <el-rate v-model="review.rating" disabled size="small" />
                <span class="review-time">{{ formatTime(review.created_at) }}</span>
              </div>
            </div>
            
            <div class="review-content">
              {{ review.content }}
            </div>
            
            <div class="review-actions">
              <el-button type="primary" link @click="editReview(review)">编辑</el-button>
              <el-button type="danger" link @click="deleteReview(review)">删除</el-button>
              <el-button type="primary" link @click="viewBookDetail(review.book_id)">查看书籍</el-button>
            </div>
          </div>

          <!-- 分页 -->
          <div class="pagination">
            <el-pagination
              v-model:current-page="currentPage"
              :page-size="pageSize"
              :total="reviewStore.totalMyReviews"
              layout="total, prev, pager, next"
              @current-change="handlePageChange"
            />
          </div>
        </div>
      </el-card>
    </div>

    <!-- 编辑评论对话框 -->
    <el-dialog v-model="showEditDialog" title="编辑评论" width="500px">
      <el-form :model="editForm" :rules="reviewRules" ref="editFormRef">
        <el-form-item label="评分" prop="rating">
          <el-rate v-model="editForm.rating" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" />
        </el-form-item>
        <el-form-item label="评论内容" prop="content">
          <el-input
            v-model="editForm.content"
            type="textarea"
            :rows="4"
            placeholder="请输入您的评论..."
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showEditDialog = false">取消</el-button>
          <el-button type="primary" @click="submitEdit" :loading="editing">确认</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useReviewStore } from '@/stores/review'

const router = useRouter()
const reviewStore = useReviewStore()

const currentPage = ref(1)
const pageSize = ref(10)
const showEditDialog = ref(false)
const editing = ref(false)
const editingReview = ref(null)
const editFormRef = ref(null)

const editForm = reactive({
  rating: 0,
  content: ''
})

const reviewRules = {
  rating: [{ required: true, message: '请选择评分', trigger: 'change' }],
  content: [
    { required: true, message: '请输入评论内容', trigger: 'blur' },
    { min: 5, message: '评论内容至少5个字符', trigger: 'blur' }
  ]
}

// 获取我的评论列表
const fetchMyReviews = async () => {
  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value
    }
    await reviewStore.fetchMyReviews(params)
  } catch (error) {
    ElMessage.error('获取评论列表失败')
  }
}

// 编辑评论
const editReview = (review) => {
  editingReview.value = review
  editForm.rating = review.rating
  editForm.content = review.content
  showEditDialog.value = true
}

// 提交编辑
const submitEdit = async () => {
  if (!editFormRef.value) return

  await editFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        editing.value = true
        await reviewStore.updateReview(editingReview.value.id, editForm)
        ElMessage.success('评论修改成功')
        showEditDialog.value = false
        await fetchMyReviews()
      } catch (error) {
        ElMessage.error('评论修改失败')
      } finally {
        editing.value = false
      }
    }
  })
}

// 删除评论
const deleteReview = async (review) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条评论吗？',
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await reviewStore.deleteReview(review.id)
    ElMessage.success('评论删除成功')
    await fetchMyReviews()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 查看书籍详情
const viewBookDetail = (bookId) => {
  router.push(`/books/${bookId}`)
}

// 分页处理
const handlePageChange = (page) => {
  currentPage.value = page
  fetchMyReviews()
}

// 格式化时间
const formatTime = (timeString) => {
  return new Date(timeString).toLocaleString('zh-CN')
}

// 初始化
onMounted(async () => {
  await fetchMyReviews()
})
</script>

<style scoped>
.my-reviews {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  margin-bottom: 20px;
}

.reviews-list {
  margin-bottom: 20px;
}

.review-item {
  padding: 20px;
  border-bottom: 1px solid #eee;
  margin-bottom: 15px;
}

.review-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.book-info h4 {
  margin: 0 0 5px 0;
  color: #333;
}

.book-author {
  color: #666;
  font-size: 14px;
}

.review-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
}

.review-time {
  color: #999;
  font-size: 12px;
}

.review-content {
  line-height: 1.6;
  color: #333;
  margin-bottom: 10px;
}

.review-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.empty-reviews {
  padding: 40px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>