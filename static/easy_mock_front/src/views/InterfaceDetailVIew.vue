<script setup lang="ts">
import {useRoute} from "vue-router";
import router from "@/router/index.js";
import {reactive, ref, onBeforeMount} from "vue";
import http from "@/http/index.js";
import type {FormInstance} from 'element-plus';
import {ElMessage} from 'element-plus';

const dialogFormVisible = ref(false);
const tableHeight = ref(300);
const currentPage = ref(1);
const total = ref(0);
const pageSize = ref(10);

const route = useRoute();
const interfaceInfo = ref({
  id: "",
  name: "",
  url: "",
  method: "",
  description: "",
});
const ruleList = ref([]);

const goBack = () => {
  router.push('/')
}

onBeforeMount(() => {
  console.log(route.params)
  if (route.params.id) {
    http.post("/interface/select", route.params).then((res) => {
      if (res["code"] === 0) {
        interfaceInfo.value = res["data"][0];
      }
    });
  }
})

const newRuleRef = ref<FormInstance>();
const newRule = ref({
  inputContent: "",
  outContent: "",
  contentType: "",
  statusCode: ""
});
const ruleRules = reactive({
  name: [
    {required: true, message: '请输入名称', trigger: 'blur'},
    {min: 1, max: 32, message: '长度在 1 到 32 个字符', trigger: 'blur'},
  ],
  url: [
    {required: true, message: '请输入URL', trigger: 'blur'},
  ],
  method: [
    {required: true, message: '请选择请求方式', trigger: 'blur'},
  ],
});

function createNewRule() {
  if (!newRuleRef) return;
  newRuleRef.value.validate((valid) => {
    if (valid) {
      http.post("/rule/create", newRule.value).then((res) => {
        if (res["code"] === 0) {
          ElMessage.success(res["msg"]);
          refreshInterfaceList();
        }
      });
    }
  });
}
</script>

<template>
  <el-page-header @back="goBack">
    <template #content>
      接口详情
    </template>
  </el-page-header>
  <el-descriptions title="接口基本信息" style="padding: 10px">
    <el-descriptions-item label="接口ID">{{ interfaceInfo.id }}</el-descriptions-item>
    <el-descriptions-item label="名称">{{ interfaceInfo.name }}</el-descriptions-item>
    <el-descriptions-item label="URL">{{ interfaceInfo.url }}</el-descriptions-item>
    <el-descriptions-item label="方法">{{ interfaceInfo.method }}</el-descriptions-item>
    <el-descriptions-item label="描述">{{ interfaceInfo.description }}</el-descriptions-item>
    <el-descriptions-item label="规则数量">{{ interfaceInfo.id }}</el-descriptions-item>
  </el-descriptions>
  <el-table :data="ruleList.slice((currentPage-1)*pageSize,currentPage*pageSize)" stripe border
            tooltip-effect="light" :show-overflow-tooltip=true :max-height="tableHeight"
            :header-cell-style="{textAlign: 'center'}" empty-text="暂无数据">
    <el-table-column label="规则ID" prop="id" min-width="20%" align="center"></el-table-column>
    <el-table-column label="请求报文" prop="name">
      <template #default="scope">
        <div v-if="scope.row.editable">
          <el-input v-model="scope.row.name"></el-input>
        </div>
        <div v-else>{{ scope.row.name }}</div>
      </template>
    </el-table-column>
    <el-table-column label="响应报文" prop="url">
      <template #default="scope">
        <div v-if="scope.row.editable">
          <el-input v-model="scope.row.url"></el-input>
        </div>
        <div v-else>{{ scope.row.url }}</div>
      </template>
    </el-table-column>
    <el-table-column label="响应状态码" prop="description">
      <template #default="scope">
        <div v-if="scope.row.editable">
          <el-input v-model="scope.row.description"></el-input>
        </div>
        <div v-else>{{ scope.row.description }}</div>
      </template>
    </el-table-column>
    <el-table-column label="操作">
      <template #default="scope">
        <el-button @click="editInterface(scope.row)">
          <div v-if="scope.row.editable">保存</div>
          <div v-else>编辑</div>
        </el-button>
        <el-button @click="$router.push('/detail/' + scope.row.id)">查看</el-button>
        <el-button type="danger" @click="deleteInterface(scope.row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<style scoped>

</style>