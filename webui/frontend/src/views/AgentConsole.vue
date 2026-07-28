<template>
  <div>
    <el-card shadow="never" style="margin-bottom: 16px">
      <el-form :inline="true" label-width="72px">
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
      </el-form>
      <el-form label-width="72px">
        <el-form-item label="任务">
          <el-input v-model="taskText" type="textarea" :rows="4" placeholder="用自然语言描述要 Agent 完成的任务，例如：为一款产品生成立项文档并产出阶段交付物" style="max-width: 760px" />
        </el-form-item>
        <el-form-item label="模型">
          <el-input v-model="model" placeholder="留空则用 LLM 模板模型" style="width: 240px" />
        </el-form-item>
        <el-form-item label="推理档位">
          <el-select v-model="reasoning" placeholder="留空则用 LLM 模板值" style="width: 200px" clearable>
            <el-option label="none" value="none" />
            <el-option label="low" value="low" />
            <el-option label="medium" value="medium" />
            <el-option label="high" value="high" />
            <el-option label="xhigh" value="xhigh" />
          </el-select>
        </el-form-item>
        <el-form-item label="迭代上限">
          <el-input-number v-model="maxIter" :min="1" :max="60" />
        </el-form-item>
        <el-form-item label="参考技能数">
          <el-input-number v-model="nSkills" :min="0" :max="20" />
        </el-form-item>
        <el-form-item label="TopK">
          <el-input-number v-model="topK" :min="1" :max="50" />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="dryRun">Dry-run（占位工具，不落盘交付物）</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :disabled="!ctx.state.activeDomain || !taskText || running" @click="onStart">运行 Agent</el-button>
          <span style="color: #909399; font-size: 12px; margin-left: 12px">单 worker 串行执行，运行期间请勿再提交其它任务</span>
        </el-form-item>
      </el-form>
    </el-card>

    <TaskProgress :task-id="taskId" @updated="onUpdated" @rerun="onRerun" />
    <div v-if="extra && extra.tool_calls && extra.tool_calls.length" style="margin-top: 12px">
      <div style="font-weight: 600; margin-bottom: 8px">工具调用记录</div>
      <el-table :data="extra.tool_calls" size="small" border max-height="240">
        <el-table-column prop="tool" label="工具" width="220" />
        <el-table-column label="结果" width="90">
          <template #default="{ row }">
            <el-tag size="small" :type="row.success ? 'success' : 'danger'">{{ row.success ? 'OK' : 'ERR' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="args" label="参数" show-overflow-tooltip />
        <el-table-column prop="error" label="错误" show-overflow-tooltip />
      </el-table>
    </div>
    <el-empty v-if="!taskId" description="选择项目/领域并填写任务后点击「运行 Agent」" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { runAgent } from '../api.js'
import { useActiveContext } from '../composables/useActiveContext.js'
import TaskProgress from '../components/TaskProgress.vue'

const ctx = useActiveContext()
const taskText = ref('')
const model = ref('')
const reasoning = ref('')
const maxIter = ref(12)
const nSkills = ref(5)
const topK = ref(20)
const dryRun = ref(false)
const taskId = ref('')
const extra = ref(null)
const running = ref(false)

function onUpdated(r) {
  extra.value = r.extra || null
  if (['done', 'error', 'stopped'].includes(r.status)) running.value = false
}

function onRerun(id) {
  taskId.value = id
  running.value = true
  extra.value = null
}

async function onStart() {
  try {
    const r = await runAgent(ctx.state.activeProject, {
      domain: ctx.state.activeDomain,
      task: taskText.value,
      model: model.value,
      reasoning: reasoning.value,
      max_iter: maxIter.value,
      n_skills: nSkills.value,
      top_k: topK.value,
      dry_run: dryRun.value,
    })
    taskId.value = r.task_id
    extra.value = null
    running.value = true
    ElMessage.success('已提交 Agent 任务')
  } catch (e) {
    ElMessage.error('提交失败：' + (e.response?.data?.detail || e.message))
  }
}

onMounted(() => ctx.loadProjects())
</script>
