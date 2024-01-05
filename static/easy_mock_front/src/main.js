import {createApp} from 'vue'
import App from './App.vue'
import router from './router'

import ElementPlus, {ElMessage} from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import {getUserInfo} from '@/assets/common/common.js'
import './assets/css/global.css'

const app = createApp(App)

app.use(router)
app.use(ElementPlus)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

const userInfo = await getUserInfo()
if (userInfo === null) {
  ElMessage.error('请先登录')
  router.push("/login")
}

app.mount('#app')