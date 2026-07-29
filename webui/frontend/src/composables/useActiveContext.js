// 共享的"当前项目/领域"上下文（模块级 reactive 单例）。
// 不引入 Pinia：应用小、单用户，模块级单例就是最简形态的 store。
import { reactive } from 'vue'
import { listProjects, listDomains, activateProject } from '../api.js'

const state = reactive({
  projects: [],
  activeProject: '',
  domains: [],
  activeDomain: '',
  loading: false,
  // UI 语言：'zh'（默认）| 'en'，持久化到 localStorage 跨刷新粘性
  locale: (() => {
    try { return localStorage.getItem('r2s_locale') || 'zh' } catch (e) { return 'zh' }
  })(),
})

// 切换 UI 语言并持久化
function setLocale(lang) {
  state.locale = lang
  try { localStorage.setItem('r2s_locale', lang) } catch (e) { /* 忽略隐私模式等异常 */ }
}

async function loadProjects() {
  const r = await listProjects()
  state.projects = r.projects || []
  const active = state.projects.find((p) => p.is_active)
  state.activeProject = active ? active.name : state.projects[0]?.name || ''
  if (state.activeProject) await loadDomains(state.activeProject)
  return state
}

async function loadDomains(project) {
  if (!project) {
    state.domains = []
    state.activeDomain = ''
    return
  }
  const r = await listDomains(project)
  state.domains = r.domains || []
  // C2：优先用服务端持久化的 active_domain 作默认选中（跨刷新粘性）；
  // 否则若当前选择在新项目里仍有效则保持（跨视图粘性），再退到第一个。
  const serverActive = r.active_domain
  if (serverActive && state.domains.includes(serverActive)) {
    state.activeDomain = serverActive
  } else if (!state.domains.includes(state.activeDomain)) {
    state.activeDomain = state.domains[0] || ''
  }
}

// 工作台下拉选项目：仅本地切换 + 拉领域，不写服务端激活
async function selectProject(name) {
  state.activeProject = name
  await loadDomains(name)
}

// 显式激活：写服务端 active_project，并刷新列表
async function setActiveProject(name) {
  await activateProject(name)
  await loadProjects()
}

export function useActiveContext() {
  return { state, loadProjects, loadDomains, selectProject, setActiveProject, setLocale }
}
