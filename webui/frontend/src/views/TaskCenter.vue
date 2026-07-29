<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div style="display: flex; align-items: center; justify-content: space-between">
          <span>{{ t('任务中心（蒸馏 / Agent 共用）') }}</span>
          <el-button size="small" @click="refresh">{{ t('刷新') }}</el-button>
        </div>
      </template>
      <el-table :data="tasks" v-loading="loading" :empty-text="t('暂无任务')">
        <el-table-column prop="id" :label="t('ID')" width="110" />
        <el-table-column prop="type" :label="t('类型')" width="90">
          <template #default="{ row }">
            <el-tag size="small" :type="row.type === 'distill' ? 'primary' : 'warning'">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="t('项目/领域')" min-width="180">
          <template #default="{ row }">{{ row.project }} / {{ row.domain }}</template>
        </el-table-column>
        <el-table-column prop="status" :label="t('状态')" width="100">
          <template #default="{ row }">
            <el-tag size="small" :type="statusType(row.status)">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" :label="t('创建时间')" width="170" />
        <el-table-column :label="t('操作')" min-width="140">
          <template #default="{ row }">
            <el-button link type="primary" @click="openLog(row)">{{ t('日志') }}</el-button>
            <el-button v-if="row.status === 'running' || row.status === 'queued'" link type="danger" @click="onStop(row)">{{ t('终止') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="visible" :title="t('任务日志 ') + (cur?.id || '')" width="760px">
      <TaskProgress :task-id="cur?.id || ''" @rerun="onRerun" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { listTasks, stopTask } from '../api.js'
import TaskProgress from '../components/TaskProgress.vue'
import { t } from '../i18n.js'

const tasks = ref([])
const loading = ref(false)
const visible = ref(false)
const cur = ref(null)

function statusType(s) {
  return { done: 'success', error: 'danger', running: 'warning', queued: 'info', stopped: 'info' }[s] || 'info'
}

async function refresh() {
  loading.value = true
  try {
    const r = await listTasks()
    tasks.value = r.tasks || []
  } catch (e) {
    ElMessage.error(t('加载任务失败：') + (e.response?.data?.detail || e.message))
  } finally {
    loading.value = false
  }
}

function openLog(row) {
  visible.value = true
  cur.value = row
}

function onRerun(id) {
  cur.value = { id }
  refresh()
}

async function onStop(row) {
  try {
    await stopTask(row.id)
    ElMessage.info(t('已发送终止信号'))
    await refresh()
  } catch (e) {
    ElMessage.error(t('终止失败：') + (e.response?.data?.detail || e.message))
  }
}

onMounted(refresh)
</script>
