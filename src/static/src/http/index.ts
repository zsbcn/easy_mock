import axios from "axios";
import {ElMessage} from "element-plus";

const http = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// 请求拦截器
http.interceptors.request.use(
  config => {
    // 在发送请求之前执行该函数，可以通过config对象来修改请求参数
    // 例如：添加token、设置请求头等
    return config;
  },
  error => {
    // 发送请求出错时，可以通过该函数来处理错误
    Promise.reject(error).then(r => {
    });
  }
);

// 响应拦截器
http.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    // 通过该函数来处理异常响应
    // 判断状态码，显示不同的错误信息
    if (error.response && error.response.status) {
      switch (error.response.status) {
        case 401:
          // 未登录，跳转到登录页面
          ElMessage.error("请先登录");
          break;
        case 403:
          ElMessage.error("没有权限");
          break;
        default:
          ElMessage.error("请求错误");
      }
    } else {
      ElMessage.error("服务器错误");
    }
    return Promise.reject(error);
  }
);
export default http;