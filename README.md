<p align="center">
	<img alt="logo" src="https://github.com/reddts/AI-Quiz/blob/main/show_pic/logo_120.png">
</p>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">Dash-FastAPI-Quiz</h1>
<h4 align="center">基于Dash+FastAPI的评测系统</h4>
<p align="center">
	<a href="https://gitee.com/insistence2022/dash-fastapi-admin/stargazers"><img src="https://gitee.com/insistence2022/dash-fastapi-admin/badge/star.svg?theme=dark"></a>
    <a href="https://github.com/insistence/Dash-FastAPI-Admin"><img src="https://img.shields.io/github/stars/insistence/Dash-FastAPI-Admin?style=social"></a>
	<a href="https://gitee.com/insistence2022/dash-fastapi-admin"><img src="https://img.shields.io/badge/DashFastAPIAdmin-v2.1.1-brightgreen.svg"></a>
	<a href="https://gitee.com/insistence2022/dash-fastapi-admin/blob/master/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>
    <img src="https://img.shields.io/badge/python-≥3.9-blue">
    <img src="https://img.shields.io/badge/MySQL-≥5.7-blue">
</p>

## 平台简介

AI-Quiz是一套基于python开发的在线评测系统，整体采用fast-api框架，后端通过api提供服务，后端的api采用python开发，便于接入AI接口，管理端采用python进行开发，前端，也就是用户端，采用uniapp开发，支持发布小程序和h5，没有PC端版本。ui采用图鸟UI 和taiwind。美观大方。
Dash-FastAPI-Admin是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。

