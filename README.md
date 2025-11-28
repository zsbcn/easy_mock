# 简介
本项目用于实现一个支持多人公用的的http接口模拟桩使用和管理服务（目前仅计划覆盖自己的使用场景，功能比较单一，会慢慢完善）
# 开发环境
前端: _暂未开发_

后端: python 3.13
* fastapi
* loguru
* pydantic-settings
* python-dotenv
* pyyaml
* redis
* sqlalchemy
* starlette-session
* uvicorn 

数据库: sqlite3

# 快速启动
## 后端
0. 本地已配置好[uv](https://uv.doczh.com/getting-started/).
1. 把代码下载到本地, 在命令行中切换到代码根目录下，运行`uv sync`安装项目依赖
2. 使用命令生成测试用证书`openssl req -x509 -nodes -days 365 -newkey rsa:4096 -keyout server.key -out server.crt -subj "/C=CN/ST=YourState/L=YourCity/O=YourOrg/CN=127.0.0.1"`, 把生成的文件放到src/conf/ssl目录下
3. 切到src目录下, 命令行输入`uv run main.py`即可启动服务
如图所示即后端项目启动成功
![image](https://github.com/zsbcn/easy_mock/assets/40849967/3255ddc0-8474-4cdf-bdcf-1e988c3f1ba1)

## 前端
_暂未开发_
