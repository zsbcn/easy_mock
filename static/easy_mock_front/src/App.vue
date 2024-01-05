<script setup>
import {RouterView, useRoute} from 'vue-router'
import {onBeforeMount, ref} from "vue";
import router from "@/router/index.js";

const route = useRoute();

onBeforeMount(() => {
  router.push('/')
})

</script>

<template>
  <el-container>
    <el-header style="background: cadetblue;">
      <label style="font-family: 'Microsoft Sans Serif';font-size:40px">easy-mock</label>
    </el-header>
    <el-main style="padding: 10px">
      <RouterView/>
    </el-main>
  </el-container>
</template>

<style scoped>
</style>
