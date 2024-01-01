<template>
  <el-row :gutter="20">
    <el-col :span="12">
      <el-form ref="newInterfaceRef" :model="newInterface" :rules="rules" label-width="100px">
        <el-form-item label="接口名称" prop="name">
          <el-input v-model="newInterface.name" placeholder="请输入接口名称" />
        </el-form-item>
        <el-form-item label="接口地址" prop="url">
          <el-input v-model="newInterface.url" placeholder="请输入接口地址" />
        </el-form-item>
        <el-form-item label="请求方式" prop="method">
          <el-select v-model="newInterface.method" placeholder="请选择请求方式">
            <el-option label="GET" value="GET"></el-option>
            <el-option label="POST" value="POST"></el-option>
            <el-option label="PUT" value="PUT"></el-option>
            <el-option label="DELETE" value="DELETE"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="接口描述" prop="params">
          <el-input v-model="newInterface.description" placeholder="请输入请求参数" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="createNewInterface">新增</el-button>
        </el-form-item>
      </el-form>
    </el-col>
    <el-col :span="12">
      <el-input></el-input>
    </el-col>
  </el-row>

  <el-table :data="interfaceList" empty-text="暂无数据">
    <el-table-column label="ID" prop="id"></el-table-column>
    <el-table-column label="名称" prop="name"></el-table-column>
    <el-table-column label="URL" prop="url"></el-table-column>
    <el-table-column label="方法" prop="method"></el-table-column>
    <el-table-column label="描述" prop="description"></el-table-column>
  </el-table>
</template>
<script lang="ts" setup>

import { onBeforeMount, ref, reactive } from 'vue';
import http from '@/http';
import type { FormInstance } from 'element-plus';
import { ElMessage } from 'element-plus';

const rules = reactive({
  name: [
    { required: true, message: '请输入名称', trigger: 'blur' },
    { min: 1, max: 32, message: '长度在 1 到 32 个字符', trigger: 'blur' },
  ],
  url: [
    { required: true, message: '请输入URL', trigger: 'blur' },
  ],
  method: [
    { required: true, message: '请选择请求方式', trigger: 'blur' },
  ],
});
const newInterfaceRef = ref<FormInstance>();
const newInterface = ref({
  name: "",
  url: "",
  method: "",
  description: ""
});

function createNewInterface() {
  if (!newInterfaceRef) return;
  newInterfaceRef.value.validate((valid) => {
    if (valid) {
      http.post("/interface/create", newInterface.value).then((res) => {
        if (res["code"] === 0) {
          ElMessage.success("新增成功");
          refreshInterfaceList();
        }
      });
    }
  });
}

const interfaceList = ref([]);

onBeforeMount(() => {
  refreshInterfaceList();
})

function refreshInterfaceList() {
  http.post('/interface/select', {}).then((res) => {
    interfaceList.value = res.data;
  })
}
</script>

<style scoped></style>
   
   