<template>
  <div>
    <el-card shadow="never" style="margin-bottom: 16px">
      <el-form :inline="true">
        <el-form-item :label="t('项目')">
          <el-select v-model="project" :placeholder="t('选择项目')" style="width: 200px" @change="onProjectChange">
            <el-option v-for="p in projects" :key="p.name" :label="p.name + (p.is_active ? t('（当前）') : '')" :value="p.name" />
          </el-select>
        </el-form-item>
        <el-form-item :label="t('领域')">
          <el-select v-model="domain" :placeholder="t('选择领域')" style="width: 200px" @change="refresh">
            <el-option v-for="d in domains" :key="d" :label="d" :value="d" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-upload
            :action="uploadUrl"
            :disabled="!domain"
            :show-file-list="false"
            :before-upload="beforeUpload"
            :on-success="onUploadSuccess"
            :on-error="onUploadError"
            multiple
          >
            <el-button type="primary" :disabled="!domain">{{ t('上传素材') }}</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <span style="color: #909399; font-size: 12px"
            >{{ t('支持 PDF / DOCX / PPTX / XLSX / MD / TXT；仅文档类') }}</span
          >
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="rows" v-loading="loading" :empty-text="t('暂无素材，先选择领域并上传')">
        <el-table-column prop="name" :label="t('文件名')" min-width="200" />
        <el-table-column prop="ext" :label="t('类型')" width="90" />
        <el-table-column :label="t('大小')" width="110">
          <template #default="{ row }">{{ fmtSize(row.size) }}</template>
        </el-table-column>
        <el-table-column :label="t('启用')" width="90">
          <template #default="{ row }">
            <el-switch v-model="row.enabled" @change="(v) => onToggle(row, v)" />
          </template>
        </el-table-column>
        <el-table-column prop="uploaded_at" :label="t('上传时间')" width="170" />
        <el-table-column :label="t('操作')" min-width="160">
          <template #default="{ row }">
            <el-button link type="primary" @click="onPreview(row)">{{ t('预览') }}</el-button>
            <el-button link type="danger" @click="onDelete(row)">{{ t('删除') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="previewVisible" :title="t('预览：') + previewName" width="720px">
      <div v-if="previewLoading" v-loading="true" style="height: 320px" />
      <pre v-else-if="previewData && previewData.available"
        style="white-space: pre-wrap; word-break: break-word; max-height: 60vh; overflow: auto; background: #f7f8fa; padding: 12px; border-radius: 6px; margin: 0">{{ previewData.text }}</pre>
      <el-alert v-else type="warning" :closable="false" :title="(previewData && previewData.message) || t('无可用文本')" />
      <template #footer v-if="previewData && previewData.available && previewData.truncated">
        <span style="color: #909399; font-size: 12px">{{ t('仅显示前 ') }}{{ previewData.text.length }}{{ t(' 字（共 ') }}{{ previewData.total_chars }}{{ t(' 字）') }}</span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  listProjects, listDomains, listFixtures, enableFixture,
  deleteFixture, previewFixture, fixtureUploadUrl,
} from '../api.js'
import { t } from '../i18n.js'

const projects = ref([])
const project = ref('')
const domains = ref([])
const domain = ref('')
const rows = ref([])
const loading = ref(false)

const uploadUrl = computed(() => (project.value && domain.value ? fixtureUploadUrl(project.value, domain.value) : ''))

const previewVisible = ref(false)
const previewLoading = ref(false)
const previewName = ref('')
const previewData = ref(null)

function fmtSize(n) {
  if (n < 1024) return n + ' B'
  if (n < 1024 * 1024) return (n / 1024).toFixed(1) + ' KB'
  return (n / 1024 / 1024).toFixed(1) + ' MB'
}

async function refresh() {
  if (!project.value || !domain.value) {
    rows.value = []
    return
  }
  loading.value = true
  try {
    const r = await listFixtures(project.value, domain.value)
    rows.value = r.fixtures || []
  } catch (e) {
    ElMessage.error(t('加载素材失败：') + (e.response?.data?.detail || e.message))
  } finally {
    loading.value = false
  }
}

async function onProjectChange() {
  domain.value = ''
  domains.value = []
  if (!project.value) return
  try {
    const r = await listDomains(project.value)
    domains.value = r.domains || []
    if (domains.value.length) domain.value = domains.value[0]
  } catch (e) {
    ElMessage.error(t('加载领域失败：') + (e.response?.data?.detail || e.message))
  }
  await refresh()
}

function beforeUpload(file) {
  const ok = /\.(pdf|docx|pptx|xlsx|md|txt)$/i.test(file.name)
  if (!ok) {
    ElMessage.error(t('不支持的类型：') + file.name)
    return false
  }
  return true
}

function onUploadSuccess() {
  ElMessage.success(t('上传成功'))
  refresh()
}

function onUploadError() {
  ElMessage.error(t('上传失败（类型不支持或服务端拒绝）'))
}

async function onToggle(row, val) {
  try {
    await enableFixture(project.value, domain.value, row.name, val)
  } catch (e) {
    row.enabled = !val
    ElMessage.error(t('更新启用状态失败：') + (e.response?.data?.detail || e.message))
  }
}

async function onDelete(row) {
  try {
    await ElMessageBox.confirm(t('确认删除素材「') + row.name + t('」？将移入回收站（可恢复）。'), t('删除确认'), {
      type: 'warning',
    })
  } catch {
    return
  }
  try {
    await deleteFixture(project.value, domain.value, row.name)
    ElMessage.success(t('已删除（软删除）'))
    refresh()
  } catch (e) {
    ElMessage.error(t('删除失败：') + (e.response?.data?.detail || e.message))
  }
}

async function onPreview(row) {
  previewName.value = row.name
  previewVisible.value = true
  previewLoading.value = true
  previewData.value = null
  try {
    previewData.value = await previewFixture(project.value, domain.value, row.name)
  } catch (e) {
    ElMessage.error(t('预览失败：') + (e.response?.data?.detail || e.message))
  } finally {
    previewLoading.value = false
  }
}

onMounted(async () => {
  try {
    const r = await listProjects()
    projects.value = r.projects || []
    const active = projects.value.find((p) => p.is_active)
    project.value = active ? active.name : (projects.value[0]?.name || '')
    if (project.value) await onProjectChange()
  } catch (e) {
    ElMessage.error(t('初始化失败：') + (e.response?.data?.detail || e.message))
  }
})
</script>
