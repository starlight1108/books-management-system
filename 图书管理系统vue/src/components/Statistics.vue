<template>
  <div class="statistics">
    <h2>统计概览</h2>
    
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon book-icon">
              <el-icon><Reading /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ statisticsStore.statistics.total_books }}</div>
              <div class="stat-label">图书总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon member-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ statisticsStore.statistics.total_members }}</div>
              <div class="stat-label">会员总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon borrowed-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ statisticsStore.statistics.borrowed_books }}</div>
              <div class="stat-label">已借出</div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon available-icon">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ statisticsStore.statistics.available_books }}</div>
              <div class="stat-label">可借阅</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon overdue-icon">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ statisticsStore.statistics.overdue_books }}</div>
              <div class="stat-label">逾期图书</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card class="chart-card" v-loading="statisticsStore.loading">
      <template #header>
        <div class="card-header">
          <span>借阅趋势</span>
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            size="small"
            style="width: 240px"
          />
        </div>
      </template>
      <div class="chart-placeholder">
        <p>借阅趋势图表功能开发中...</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStatisticsStore } from '@/stores/statistics'
import { Reading, User, Document, Check, Warning } from '@element-plus/icons-vue'

const statisticsStore = useStatisticsStore()
const dateRange = ref('')

onMounted(() => {
  statisticsStore.fetchStatistics()
})
</script>

<style scoped>
.statistics {
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
  padding: 20px 0;
}

.stat-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.stat-icon {
  font-size: 48px;
  padding: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.book-icon {
  background-color: #e1f3d8;
  color: #67c23a;
}

.member-icon {
  background-color: #d9ecff;
  color: #409eff;
}

.borrowed-icon {
  background-color: #faecd8;
  color: #e6a23c;
}

.available-icon {
  background-color: #f0f9ff;
  color: #13ce66;
}

.overdue-icon {
  background-color: #fde2e2;
  color: #f56c6c;
}

.stat-info {
  text-align: left;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.chart-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.chart-placeholder p {
  color: #909399;
  font-size: 16px;
}
</style>