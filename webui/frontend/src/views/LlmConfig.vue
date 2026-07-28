<template>
  <div>
    <div style="margin-bottom: 12px">
      <el-button type="primary" @click="openCreate">新建配置模板</el-button>
    </div>

    <el-table :data="list" border style="width: 100%">
      <el-table-column prop="name" label="名称" />
      <el-table-column prop="provider" label="厂商" />
      <el-table-column prop="model" label="模型" />
      <el-table-column prop="endpoint" label="Endpoint" />
      <el-table-column prop="api_key_masked" label="Key" />
      <el-table-column label="激活" width="70">
        <template #default="{ row }">
          <el-tag v-if="row.is_active" type="success">是</el-tag>
          <span v-else>否</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="240">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">测试/编辑</el-button>
          <el-button
            size="small"
            type="success"
            :disabled="row.is_active"
            @click="onActive(row)"
            >激活</el-button
          >
          <el-button size="small" type="danger" @click="onDelete(row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialog"
      :title="editing ? '测试/编辑：' + form.name : '新建配置模板'"
      width="560px"
    >
      <el-form :model="form" label-width="110px">
        <el-form-item label="名称">
          <el-input v-model="form.name" :disabled="editing" />
        </el-form-item>
        <el-form-item label="厂商">
          <el-select v-model="form.provider" style="width: 100%">
            <el-option label="DeepSeek" value="deepseek" />
            <el-option label="OpenAI" value="openai" />
            <el-option label="Azure OpenAI" value="azure" />
            <el-option label="Ollama(本地)" value="ollama" />
            <el-option label="自定义API" value="custom" />
          </el-select>
        </el-form-item>
        <el-form-item label="Endpoint">
          <el-input v-model="form.endpoint" placeholder="https://api.deepseek.com/v1" />
        </el-form-item>
        <el-form-item label="API Key">
          <el-input
            v-model="form.api_key"
            type="password"
            show-password
            placeholder="不明文展示，仅本机加密存储"
          />
        </el-form-item>
        <el-form-item label="模型">
          <el-input v-model="form.model" />
        </el-form-item>
        <el-form-item label="Temperature">
          <el-input-number v-model="form.temperature" :min="0" :max="1" :step="0.1" />
        </el-form-item>
        <el-form-item label="Max Tokens">
          <el-input-number v-model="form.max_tokens" :min="256" :max="32000" :step="256" />
        </el-form-item>
        <el-form-item label="Reasoning">
          <el-select v-model="form.reasoning" style="width: 100%">
            <el-option label="none" value="none" />
            <el-option label="low" value="low" />
            <el-option label="medium" value="medium" />
            <el-option label="high" value="high" />
          </el-select>
        </el-form-item>
        <el-form-item label="代理(可选)">
          <el-input v-model="form.proxy" placeholder="http://127.0.0.1:7890" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog = false">取消</el-button>
        <el-button @click="onTestDialog">测试连接</el-button>
        <el-button type="primary" @click="onSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { listLlm, upsertLlm, deleteLlm, setActive, testLlm } from '../api.js'

const list = ref([])
const dialog = ref(false)
const editing = ref(false)
const form = ref(blank())

function blank() {
  return {
    name: '',
    provider: 'deepseek',
    endpoint: '',
    api_key: '',
    model: '',
    temperature: 0.2,
    max_tokens: 4096,
    reasoning: 'low',
    proxy: ''
  }
}

async function refresh() {
  const r = await listLlm()
  list.value = r.templates
}

function openCreate() {
  form.value = blank()
  editing.value = false
  dialog.value = true
}

function openEdit(row) {
  form.value = { ...row, api_key: '' }
  editing.value = true
  dialog.value = true
}

async function onSave() {
  const r = await upsertLlm(form.value)
  if (r.ok) {
    ElMessage.success('已保存')
    dialog.value = false
    await refresh()
  }
}

async function onActive(row) {
  const r = await setActive(row.name)
  if (r.ok) {
    ElMessage.success('已激活')
    await refresh()
  }
}

async function onDelete(row) {
  await deleteLlm(row.name)
  ElMessage.success('已删除')
  await refresh()
}

async function onTestDialog() {
  if (!form.value.api_key) {
    ElMessage.warning('请输入真实 API Key 后再测试')
    return
  }
  const r = await testLlm(form.value)
  if (r.ok) ElMessage.success('连通成功 (' + r.status + ')')
  else ElMessage.error('连通失败：' + (r.message || r.status))
}

onMounted(refresh)
</script>
