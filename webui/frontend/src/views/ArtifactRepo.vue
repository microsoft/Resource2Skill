<template>
  <div>
    <el-card shadow="never" style="margin-bottom: 16px">
      <el-form :inline="true">
        <el-form-item label="项目">
          <el-select v-model="project" placeholder="选择项目" style="width: 200px" @change="onProjectChange">
            <el-option v-for="p in projects" :key="p.name" :label="p.name + (p.is_active ? '（当前）' : '')" :value="p.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="领域">
          <el-select v-model="domain" placeholder="选择领域" style="width: 200px" @change="load">
            <el-option v-for="d in domains" :key="d" :label="d" :value="d" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button :disabled="!domain" @click="load">刷新</el-button>
        </el-form-item>
        <el-form-item>
          <span style="color: #909399; font-size: 12px">
            技能 {{ (data.skills || []).length }} 个 · 技能文件 {{ (data.skill_files || []).length }} 个 · 产物 {{ (data.output_files || []).length }} 个
          </span>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never" v-if="domain">
      <el-tabs v-model="tab">
        <el-tab-pane label="技能库" name="skills">
          <el-table :data="data.skill_files || []" size="small" border max-height="52vh" @row-dblclick="openFile">
            <el-table-column prop="rel_path" label="相对路径" min-width="260" show-overflow-tooltip />
            <el-table-column prop="ext" label="类型" width="90" />
            <el-table-column label="大小" width="110">
              <template #default="{ row }">{{ fmtSize(row.size) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="160">
              <template #default="{ row }">
                <el-button size="small" @click="openFile(row)">预览</el-button>
                <el-button size="small" type="primary" @click="download(row, 'skills')">下载</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="产物 output" name="output">
          <el-table :data="data.output_files || []" size="small" border max-height="52vh" @row-dblclick="openOutput">
            <el-table-column prop="rel_path" label="相对路径" min-width="260" show-overflow-tooltip />
            <el-table-column prop="ext" label="类型" width="90" />
            <el-table-column label="大小" width="110">
              <template #default="{ row }">{{ fmtSize(row.size) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="160">
              <template #default="{ row }">
                <el-button size="small" @click="openOutput(row)">预览</el-button>
                <el-button size="small" type="primary" @click="download(row, 'output')">下载</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <el-empty v-else description="选择项目/领域后浏览产物" />

    <el-dialog v-model="showPreview" title="预览" width="80%" top="5vh">
      <div v-if="preview" style="max-height: 70vh; overflow: auto">
        <div style="margin-bottom: 8px; color: #909399; font-size: 12px">{{ preview.rel }} · {{ preview.kind }}</div>
        <img v-if="preview.kind === 'image'" :src="preview.url" style="max-width: 100%" />
        <iframe v-else-if="preview.ext === 'html' || preview.ext === 'htm'" :src="preview.url" style="width: 100%; height: 68vh; border: 1px solid #dcdfe6" />
        <pre v-else style="white-space: pre-wrap; word-break: break-word; background: #0f1419; color: #d4d4d4; padding: 12px; border-radius: 6px; font-size: 13px">{{ preview.text || '（加载中…）' }}</pre>
      </div>
      <template #footer>
        <el-button @click="showPreview = false">关闭</el-button>
        <el-button v-if="preview" type="primary" @click="downloadCurrent">下载</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { listProjects, listDomains, listRepo, repoFileUrl } from '../api.js'

const projects = ref([])
const project = ref('')
const domains = ref([])
const domain = ref('')
const tab = ref('skills')
const data = ref({})
const showPreview = ref(false)
const preview = ref(null)

function fmtSize(n) {
  n = n || 0
  if (n < 1024) return n + ' B'
  if (n < 1024 * 1024) return (n / 1024).toFixed(1) + ' KB'
  return (n / 1024 / 1024).toFixed(1) + ' MB'
}

async function onProjectChange() {
  domain.value = ''
  domains.value = []
  if (!project.value) return
  try {
    const r = await listDomains(project.value)
    domains.value = r.domains || []
    if (domains.value.length) domain.value = domains.value[0]
    await load()
  } catch (e) {
    ElMessage.error('加载领域失败：' + (e.response?.data?.detail || e.message))
  }
}

async function load() {
  if (!project.value || !domain.value) return
  try {
    const r = await listRepo(project.value, domain.value)
    data.value = r
  } catch (e) {
    ElMessage.error('加载产物失败：' + (e.response?.data?.detail || e.message))
  }
}

function previewUrl(row, kind) {
  return repoFileUrl(project.value, kind, kind === 'skills' ? domain.value : '', row.rel_path)
}

async function openFile(row) {
  await openPreview(row, 'skills')
}
async function openOutput(row) {
  await openPreview(row, 'output')
}

async function openPreview(row, kind) {
  const url = previewUrl(row, kind)
  const item = { rel: row.rel_path, ext: (row.ext || '').toLowerCase(), kind: row.kind, url, text: '' }
  if (row.kind === 'text') {
    try {
      const r = await fetch(url)
      item.text = await r.text()
    } catch { item.text = '（文本加载失败）' }
  }
  preview.value = item
  showPreview.value = true
}

function download(row, kind) {
  const url = previewUrl(row, kind)
  window.open(url, '_blank')
}
function downloadCurrent() {
  if (preview.value) window.open(preview.value.url, '_blank')
}

onMounted(async () => {
  try {
    const r = await listProjects()
    projects.value = r.projects || []
    const active = projects.value.find((p) => p.is_active)
    project.value = active ? active.name : (projects.value[0]?.name || '')
    if (project.value) await onProjectChange()
  } catch (e) {
    ElMessage.error('初始化失败：' + (e.response?.data?.detail || e.message))
  }
})
</script>
