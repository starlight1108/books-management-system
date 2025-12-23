<template>
  <div class="book-detail">
    <div class="header">
      <el-button type="primary" link @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h2>书籍详情</h2>
    </div>

    <div class="book-info" v-if="book">
      <el-card>
        <div class="book-header">
          <h3>{{ book.title }}</h3>
          <div class="book-meta">
            <span class="rating-info">
              <el-rate v-model="reviewStore.averageRating" disabled show-score text-color="#ff9900" />
              <span class="rating-text">({{ reviewStore.totalReviews }} 条评论)</span>
            </span>
          </div>
        </div>
        
        <div class="book-details">
          <div class="detail-row">
            <span class="label">作者：</span>
            <span class="value">{{ book.author }}</span>
          </div>
          <div class="detail-row">
            <span class="label">ISBN：</span>
            <span class="value">{{ book.isbn }}</span>
          </div>
          <div class="detail-row">
            <span class="label">出版社：</span>
            <span class="value">{{ book.publisher || '未知' }}</span>
          </div>
          <div class="detail-row">
            <span class="label">分类：</span>
            <span class="value">{{ book.category || '未分类' }}</span>
          </div>
          <div class="detail-row">
            <span class="label">总册数：</span>
            <span class="value">{{ book.total_copies }}</span>
          </div>
          <div class="detail-row">
            <span class="label">可借册数：</span>
            <span class="value">{{ book.available_copies }}</span>
          </div>
          <div class="detail-row" v-if="book.location">
            <span class="label">位置：</span>
            <span class="value">{{ book.location }}</span>
          </div>
          <div class="detail-row" v-if="book.description">
            <span class="label">描述：</span>
            <span class="value">{{ book.description }}</span>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 评论统计 -->
    <div class="rating-statistics" v-if="reviewStore.ratingCounts">
      <el-card header="评分统计">
        <div class="rating-bars">
          <div class="rating-bar" v-for="i in 5" :key="i">
            <span class="star-label">{{ 6-i }}星</span>
            <el-progress 
              :percentage="getRatingPercentage(6-i)" 
              :show-text="false" 
              :stroke-width="8"
              class="rating-progress"
            />
            <span class="count">{{ reviewStore.ratingCounts[6-i] || 0 }}</span>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 添加评论 -->
    <div class="add-review" v-if="authStore.isAuthenticated">
      <el-card header="发表评论">
        <el-form :model="reviewForm" :rules="reviewRules" ref="reviewFormRef">
          <el-form-item label="评分" prop="rating">
            <el-rate v-model="reviewForm.rating" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" />
          </el-form-item>
          <el-form-item label="评论内容" prop="content">
            <el-input
              v-model="reviewForm.content"
              type="textarea"
              :rows="4"
              placeholder="请输入您的评论..."
              maxlength="500"
              show-word-limit
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitReview" :loading="submitting">
              发表评论
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>

    <!-- 评论列表 -->
    <div class="reviews-list">
      <el-card header="评论列表">
        <div v-if="reviewStore.currentBookReviews.length === 0" class="empty-reviews">
          <el-empty description="暂无评论" />
        </div>
        
        <div v-else>
          <div class="review-item" v-for="review in reviewStore.currentBookReviews" :key="review.id">
            <div class="review-header">
              <div class="reviewer-info">
                <span class="reviewer-name">{{ review.member_name }}</span>
                <el-rate v-model="review.rating" disabled size="small" />
                <span class="review-time">{{ formatTime(review.created_at) }}</span>
              </div>
              <div class="review-actions" v-if="authStore.user?.id === review.member_id || authStore.isAdmin">
                <el-button type="primary" link @click="editReview(review)">编辑</el-button>
                <el-button type="danger" link @click="deleteReview(review)">删除</el-button>
              </div>
            </div>
            <div class="review-content">
              {{ review.content }}
            </div>
          </div>

          <!-- 分页 -->
          <div class="pagination">
            <el-pagination
              v-model:current-page="reviewStore.currentPage"
              :page-size="reviewStore.pageSize"
              :total="reviewStore.totalReviews"
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft } from '@element-plus/icons-vue'
import { useBookStore } from '@/stores/book'
import { useReviewStore } from '@/stores/review'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const bookStore = useBookStore()
const reviewStore = useReviewStore()
const authStore = useAuthStore()

