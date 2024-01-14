import {createApp} from 'vue'
import App from './App.vue'
import router from './router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

import http from '@/http/index';

const app = createApp(App)

app.use(router)
app.use(ElementPlus, {
  locale: zhCn,
})
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

async function getUser() {
  const res = await http.post('/user/select', {})
  if (res.code !== "0") {
    await router.push('/login')
  }
}

getUser().then(r => {
})
app.mount('#app')

