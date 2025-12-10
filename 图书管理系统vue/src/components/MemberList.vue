<template>
  <div class="member-list">
    <div class="header">
      <h2>会员管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        添加会员
      </el-button>
    </div>

    <el-table :data="memberStore.members" style="width: 100%" v-loading="memberStore.loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="姓名" width="120" />
      <el-table-column prop="email" label="邮箱" width="200" />
      <el-table-column prop="phone" label="电话" width="120" />
      <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip />
      <el-table-column prop="membership_date" label="入会日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.membership_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
            {{ row.status === 'active' ? '正常' : '停用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="editMember(row)">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加会员对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="editingMember ? '编辑会员' : '添加会员'"
      width="500px"
    >
      <el-form :model="memberForm" :rules="rules" ref="memberFormRef" label-width="80px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="memberForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="memberForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="memberForm.phone" placeholder="请输入电话" />
        </el-form-item>
        <el-form-item label="地址">
          <el-input
            v-model="memberForm.address"
            type="textarea"
            :rows="2"
            placeholder="请输入地址"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="submitMember">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { useMemberStore } from '@/stores/member'

const memberStore = useMemberStore()

const showAddDialog = ref(false)
const editingMember = ref(null)
const memberFormRef = ref(null)

const memberForm = reactive({
  name: '',
  email: '',
  phone: '',
  address: ''
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const editMember = (member) => {
  editingMember.value = member
  Object.assign(memberForm, {
    name: member.name,
    email: member.email || '',
    phone: member.phone || '',
    address: member.address || ''
  })
  showAddDialog.value = true
}

const submitMember = async () => {
  try {
    await memberFormRef.value.validate()
    
    if (editingMember.value) {
      // 编辑会员（这里需要后端API支持）
      ElMessage.success('编辑功能需要后端API支持')
    } else {
      await memberStore.addMember(memberForm)
      ElMessage.success('添加成功')
    }
    
    showAddDialog.value = false
    resetForm()
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '操作失败')
  }
}

const resetForm = () => {
  editingMember.value = null
  Object.assign(memberForm, {
    name: '',
    email: '',
    phone: '',
    address: ''
  })
  memberFormRef.value?.clearValidate()
}

onMounted(() => {
  memberStore.fetchMembers()
})
</script>

<style scoped>
.member-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>