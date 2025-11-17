<template>
  <el-dialog v-model="dialogFormVisible" title="新增规则" center>
    <el-form ref="newRuleRef" :model="newRule" :rules="ruleRules" label-width="100px">
      <el-form-item label="规则名称" prop="name">
        <el-input v-model="newRule.name" show-word-limit maxlength="32" placeholder="请输入接口名称"/>
      </el-form-item>
      <el-form-item label="请求报文" prop="input_content">
        <el-input v-model="newRule.input_content" show-word-limit maxlength="64" placeholder="请输入请求报文">
        </el-input>
      </el-form-item>
      <el-form-item label="请求报文类型" prop="request_media_type">
        <el-input v-model="newRule.request_media_type" show-word-limit maxlength="64"
                  placeholder="请输入请求报文类型, 如application/json"/>
      </el-form-item>
      <el-form-item label="响应报文" prop="output_content">
        <el-input v-model="newRule.output_content" show-word-limit maxlength="64" placeholder="请输入响应报文">
        </el-input>
      </el-form-item>
      <el-form-item label="响应报文类型" prop="response_media_type">
        <el-input v-model="newRule.response_media_type" show-word-limit maxlength="64"
                  placeholder="请输入响应报文类型, 如application/json"/>
      </el-form-item>
      <el-form-item label="响应状态码" prop="status_code">
        <el-input v-model="newRule.status_code" show-word-limit maxlength="64" placeholder="请输入响应状态码, 如200"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button type="primary" @click="createNewRule">新增</el-button>
      <el-button @click="dialogFormVisible=false">取消</el-button>
    </template>
  </el-dialog>
  <el-page-header @back="goBack">
    <template #content>
      接口详情
    </template>
  </el-page-header>
  <el-descriptions title="接口基本信息" :column="4" style="padding: 10px">
    <el-descriptions-item label="接口ID">{{ interfaceInfo.id }}</el-descriptions-item>
    <el-descriptions-item label="名称">{{ interfaceInfo.name }}</el-descriptions-item>
    <el-descriptions-item label="URL">{{ interfaceInfo.url }}</el-descriptions-item>
    <el-descriptions-item label="方法">{{ interfaceInfo.method }}</el-descriptions-item>
    <el-descriptions-item label="描述">{{ interfaceInfo.description }}</el-descriptions-item>
    <el-descriptions-item label="规则数量">{{ total }}</el-descriptions-item>
    <el-descriptions-item>
      <el-button type="primary" @click="dialogFormVisible = true">添加规则</el-button>
    </el-descriptions-item>
  </el-descriptions>

  <el-table :data="ruleList.slice((currentPage-1)*pageSize,currentPage*pageSize)" stripe border
            :show-overflow-tooltip=true
            :tooltip-options="{ effect: 'light', placement: 'top', showArrow: true, width: '80px' }"
            :max-height="tableHeight" :header-cell-style="{textAlign: 'center'}" empty-text="暂无数据">
    <el-table-column label="Name" prop="name" align="center"></el-table-column>
    <el-table-column label="请求报文" prop="input_content">
      <template #default="scope">
        <div v-if="scope.row.editable">
          <el-input v-model="scope.row.input_content"></el-input>
        </div>
        <div v-else>{{ scope.row.input_content }}</div>
      </template>
    </el-table-column>
    <el-table-column label="响应报文" prop="output_content">
      <template #default="scope">
        <div v-if="scope.row.editable">
          <el-input v-model="scope.row.output_content"></el-input>
        </div>
        <div v-else>{{ scope.row.output_content }}</div>
      </template>
    </el-table-column>
    <el-table-column label="响应状态码" prop="status_code">
      <template #default="scope">
        <div v-if="scope.row.editable">
          <el-input v-model="scope.row.status_code"></el-input>
        </div>
        <div v-else>{{ scope.row.status_code }}</div>
      </template>
    </el-table-column>
    <el-table-column label="响应文本类型" prop="response_media_type">
      <template #default="scope">
        <div v-if="scope.row.editable">
          <el-input v-model="scope.row.response_media_type"></el-input>
        </div>
        <div v-else>{{ scope.row.response_media_type }}</div>
      </template>
    </el-table-column>
    <el-table-column label="操作">
      <template #default="scope">
        <el-button @click="editRule(scope.row)">
          <div v-if="scope.row.editable">保存</div>
          <div v-else>编辑</div>
        </el-button>
        <el-button type="danger" @click="deleteInterface(scope.row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :page-sizes="[10, 20, 50, 100]"
      :background="true"
      layout="total, sizes, prev, pager, next, jumper, ->"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      style="padding: 8px"
  />
</template>
<script setup lang="ts">
import {useRoute} from "vue-router";
import router from "@/router/index.js";
import {reactive, ref, onBeforeMount} from "vue";
import http from "@/http/index.js";
import type {FormInstance} from 'element-plus';
import {ElMessage} from 'element-plus';

const dialogFormVisible = ref(false);
const tableHeight = ref(500);
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

function refreshRuleList() {
  http.post("/rule/select", {interface_id: route.params.id}).then((res) => {
    if (res["code"] === "0") {
      ruleList.value = res["data"];
      total.value = res["data"].length;
    }
  });
}

onBeforeMount(() => {
  console.log(route.params)
  if (route.params.id) {
    http.post("/interface/select", route.params).then((res) => {
      if (res["code"] === "0") {
        interfaceInfo.value = res["data"][0];
      }
    });
    refreshRuleList()
  }
  tableHeight.value = document.documentElement.clientHeight - 310
})

const newRuleRef = ref<FormInstance>();
const newRule = ref({
  name: "",
  input_content: "",
  request_media_type: "application/json",
  output_content: "",
  response_media_type: "application/json",
  status_code: "200",
  interface_id: route.params.id
});
const ruleRules = reactive({
  name: [
    {required: true, message: '请输入名称', trigger: 'blur'},
    {min: 1, max: 32, message: '长度在 1 到 32 个字符', trigger: 'blur'},
  ],
  input_content: [
    {required: true, message: '请输入请求报文', trigger: 'blur'},
  ],
  output_content: [
    {required: true, message: '请选择响应报文', trigger: 'blur'},
  ],
});

function createNewRule() {
  if (!newRuleRef) return;
  newRuleRef.value.validate((valid) => {
    if (valid) {
      http.post("/rule/create", newRule.value).then((res) => {
        ElMessage({type: res["code"] === "0" ? 'success' : 'error', message: res["msg"]});
        if (res["code"] === "0") {
          dialogFormVisible.value = false
          refreshRuleList();
        }
      });
    }
  });
}
</script>
<style scoped>

</style>