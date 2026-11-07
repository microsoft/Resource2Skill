<template>
  <div>
    <el-row :gutter="16">
      <!-- 当前激活项目信息 -->
      <el-col :span="24">
        <el-card shadow="never" style="margin-bottom: 16px">
          <template #header>
            <span style="font-weight: 600">{{ t('当前工作区') }}</span>
          </template>
          <el-descriptions :column="3" border>
            <el-descriptions-item :label="t('激活项目')">
              {{ config.active_project || t('（未选择）') }}
            </el-descriptions-item>
            <el-descriptions-item :label="t('项目根路径')">
              <code>{{ t('webui/projects/') }}{{ config.active_project || t('—') }}</code>
            </el-descriptions-item>
            <el-descriptions-item :label="t('当前 Domain')">
              {{ config.active_domain || t('（未选择）') }}
            </el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-col>
    </el-row>

    <!-- 统计卡片 -->
    <el-row :gutter="16" style="margin-bottom: 16px">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic :title="t('运行中任务')" :value="runningCount" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic :title="t('待运行任务')" :value="queuedCount" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic :title="t('Skill 总数')" :value="skillsCount" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic :title="t('素材文件数')" :value="fixturesCount" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 快捷操作 -->
    <el-row style="margin-bottom: 16px">
      <el-button type="primary" @click="navigate('projects')">{{ t('+ 新建项目') }}</el-button>
      <el-button type="success" @click="navigate('distill')">{{ t('打开蒸馏工作台') }}</el-button>
      <el-button type="warning" @click="navigate('agent')">{{ t('新建 Agent 任务') }}</el-button>
    </el-row>

    <!-- 最近任务列表 -->
    <el-card shadow="never">
      <template #header>
        <span style="font-weight: 600">{{ t('最近任务') }}</span>
      </template>
      <el-table :data="recentTasks" style="width: 100%" v-loading="loading" :empty-text="t('暂无任务')">
        <el-table-column prop="status" :label="t('状态')" width="110">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="type" :label="t('类型')" width="120" />
        <el-table-column prop="domain" :label="t('Domain')" width="140" />
        <el-table-column prop="created_at" :label="t('创建时间')" width="200" />
        <el-table-column :label="t('操作')">
          <template #default="{ row }">
            <el-button link type="primary" @click="navigate('tasks')">{{ t('查看详情') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getConfig, listProjects, listTasks, listFixtures, listRepo } from '../api.js'
import { t } from '../i18n.js'

const config = ref({})
const projects = ref([])
const tasks = ref([])
const fixturesCount = ref(0)
const skillsCount = ref(0)
const loading = ref(false)

const emit = defineEmits(['navigate'])
function navigate(key) {
  emit('navigate', key)
}

const activeProject = computed(() =>
  projects.value.find((p) => p.name === config.value.active_project) || null
)
const domains = computed(() => activeProject.value?.domains || [])
const targetDomain = computed(() => config.value.active_domain || domains.value[0] || '')

const runningCount = computed(() => tasks.value.filter((x) => x.status === 'running').length)
const queuedCount = computed(() => tasks.value.filter((x) => x.status === 'queued').length)
const recentTasks = computed(() => tasks.value.slice(0, 5))

function statusType(s) {
  return { running: 'primary', queued: 'warning', done: 'success', error: 'danger', stopped: 'info' }[s] || 'info'
}
function statusText(s) {
  return { running: t('运行中'), queued: t('排队中'), done: t('成功'), error: t('失败'), stopped: t('已终止') }[s] || s
}

function asArray(data, key) {
  if (Array.isArray(data)) return data
  if (data && Array.isArray(data[key])) return data[key]
  if (data && Array.isArray(data[key + 's'])) return data[key + 's']
  return []
}

async function loadAll() {
  loading.value = true
  try {
    const [cfg, proj, tsk] = await Promise.all([getConfig(), listProjects(), listTasks()])
    config.value = cfg || {}
    projects.value = proj.projects || []
    tasks.value = tsk.tasks || []
    const p = config.value.active_project
    const d = targetDomain.value
    if (p && d) {
      const [fx, rp] = await Promise.all([
        listFixtures(p, d).catch(() => []),
        listRepo(p, d).catch(() => []),
      ])
      fixturesCount.value = asArray(fx, 'fixtures').length
      skillsCount.value = asArray(rp, 'skills').length
    }
  } catch (e) {
    console.error('Overview load failed', e)
  } finally {
    loading.value = false
  }
}

onMounted(loadAll)
</script>
