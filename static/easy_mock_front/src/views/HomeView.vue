<template>
  <el-dialog v-model="dialogFormVisible" title="新增接口" center>
    <el-form ref="newInterfaceRef" :model="newInterface" :rules="interfaceRules" label-width="80px">
      <el-form-item label="接口名称" prop="name">
        <el-input v-model="newInterface.name" show-word-limit maxlength="32" placeholder="请输入接口名称"/>
      </el-form-item>
      <el-form-item label="接口地址" prop="url">
        <el-input v-model="newInterface.url" show-word-limit maxlength="64"
                  placeholder="请输入接口地址, 样例:/xwx1234567/xxx">
        </el-input>
      </el-form-item>
      <el-form-item label="请求方式" prop="method">
        <el-select v-model="newInterface.method" placeholder="请选择请求方式">
          <el-option v-for="item in methods" :key="item.key" :label="item.value" :value="item.key"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="接口描述" prop="params">
        <el-input v-model="newInterface.description" type="textarea" rows="5" resize="none" show-word-limit
                  maxlength="200" placeholder="请输入接口描述"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button type="primary" @click="createNewInterface">新增</el-button>
      <el-button @click="dialogFormVisible=false">取消</el-button>
    </template>
  </el-dialog>

  <el-form ref="interfaceRef" :model="interfaceInfo" label-width="80px" :inline="true">
    <el-form-item label="接口名称" prop="name" style="width: 300px">
      <el-input v-model="interfaceInfo.name" show-word-limit maxlength="32" placeholder="请输入接口名称"/>
    </el-form-item>
    <el-form-item label="接口地址" prop="url" style="width: 500px;">
      <el-input v-model="interfaceInfo.url" show-word-limit maxlength="64"
                placeholder="请输入接口地址, 样例:/xwx1234567/xxx">
      </el-input>
    </el-form-item>
    <el-form-item label="请求方式" prop="method">
      <el-select v-model="interfaceInfo.method" :default-first-option="true">
        <el-option key="ALL" label="ALL" value=""></el-option>
        <el-option v-for="item in methods" :key="item.key" :label="item.value" :value="item.key"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="refreshInterfaceList">查询</el-button>
    </el-form-item>
    <el-form-item>
      <el-button @click="resetInterfaceInfo">重置</el-button>
    </el-form-item>
    <el-form-item>
      <el-button @click="dialogFormVisible = true">新建</el-button>
    </el-form-item>
  </el-form>

  <el-table :data="interfaceList.slice((currentPage-1)*pageSize,currentPage*pageSize)" stripe border
            tooltip-effect="light" :show-overflow-tooltip=true :max-height="tableHeight"
            :header-cell-style="{textAlign: 'center'}" empty-text="暂无数据">
    <el-table-column label="ID" prop="id" width="100px" align="center"/>
    <el-table-column label="名称" prop="name">
      <template #default="scope">
        <div v-if="scope.row.editable">
          <el-input v-model="scope.row.name"></el-input>
        </div>
        <div v-else>{{ scope.row.name }}</div>
      </template>
    </el-table-column>
    <el-table-column label="URL" prop="url">
      <template #default="scope">
        <div v-if="scope.row.editable">
          <el-input v-model="scope.row.url"></el-input>
        </div>
        <div v-else>{{ scope.row.url }}</div>
      </template>
    </el-table-column>
    <el-table-column label="方法" prop="method" width="100px" align="center">
      <template #default="scope">
        <div v-if="scope.row.editable">
          <el-select v-model="scope.row.method" placeholder="请选择请求方式">
            <el-option v-for="item in methods" :key="item.key" :label="item.value" :value="item.key"></el-option>
          </el-select>
        </div>
        <div v-else>{{ scope.row.method }}</div>
      </template>
    </el-table-column>
    <el-table-column label="描述" prop="description">
      <template #default="scope">
        <div v-if="scope.row.editable">
          <el-input v-model="scope.row.description"></el-input>
        </div>
        <div v-else>{{ scope.row.description }}</div>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="230px" align="center">
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
  <el-config-provider :locale="zhCn">
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
  </el-config-provider>
</template>
<script lang="ts" setup>

import {onBeforeMount, ref, reactive} from 'vue';
import http from '@/http';
import {ElMessageBox, FormInstance} from 'element-plus';
import {ElMessage} from 'element-plus';
import zhCn from "element-plus/es/locale/lang/zh-cn";

const dialogFormVisible = ref(false);
const tableHeight = ref(300);
const currentPage = ref(1);
const total = ref(0);
const pageSize = ref(10);

const handleSizeChange = (val: number) => {
  currentPage.value = 1;
  console.log(`${val} items per page`)
}
const handleCurrentChange = (val: number) => {
  console.log(`current page: ${val}`)
}

const methods = ref([]);

const interfaceRules = reactive({
  name: [
    {required: true, message: '请输入名称', trigger: 'blur'},
    {min: 1, max: 32, message: '长度在 1 到 32 个字符', trigger: 'blur'},
  ],
  url: [
    {required: true, message: '请输入URL', trigger: 'blur'},
    {min: 1, max: 64, message: '长度在 1 到 64 个字符', trigger: 'blur'},
  ],
  method: [
    {required: true, message: '请选择请求方式', trigger: 'blur'},
  ],
});


const newInterfaceRef = ref<FormInstance>();
const interfaceRef = ref<FormInstance>();
const newInterface = ref({
  name: "",
  url: "",
  method: "",
  description: "",
  editable: false
});

const interfaceInfo = ref({
  name: "",
  url: "",
  method: ""
});

function resetInterfaceInfo() {
  interfaceRef.value.clearValidate();
  interfaceRef.value.resetFields();
  refreshInterfaceList();
}

function createNewInterface() {
  if (!newInterfaceRef) return;
  newInterfaceRef.value.validate((valid) => {
    if (valid) {
      http.post("/interface/create", newInterface.value).then((res) => {
        ElMessage({type: res["code"] === 0 ? "success" : "error", message: res["msg"]});
        if (res["code"] === 0) {
          dialogFormVisible.value = false;
          refreshInterfaceList();
        }
      });
    }
  });
}


function editInterface(data) {
  data.editable = !data.editable;
  if (data.editable === false) {
    http.post('/interface/update', data).then((res) => {
      ElMessage({type: res["code"] === 0 ? 'success' : 'error', message: res["msg"]});
      if (res["code"] === 0) {
        refreshInterfaceList();
      }
    })
  }
}


function deleteInterface(id) {
  ElMessageBox.confirm(
      '确认删除此接口吗？',
      '警告',
      {
        autofocus: false,
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning',
      }
  ).then(() => {
    http.post('/interface/delete', {id: id}).then((res) => {
      if (res["code"] === 0) {
        ElMessage({
          type: 'success',
          message: '接口删除成功',
        })
        refreshInterfaceList();
      }
    })
  }).catch(() => {
    ElMessage({
      type: 'info',
      message: '取消删除接口',
    })
  })
}

const interfaceList = ref([]);

function refreshInterfaceList() {
  http.post('/interface/select', interfaceInfo.value).then((res) => {
    interfaceList.value = res.data;
    currentPage.value = 1;
    total.value = interfaceList.value.length
  })
}

function getMethodList() {
  http.get('/config/get?group=method&key=',
  ).then((res) => {
    methods.value = res.data;
    newInterface.value.method = methods.value[0].key;
  })
}

onBeforeMount(() => {
  getMethodList();
  refreshInterfaceList();
  tableHeight.value = document.documentElement.clientHeight - 60 - 60 - 60
})
</script>

<style scoped>
</style>
   
   