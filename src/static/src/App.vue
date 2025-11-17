<script setup lang="ts">
import {RouterView} from 'vue-router'
import router from "@/router/index.js";
import http from '@/http/index';
import {ElMessage} from "element-plus";


function exitSystem() {
  http.post("/logout")
  ElMessage.success("退出成功")
  router.push('/login')
}

</script>

<template>
  <el-container>
    <el-header style="display: flex; justify-content: space-between; align-items: center">
      <label style="font-family: 'Microsoft Sans Serif';font-size:40px">easy-mock</label>
      <el-button icon="SwitchButton" size="small" @click="exitSystem"/>
    </el-header>
    <el-main style="padding: 10px">
      <RouterView/>
    </el-main>
  </el-container>
</template>


<style scoped>

</style>