const bookId = computed(() => parseInt(route.params.id))
const book = computed(() => bookStore.currentBook)

const reviewFormRef = ref(null)
const editFormRef = ref(null)
const showEditDialog = ref(false)
const submitting = ref(false)
const editing = ref(false)
const editingReview = ref(null)

const reviewForm = reactive({
  rating: 5,
  content: ''
})

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

// 获取书籍详情
const fetchBookDetail = async () => {
  try {
    await bookStore.fetchBookDetail(bookId.value)
  } catch (error) {
    ElMessage.error('获取书籍详情失败')
    router.push('/books')
  }
}

// 获取评论列表
const fetchReviews = async () => {
  try {
    const params = {
      page: reviewStore.currentPage,
      per_page: reviewStore.pageSize
    }
    await reviewStore.fetchBookReviews(bookId.value, params)
  } catch (error) {
    ElMessage.error('获取评论失败')
  }
}

// 提交评论
const submitReview = async () => {
  if (!reviewFormRef.value) return

  await reviewFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        submitting.value = true
        await reviewStore.addReview(bookId.value, reviewForm)
        ElMessage.success('评论发表成功')
        
        // 清空表单
        reviewForm.rating = 5
        reviewForm.content = ''
        reviewFormRef.value.resetFields()
      } catch (error) {
        ElMessage.error(error.response?.data?.error || '评论发表失败')
      } finally {
        submitting.value = false
      }
    }
  })
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
        await fetchReviews()
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
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 分页处理
const handlePageChange = (page) => {
  reviewStore.currentPage = page
  fetchReviews()
}

// 计算评分百分比
const getRatingPercentage = (rating) => {
  const total = Object.values(reviewStore.ratingCounts).reduce((sum, count) => sum + count, 0)
  const count = reviewStore.ratingCounts[rating] || 0
  return total > 0 ? Math.round((count / total) * 100) : 0
}

// 格式化时间
const formatTime = (timeString) => {
  return new Date(timeString).toLocaleString('zh-CN')
}

// 初始化
onMounted(async () => {
  await fetchBookDetail()
  await fetchReviews()
})

// 组件卸载时清空评论数据
import { onUnmounted } from 'vue'
onUnmounted(() => {
  reviewStore.clearCurrentBookReviews()
})
</script>

<style scoped>
.book-detail {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0 0 0 10px;
}

.book-info {
  margin-bottom: 20px;
}

.book-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.rating-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rating-text {
  color: #666;
  font-size: 14px;
}

.book-details {
  display: grid;
  gap: 10px;
}

.detail-row {
  display: flex;
  align-items: center;
}

.label {
  font-weight: bold;
  min-width: 80px;
  color: #666;
}

.value {
  color: #333;
}

.rating-statistics {
  margin-bottom: 20px;
}

.rating-bars {
  display: grid;
  gap: 10px;
}

.rating-bar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.star-label {
  min-width: 40px;
  font-size: 14px;
}

.rating-progress {
  flex: 1;
}

.count {
  min-width: 30px;
  text-align: right;
  font-size: 14px;
  color: #666;
}

.add-review {
  margin-bottom: 20px;
}

.reviews-list {
  margin-bottom: 20px;
}

.review-item {
  padding: 15px 0;
  border-bottom: 1px solid #eee;
}

.review-item:last-child {
  border-bottom: none;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.reviewer-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.reviewer-name {
  font-weight: bold;
}

.review-time {
  color: #999;
  font-size: 12px;
}

.review-actions {
  display: flex;
  gap: 10px;
}

.review-content {
  line-height: 1.6;
  color: #333;
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