<template>
  <div class="member-list">
    <div class="header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="showAddDialog = true">
        <el-icon><Plus /></el-icon>
        添加用户
      </el-button>
    </div>

    <el-table :data="memberStore.members" style="width: 100%" v-loading="memberStore.loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="姓名" width="120" />
      <el-table-column prop="email" label="邮箱" width="200" />
      <el-table-column prop="phone" label="电话" width="120" />
      <el-table-column prop="address" label="地址" min-width="200" show-overflow-tooltip />
      <el-table-column prop="join_date" label="注册日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.join_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
            {{ row.status === 'active' ? '正常' : '停用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="editMember(row)">编辑</el-button>
          <el-button 
            :type="row.status === 'active' ? 'warning' : 'success'" 
            link 
            @click="toggleMemberStatus(row)"
          >
            {{ row.status === 'active' ? '停用' : '启用' }}
          </el-button>
          <el-button type="danger" link @click="confirmDeleteMember(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加会员对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="editingMember ? '编辑用户' : '添加用户'"
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
        <el-form-item 
          label="密码" 
          prop="password"
          :rules="editingMember ? [] : rules.password"
        >
          <el-input 
            v-model="memberForm.password" 
            placeholder="{{ editingMember ? '请输入新密码（不填则保持不变）' : '请输入密码' }}"
            type="password"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="submitMember">确定</el-button>
      </template>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="showDeleteDialog"
      title="确认删除"
      width="400px"
    >
      <p>确定要删除会员 <strong>{{ memberToDelete?.name }}</strong> 吗？</p>
      <p style="color: #f56c6c; font-size: 12px;">删除后数据将无法恢复，且该会员的所有借阅记录也会被删除。</p>
      <template #footer>
        <el-button @click="showDeleteDialog = false">取消</el-button>
        <el-button type="danger" @click="deleteMember">确定删除</el-button>
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
const showDeleteDialog = ref(false)
const editingMember = ref(null)
const memberToDelete = ref(null)
const memberFormRef = ref(null)

const memberForm = reactive({
  name: '',
  email: '',
  phone: '',
  address: '',
  password: ''
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ]
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
    address: member.address || '',
    password: '' // 编辑时不自动填充密码
  })
  showAddDialog.value = true
}

const submitMember = async () => {
  try {
    await memberFormRef.value.validate()
    
    // 创建提交数据对象，过滤掉空密码
    const formData = { ...memberForm }
    if (editingMember.value && !formData.password) {
      delete formData.password // 编辑时如果密码为空，则不更新密码
    }
    
    if (editingMember.value) {
      // 调用后端API更新会员
      await memberStore.updateMember(editingMember.value.id, formData)
      ElMessage.success('编辑成功')
    } else {
      await memberStore.addMember(formData)
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
    address: '',
    password: '' // 重置时清除密码
  })
  memberFormRef.value?.clearValidate()
}

// 切换会员状态（启用/停用）
const toggleMemberStatus = async (member) => {
  try {
    await memberStore.updateMember(member.id, {
      status: member.status === 'active' ? 'inactive' : 'active'
    })
    ElMessage.success(member.status === 'active' ? '会员已停用' : '会员已启用')
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '操作失败')
  }
}

// 确认删除会员
const confirmDeleteMember = (member) => {
  memberToDelete.value = member
  showDeleteDialog.value = true
}

// 删除会员
const deleteMember = async () => {
  if (!memberToDelete.value) return
  
  try {
    await memberStore.deleteMember(memberToDelete.value.id)
    ElMessage.success('会员删除成功')
    showDeleteDialog.value = false
    memberToDelete.value = null
  } catch (error) {
    ElMessage.error(error.response?.data?.error || '删除失败')
  }
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