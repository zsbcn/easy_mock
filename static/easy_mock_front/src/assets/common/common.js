import http from '@/http/index.js'

export async function getUserInfo(userId = '') {
  const res = await http.post('/user/select', {id: userId});
  if (res['code'] !== 0) {
    return null;
  }
  return res['data'];
}