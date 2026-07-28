<template>
  <el-card shadow="never" v-if="taskId">
    <template #header>
      <div style="display: flex; align-items: center; justify-content: space-between">
        <span>
          任务 <code>{{ taskId }}</code> ·
          <el-tag :type="statusType(taskStatus)" size="small">{{ taskStatus }}</el-tag>
        </span>
        <el-button v-if="isRunning" size="small" type="danger" @click="onStop">终止</el-button>
      </div>
    </template>
    <pre style="white-space: pre-wrap; word-break: break-word; max-height: 50vh; overflow: auto; background: #0f1419; color: #d4d4d4; padding: 12px; border-radius: 6px; margin: 0; font-size: 13px">{{ logText || '（等待日志…）' }}</pre>
    <div v-if="summary" style="margin-top: 12px">
      <el-alert type="success" :closable="false"
        :title="`新增 ${summary.added} 条，跳过 ${summary.skipped} 个，技能库现有 ${summary.total_skills} 条`" />
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, watch, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getTask, stopTask } from '../api.js'

const props = defineProps({ taskId: { type: String, default: '' } })
const emit = defineEmits(['updated', 'stopped'])

const taskStatus = ref('')
const log = ref([])
const summary = ref(null)
const isRunning = computed(() => taskStatus.value === 'running' || taskStatus.value === 'queued')
const logText = computed(() => (log.value || []).join('\n'))

function statusType(s) {
  return { done: 'success', error: 'danger', running: 'warning', queued: 'info', stopped: 'info' }[s] || 'info'
}

let timer = null
function startPoll() {
  stopPoll()
  timer = setInterval(async () => {
    if (!props.taskId) return
    try {
      const r = await getTask(props.taskId)
      taskStatus.value = r.status
      log.value = r.log || []
      summary.value = r.summary || null
      emit('updated', r)
      if (!isRunning.value) stopPoll()
    } catch { /* ignore transient */ }
  }, 1500)
}
function stopPoll() {
  if (timer) { clearInterval(timer); timer = null }
}

async function onStop() {
  try {
    await stopTask(props.taskId)
    ElMessage.info('已发送终止信号')
    emit('stopped')
  } catch (e) {
    ElMessage.error('终止失败：' + (e.response?.data?.detail || e.message))
  }
}

watch(() => props.taskId, (id) => {
  if (id) {
    taskStatus.value = 'queued'
    log.value = []
    summary.value = null
    startPoll()
  } else {
    stopPoll()
  }
}, { immediate: true })

onUnmounted(stopPoll)
</script>
