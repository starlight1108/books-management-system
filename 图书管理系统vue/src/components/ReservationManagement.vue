<template>
  <div class="reservation-management">
    <div class="header">
      <h2>{{ authStore.isAdmin ? '预约管理' : '我的预约' }}</h2>
    </div>

    <!-- 搜索和筛选 -->
    <div class="search-bar">
      <el-select
        v-model="statusFilter"
        placeholder="选择状态"
        style="width: 150px; margin-right: 10px"
        clearable
      >
        <el-option label="待处理" value="pending" />
        <el-option label="已批准" value="approved" />
        <el-option label="已完成" value="completed" />
        <el-option label="已取消" value="cancelled" />
      </el-select>
      <el-button type="primary" @click="fetchReservations">筛选</el-button>
      <el-button @click="resetFilter">重置</el-button>
    </div>

    <!-- 预约列表 -->
    <el-table :data="reservations" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="book_title" label="图书名称" min-width="200" show-overflow-tooltip />
      <el-table-column v-if="authStore.isAdmin" prop="member_name" label="预约人" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="reservation_date" label="预约时间" width="180">
        <template #default="{ row }">
          {{ formatDateTime(row.reservation_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="expiry_date" label="过期时间" width="180">
        <template #default="{ row }">
          {{ formatDateTime(row.expiry_date) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <!-- 普通用户操作 -->
          <template v-if="!authStore.isAdmin">
            <el-button 
              v-if="row.status === 'pending'" 
              type="danger" 
              link 
              @click="cancelReservation(row)"
            >
              取消预约
            </el-button>
            <span v-else-if="row.status === 'completed'" class="completed-text">已完成借阅</span>
            <span v-else-if="row.status === 'cancelled'" class="cancelled-text">已取消</span>
          </template>
          
          <!-- 管理员操作 -->
          <template v-if="authStore.isAdmin">
            <el-button 
              v-if="row.status === 'pending'" 
              type="primary" 
              link 
              @click="approveReservation(row)"
              :disabled="row.book_available_copies <= 0"
            >
              批准预约
            </el-button>
            <el-button 
              v-if="row.status === 'pending'" 
              type="danger" 
              link 
              @click="cancelReservation(row)"
            >
              取消预约
            </el-button>
            <span v-if="row.status === 'completed'" class="completed-text">已完成</span>
            <span v-if="row.status === 'cancelled'" class="cancelled-text">已取消</span>
          </template>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="totalReservations"
        layout="total, prev, pager, next"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()

// 响应式数据
const reservations = ref([])
const loading = ref(false)
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const totalReservations = ref(0)

// 状态映射
const statusMap = {
  pending: { text: '待处理', type: 'warning' },
  approved: { text: '已批准', type: 'success' },
  completed: { text: '已完成', type: 'info' },
  cancelled: { text: '已取消', type: 'danger' }
}

// 获取预约列表
const fetchReservations = async () => {
  try {
    loading.value = true
    const params = {
      page: currentPage.value,
      per_page: pageSize.value
    }
    
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    
    // 根据用户角色选择不同的API方法
    const response = authStore.isAdmin 
      ? await api.getReservations(params)
      : await api.getMyReservations(params)
    
    reservations.value = response.data.reservations
    totalReservations.value = response.data.total
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '获取预约列表失败')
  } finally {
    loading.value = false
  }
}

// 批准预约
const approveReservation = async (reservation) => {
  try {
    await ElMessageBox.confirm(
      `确定要批准《${reservation.book_title}》的预约吗？`,
      '批准确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await api.approveReservation(reservation.id)
    
    ElMessage.success('预约已批准并完成借阅')
    fetchReservations()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.error || '批准预约失败')
    }
  }
}

// 取消预约
const cancelReservation = async (reservation) => {
  try {
    const message = authStore.isAdmin 
      ? `确定要取消《${reservation.book_title}》的预约吗？`
      : `确定要取消《${reservation.book_title}》的预约吗？`
    
    await ElMessageBox.confirm(
      message,
      '取消确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await api.cancelReservation(reservation.id)
    
    ElMessage.success('预约已取消')
    fetchReservations()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.error || '取消预约失败')
    }
  }
}



// 工具函数
const getStatusType = (status) => statusMap[status]?.type || 'info'
const getStatusText = (status) => statusMap[status]?.text || status

const formatDateTime = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchReservations()
}

const resetFilter = () => {
  statusFilter.value = ''
  currentPage.value = 1
  fetchReservations()
}

// 初始化
onMounted(() => {
  fetchReservations()
})
</script>

<style scoped>
.reservation-management {
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

.completed-text {
  color: #67c23a;
  font-size: 14px;
}

.cancelled-text {
  color: #f56c6c;
  font-size: 14px;
}

.rating-bar {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.star-label {
  width: 40px;
  font-size: 14px;
}

.rating-progress {
  flex: 1;
  margin: 0 10px;
}

.count {
  width: 30px;
  text-align: right;
  font-size: 14px;
}
</style>