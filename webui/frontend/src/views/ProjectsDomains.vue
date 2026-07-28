<template>
  <div>
    <!-- 项目区 -->
    <el-card shadow="never" style="margin-bottom: 16px">
      <template #header>
        <div style="display: flex; align-items: center; justify-content: space-between">
          <span style="font-weight: 600">项目（多项目隔离）</span>
          <el-button type="primary" size="small" @click="openProject">新建项目</el-button>
        </div>
      </template>
      <el-table :data="ctx.state.projects" border style="width: 100%" @current-change="onRow">
        <el-table-column prop="name" label="名称" width="160" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="激活" width="70">
          <template #default="{ row }">
            <el-tag v-if="row.is_active" type="success">是</el-tag>
            <span v-else>否</span>
          </template>
        </el-table-column>
        <el-table-column label="领域数" width="80">
          <template #default="{ row }">{{ row.domains.length }}</template>
        </el-table-column>
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button
              size="small"
              type="success"
              :disabled="row.is_active"
              @click="onActivateProject(row)"
              >激活</el-button
            >
            <el-button size="small" type="danger" @click="onDeleteProject(row)"
              >删除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 领域区 -->
    <el-card shadow="never">
      <template #header>
        <div style="display: flex; align-items: center; justify-content: space-between">
          <span style="font-weight: 600">
            领域管理
            <span v-if="current" style="color: #888; font-weight: 400"
              >· 当前项目：{{ current }}<template v-if="ctx.state.activeDomain"> · 当前领域：{{ ctx.state.activeDomain }}</template></span
            >
            <span v-else style="color: #c00; font-weight: 400">（请先在上方选择或激活一个项目）</span>
          </span>
          <el-button
            type="primary"
            size="small"
            :disabled="!current"
            @click="openDomain"
            >新建领域</el-button
          >
        </div>
      </template>

      <el-empty v-if="!current" description="请先在上方选择或激活一个项目" />
      <el-table v-else :data="domainRows" border style="width: 100%">
        <el-table-column prop="name" label="领域" width="160" />
        <el-table-column label="激活" width="70">
          <template #default="{ row }">
            <el-tag v-if="row.name === ctx.state.activeDomain" type="success">是</el-tag>
            <span v-else>否</span>
          </template>
        </el-table-column>
        <el-table-column label="校验结果" width="120">
          <template #default="{ row }">
            <template v-if="row.result === undefined">
              <span style="color: #888">未校验</span>
            </template>
            <el-tag v-else :type="row.result.valid ? 'success' : 'danger'">
              {{ row.result.valid ? 'PASS' : 'FAIL' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="错误详情" min-width="200">
          <template #default="{ row }">
            <span v-if="!row.result || row.result.valid" style="color: #888">—</span>
            <ul v-else style="margin: 0; padding-left: 18px; color: #c00">
              <li v-for="(e, i) in row.result.errors" :key="i">{{ e }}</li>
            </ul>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240">
          <template #default="{ row }">
            <el-button size="small" @click="onValidate(row)">校验</el-button>
            <el-button
              size="small"
              type="success"
              :disabled="row.name === ctx.state.activeDomain"
              @click="onActivateDomain(row)"
              >激活</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新建项目对话框 -->
    <el-dialog v-model="projectDialog" title="新建项目" width="460px">
      <el-form :model="projectForm" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="projectForm.name" placeholder="仅字母/数字/-/_" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="projectForm.description" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="projectDialog = false">取消</el-button>
        <el-button type="primary" @click="onSaveProject">创建</el-button>
      </template>
    </el-dialog>

    <!-- 新建领域对话框 -->
    <el-dialog v-model="domainDialog" title="新建领域" width="460px">
      <el-form :model="domainForm" label-width="80px">
        <el-form-item label="领域名">
          <el-input v-model="domainForm.domain" placeholder="如 ipd / ppt / 自定义" />
        </el-form-item>
        <el-form-item label="播种来源">
          <el-select
            v-model="domainForm.seedFrom"
            placeholder="留空=生成空白脚手架"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="d in repoDomains"
              :key="d"
              :label="d"
              :value="d"
            />
          </el-select>
          <div style="font-size: 12px; color: #888; margin-top: 4px">
            选择仓库已有领域可直接复制其 domain.yaml 与引用文件（校验直接 PASS）。
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="domainDialog = false">取消</el-button>
        <el-button type="primary" @click="onSaveDomain">创建并校验</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  createProject,
  deleteProject,
  listRepoDomains,
  createDomain,
  activateDomain,
  validateDomain,
} from '../api.js'
import { useActiveContext } from '../composables/useActiveContext.js'

const ctx = useActiveContext()
const current = ref('')
const domainRows = ref([])
const repoDomains = ref([])

const projectDialog = ref(false)
const projectForm = ref({ name: '', description: '' })
const domainDialog = ref(false)
const domainForm = ref({ domain: '', seedFrom: '' })

async function loadDomainsHere() {
  if (!current.value) {
    domainRows.value = []
    return
  }
  await ctx.loadDomains(current.value)
  domainRows.value = ctx.state.domains.map((n) => ({ name: n, result: undefined }))
}

// 行点击：直接加载该项目的领域（修复 I1：之前点了不加载、必须再点激活）
function onRow(row) {
  if (row) {
    current.value = row.name
    loadDomainsHere()
  }
}

async function refreshProjects() {
  await ctx.loadProjects()
  const active = ctx.state.projects.find((p) => p.is_active)
  if (active && active.name !== current.value) {
    current.value = active.name
    await loadDomainsHere()
  } else if (!active) {
    current.value = ''
    domainRows.value = []
  }
}

function openProject() {
  projectForm.value = { name: '', description: '' }
  projectDialog.value = true
}

async function onSaveProject() {
  if (!projectForm.value.name) {
    ElMessage.warning('请填写项目名称')
    return
  }
  const r = await createProject(projectForm.value.name, projectForm.value.description)
  if (r.ok) {
    ElMessage.success('项目已创建')
    projectDialog.value = false
    await refreshProjects()
  }
}

async function onActivateProject(row) {
  await ctx.setActiveProject(row.name)
  ElMessage.success('已激活：' + row.name)
  current.value = row.name
  await loadDomainsHere()
}

async function onDeleteProject(row) {
  await deleteProject(row.name)
  ElMessage.success('已删除（移入 .trash）：' + row.name)
  if (current.value === row.name) current.value = ''
  await refreshProjects()
}

function openDomain() {
  domainForm.value = { domain: '', seedFrom: '' }
  domainDialog.value = true
}

async function onSaveDomain() {
  if (!domainForm.value.domain) {
    ElMessage.warning('请填写领域名')
    return
  }
  const r = await createDomain(
    current.value,
    domainForm.value.domain,
    domainForm.value.seedFrom || null
  )
  if (r.ok) {
    ElMessage.success(r.seeded ? '已从仓库播种' : '已生成空白脚手架')
    domainDialog.value = false
    await loadDomainsHere()
    const row = domainRows.value.find((d) => d.name === r.domain)
    if (row) await onValidate(row)
  }
}

async function onValidate(row) {
  const r = await validateDomain(current.value, row.name)
  row.result = { valid: r.valid, errors: r.errors || [] }
  if (r.valid) ElMessage.success(row.name + ' 校验 PASS')
  else ElMessage.error(row.name + ' 校验 FAIL')
}

async function onActivateDomain(row) {
  await activateDomain(current.value, row.name)
  ElMessage.success('已激活领域：' + row.name)
  // 激活后刷新 store 的 activeDomain（C2：让工作台立即读到新激活的领域）
  await ctx.loadDomains(current.value)
}

onMounted(async () => {
  const rd = await listRepoDomains()
  repoDomains.value = rd.domains
  await refreshProjects()
})
</script>
