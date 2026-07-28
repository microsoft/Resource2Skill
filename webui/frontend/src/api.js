import axios from 'axios'

const http = axios.create({ baseURL: '/api' })

export const listLlm = () => http.get('/llm').then((r) => r.data)
export const upsertLlm = (t) => http.post('/llm', t).then((r) => r.data)
export const deleteLlm = (name) => http.delete(`/llm/${name}`).then((r) => r.data)
export const setActive = (name) => http.post(`/llm/${name}/active`).then((r) => r.data)
export const testLlm = (t) => http.post('/llm/test', t).then((r) => r.data)
export const getConfig = () => http.get('/config').then((r) => r.data)

// ---- 项目 / 领域（切片1） ----
export const listProjects = () => http.get('/projects').then((r) => r.data)
export const createProject = (name, description) =>
  http.post('/projects', { name, description }).then((r) => r.data)
export const deleteProject = (name) => http.delete(`/projects/${name}`).then((r) => r.data)
export const activateProject = (name) =>
  http.post(`/projects/${name}/active`).then((r) => r.data)
export const listRepoDomains = () => http.get('/repo-domains').then((r) => r.data)
export const listDomains = (project) =>
  http.get(`/projects/${project}/domains`).then((r) => r.data)
export const createDomain = (project, domain, seedFrom) =>
  http.post(`/projects/${project}/domains`, { domain, seed_from: seedFrom || null }).then((r) => r.data)
export const activateDomain = (project, domain) =>
  http.post(`/projects/${project}/domains/${domain}/active`).then((r) => r.data)
export const validateDomain = (project, domain) =>
  http.post(`/projects/${project}/domains/${domain}/validate`).then((r) => r.data)

// ---- 素材管理（切片2） ----
export const listFixtures = (project, domain) =>
  http.get(`/projects/${project}/domains/${domain}/fixtures`).then((r) => r.data)
export const enableFixture = (project, domain, filename, enabled) =>
  http.post(`/projects/${project}/domains/${domain}/fixtures/${encodeURIComponent(filename)}/enable`, { enabled }).then((r) => r.data)
export const deleteFixture = (project, domain, filename) =>
  http.delete(`/projects/${project}/domains/${domain}/fixtures/${encodeURIComponent(filename)}`).then((r) => r.data)
export const previewFixture = (project, domain, filename) =>
  http.get(`/projects/${project}/domains/${domain}/fixtures/${encodeURIComponent(filename)}/preview`).then((r) => r.data)
// el-upload 不走 axios，需完整相对路径（dev server 代理 /api）
export const fixtureUploadUrl = (project, domain) =>
  `/api/projects/${encodeURIComponent(project)}/domains/${encodeURIComponent(domain)}/fixtures`

// ---- 蒸馏工作台 + 任务中心（切片3） ----
export const startDistill = (project, domain, dryRun = false) =>
  http.post(`/projects/${project}/domains/${domain}/distill`, { dry_run: dryRun }).then((r) => r.data)
export const listTasks = () => http.get('/tasks').then((r) => r.data)
export const getTask = (id) => http.get(`/tasks/${id}`).then((r) => r.data)
export const stopTask = (id) => http.post(`/tasks/${id}/stop`).then((r) => r.data)

// ---- Agent 执行台（切片4） ----
export const runAgent = (project, body) =>
  http.post(`/projects/${encodeURIComponent(project)}/agent/run`, body).then((r) => r.data)

// ---- 产物仓库（切片4） ----
export const listRepo = (project, domain) =>
  http.get(`/projects/${encodeURIComponent(project)}/repo`, { params: { domain } }).then((r) => r.data)
export const repoFileUrl = (project, kind, domain, relPath) => {
  const params = new URLSearchParams({ kind, rel_path: relPath })
  if (domain) params.set('domain', domain)
  return `/api/projects/${encodeURIComponent(project)}/repo/file?${params.toString()}`
}

