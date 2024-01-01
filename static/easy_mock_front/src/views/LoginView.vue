<template>
  <el-form ref="formRef" :model="form" :rules="rules" label-width="60px" label-position="left" style="margin: auto;">
    <el-form-item label="ID" prop="id">
      <el-input v-model="form.id" placeholder="请输入ID"></el-input>
    </el-form-item>
    <el-form-item label="Name" prop="name">
      <el-input v-model="form.name" placeholder="请输入Name"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm()">登录</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import http from '@/http'
import { useRouter } from 'vue-router'

const router = useRouter()
interface UserForm {
  id: string,
  name: string
}

const formRef = ref<FormInstance>()
const form = reactive<UserForm>({
  id: '',
  name: ''
})

const rules = reactive<FormRules<UserForm>>({
  id: [
    { required: true, message: '请输入ID', trigger: 'blur' },
    { min: 1, max: 32, message: '长度在 1 到 32 个字符', trigger: 'blur' },
  ],
  name: [
    { required: true, message: '请输入Name', trigger: 'blur' },
    { min: 1, max: 32, message: '长度在 1 到 32 个字符', trigger: 'blur' },
  ]
})

const submitForm = function () {
  if (!formRef) return;
  formRef.value.validate((valid) => {
    if (valid) {
      http.post('/login', form).then(res => {
        if (res['code'] === 0)
          router.push('/');
      });
    }
  })
}
</script>
<style scoped></style>