* 管理前端采用Dash、feffery-antd-components、feffery-utils-components。
* 后端采用FastAPI、sqlalchemy、MySQL（PostgreSQL）、Redis、OAuth2 & Jwt。
* 权限认证使用OAuth2 & Jwt，支持多终端认证系统。
* 支持加载动态权限菜单，多方式轻松权限控制。
* 前端采用uniapp
* 支持多种AI接口，目前支持openai等，更多的ai接口接入中
* 支持多种测试量表，量表也在不断添加中。
* 特别鸣谢：<u>[insistence](https://github.com/insistence/Dash-FastAPI-Admin)</u> 。

## 后台管理功能

1.  用户管理：用户是系统操作者，该功能主要完成系统用户配置。
2.  角色管理：角色菜单权限分配、设置角色按机构进行数据范围权限划分。
3.  菜单管理：配置系统菜单，操作权限，按钮权限标识等。
4.  部门管理：配置系统组织机构（公司、部门、小组）。
5.  岗位管理：配置系统用户所属担任职务。
6.  字典管理：对系统中经常使用的一些较为固定的数据进行维护。
7.  参数管理：对系统动态配置常用参数。
8.  通知公告：系统通知公告信息发布维护。
9.  操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
10. 登录日志：系统登录日志记录查询包含登录异常。
11. 在线用户：当前系统中活跃用户状态监控。
12. 定时任务：在线（添加、修改、删除）任务调度包含执行结果日志。
13. 服务监控：监视当前系统CPU、内存、磁盘、堆栈等相关信息。
14. 缓存监控：对系统的缓存信息查询，命令统计等。
15. 系统接口：根据业务代码自动生成相关的api接口文档。

## 前端uniapp功能


## 演示图

<table>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%99%BB%E5%BD%95.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%BF%98%E8%AE%B0%E5%AF%86%E7%A0%81.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%94%A8%E6%88%B7%E7%AE%A1%E7%90%86.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E8%A7%92%E8%89%B2%E7%AE%A1%E7%90%86.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E8%8F%9C%E5%8D%95%E7%AE%A1%E7%90%86.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E9%83%A8%E9%97%A8%E7%AE%A1%E7%90%86.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%B2%97%E4%BD%8D%E7%AE%A1%E7%90%86.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%AD%97%E5%85%B8%E7%AE%A1%E7%90%86.png"/></td>
    </tr>	 
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%8F%82%E6%95%B0%E8%AE%BE%E7%BD%AE.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E6%93%8D%E4%BD%9C%E6%97%A5%E5%BF%97.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%99%BB%E5%BD%95%E6%97%A5%E5%BF%97.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%9C%A8%E7%BA%BF%E7%94%A8%E6%88%B7.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E5%AE%9A%E6%97%B6%E4%BB%BB%E5%8A%A1.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E6%9C%8D%E5%8A%A1%E7%9B%91%E6%8E%A7.png"/></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%BC%93%E5%AD%98%E7%9B%91%E6%8E%A7.png"/></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%BC%93%E5%AD%98%E5%88%97%E8%A1%A8.png"></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E7%B3%BB%E7%BB%9F%E6%8E%A5%E5%8F%A3.png"></td>
    </tr>
    <tr>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E9%A6%96%E9%A1%B5.png"></td>
        <td><img src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/%E4%B8%AA%E4%BA%BA%E8%B5%84%E6%96%99.png"/></td>
    </tr>
</table>

## 管理端在线体验
- *账号：admin*
- *密码：admin123*
- 演示地址：<a href="https://admin.ai-quiz.info">AI-Quiz管理中心<a>

## 项目开发及发布

```bash
# 克隆项目
git clone https://github.com/reddts/AI-Quiz.git

# 进入项目根目录
cd AI-Quiz

# 如果使用的是MySQL数据库，请执行以下命令安装项目依赖环境
pip3 install -r requirements.txt
# 如果使用的是PostgreSQL数据库，请执行以下命令安装项目依赖环境
pip3 install -r requirements-pg.txt
```

### 开发

#### 前端
```bash
# 进入前端目录
cd fastapi-frontend

# 配置应用信息
在.env.dev文件中配置应用开发模式的相关信息

# 运行前端
python3 app.py --env=dev
```

#### 后端API
```bash
# 进入后端目录
cd fastapi-backend

# 配置环境
1.在.env.dev文件中配置开发模式的数据库环境
2.在.env.dev文件中配置开发模式的redis环境

# 运行sql文件
1.新建数据库dash-fastapi(默认，可修改)
2.如果使用的是MySQL数据库，使用命令或数据库连接工具运行sql文件夹下的dash-fastapi.sql；如果使用的是PostgreSQL数据库，使用命令或数据库连接工具运行sql文件夹下的dash-fastapi-pg.sql

# 运行后端
python3 app.py --env=dev
```

### 发布

本应用发布建议使用nginx部署，nginx代理配置参考如下：

```bash
server {
    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header REMOTE-HOST $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:8088/;
    }

    location /prod-api {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header REMOTE-HOST $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_pass http://127.0.0.1:9099/;
        rewrite ^/prod-api/(.*)$ /$1 break;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   html;
    }
}
```

#### 前端
```bash
# 进入前端目录
cd fastapi-frontend

# 配置应用信息
在.env.prod文件中配置应用发布的相关信息，注意：APP_BASE_URL需要配置为nginx代理的地址，例如上面的nginx代理监听的是8000端口，则APP_BASE_URL需要配置为http://127.0.0.1:8000

# 运行前端
python3 wsgi.py --env=prod
```

#### 后端
```bash
# 进入后端目录
cd dash-fastapi-backend

# 配置环境
1.在.env.prod文件中配置生产模式的数据库环境
2.在.env.prod文件中配置生产模式的redis环境

# 运行sql文件
1.新建数据库dash-fastapi(默认，可修改)
2.如果使用的是MySQL数据库，使用命令或数据库连接工具运行sql文件夹下的dash-fastapi.sql；如果使用的是PostgreSQL数据库，使用命令或数据库连接工具运行sql文件夹下的dash-fastapi-pg.sql

# 运行后端
python3 app.py --env=prod
```

### 访问
```bash
# 默认账号密码
账号：admin
密码：admin123

# 浏览器访问
地址：http://127.0.0.1:8088
```

## 交流与赞助
如果有对本项目及FastAPI和AI感兴趣的朋友，欢迎入群交流。如果你觉得这个项目帮助到了你，你可以请作者喝杯咖啡表示鼓励☕。扫描下面微信二维码添加微信备注AI-Quiz即可进群。
<table>
    <tr>
        <td style="width: 50%"><img alt="zanzhu_wx" src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/zanzhu_wx.jpg"></td>
        <td style="width: 50%"><img alt="zanzhu_zfb" src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/zanzhu_zfb.jpg"></td>
    </tr>
    <tr>
        <td style="width: 50%"><img alt="zsxq" src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/zsxq.jpg"></td>
        <td style="width: 50%"><img alt="dashzsxq" src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/dashzsxq.jpg"></td>
    </tr>
    <tr>
        <td style="width: 50%"><img alt="wxcode" src="https://gitee.com/insistence2022/dash-fastapi-admin/raw/master/demo-pictures/wxcode.jpg"></td>
    </tr>
</table>