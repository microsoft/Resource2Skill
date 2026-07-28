<template>
  <el-container style="height: 100vh">
    <el-header
      style="
        display: flex;
        align-items: center;
        background: #1f3a5f;
        color: #fff;
        padding: 0 16px;
      "
    >
      <span style="font-size: 18px; font-weight: 600; margin-right: 24px"
        >Resource2Skill WebUI</span
      >
      <el-menu
        mode="horizontal"
        :default-active="current"
        background-color="#1f3a5f"
        text-color="#fff"
        active-text-color="#ffd04b"
        @select="onSelect"
      >
        <el-menu-item index="home">首页</el-menu-item>
        <el-menu-item index="projects">项目与 Domain 管理</el-menu-item>
        <el-menu-item index="tasks">任务中心</el-menu-item>
        <el-menu-item index="agent">Agent 执行台</el-menu-item>
        <el-menu-item index="fixtures">素材管理</el-menu-item>
        <el-menu-item index="distill">蒸馏工作台</el-menu-item>
        <el-menu-item index="repo">产物仓库</el-menu-item>
        <el-menu-item index="llm">LLM 配置</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <Overview v-if="current === 'home'" @navigate="onSelect" />
      <ProjectsDomains v-if="current === 'projects'" />
      <TaskCenter v-else-if="current === 'tasks'" />
      <AgentConsole v-else-if="current === 'agent'" />
      <Fixtures v-else-if="current === 'fixtures'" />
      <DistillWorkbench v-else-if="current === 'distill'" />
      <ArtifactRepo v-else-if="current === 'repo'" />
      <LlmConfig v-else-if="current === 'llm'" />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref } from 'vue'
import Overview from './views/Overview.vue'
import LlmConfig from './views/LlmConfig.vue'
import ProjectsDomains from './views/ProjectsDomains.vue'
import Fixtures from './views/Fixtures.vue'
import DistillWorkbench from './views/DistillWorkbench.vue'
import TaskCenter from './views/TaskCenter.vue'
import AgentConsole from './views/AgentConsole.vue'
import ArtifactRepo from './views/ArtifactRepo.vue'

const current = ref('home')
function onSelect(key) {
  current.value = key
}
</script>
