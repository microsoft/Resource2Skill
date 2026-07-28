<template>
  <div>
    <el-card shadow="never" style="margin-bottom: 16px">
      <el-form :inline="true">
        <el-form-item label="项目">
          <el-select v-model="ctx.state.activeProject" placeholder="选择项目" style="width: 200px" @change="ctx.selectProject">
            <el-option v-for="p in ctx.state.projects" :key="p.name" :label="p.name + (p.is_active ? '（当前）' : '')" :value="p.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="领域">
          <el-select v-model="ctx.state.activeDomain" placeholder="选择领域" style="width: 200px">
            <el-option v-for="d in ctx.state.domains" :key="d" :label="d" :value="d" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="dryRun">仅验证管线（不调用 LLM）</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :disabled="!ctx.state.activeDomain || running" @click="onStart">开始蒸馏</el-button>
        </el-form-item>
        <el-form-item>
          <span style="color: #909399; font-size: 12px">本域已蒸馏技能：{{ skillCount }}</span>
        </el-form-item>
      </el-form>
    </el-card>

    <TaskProgress :task-id="taskId" @updated="onUpdated" />
    <el-empty v-if="!taskId" description="选择领域后点击「开始蒸馏」" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { startDistill } from '../api.js'
import { useActiveContext } from '../composables/useActiveContext.js'
import TaskProgress from '../components/TaskProgress.vue'

const ctx = useActiveContext()
const dryRun = ref(false)
const taskId = ref('')
const skillCount = ref(0)
const running = ref(false)

function onUpdated(r) {
  if (r.summary && r.domain === ctx.state.activeDomain) {
    skillCount.value = r.summary.total_skills
  }
  if (['done', 'error', 'stopped'].includes(r.status)) running.value = false
}

async function onStart() {
  try {
    const r = await startDistill(ctx.state.activeProject, ctx.state.activeDomain, dryRun.value)
    taskId.value = r.task_id
    skillCount.value = 0
    running.value = true
    ElMessage.success('已提交蒸馏任务')
  } catch (e) {
    ElMessage.error('提交失败：' + (e.response?.data?.detail || e.message))
  }
}

onMounted(() => ctx.loadProjects())
</script>
