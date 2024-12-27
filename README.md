<p align="center">
	<img alt="logo" src="https://github.com/reddts/AI-Quiz/blob/main/show_pic/logo_120.png">
</p>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">AI-Quiz</h1>
<h4 align="center">本平台是采FastApi框架的python泛化人工智能平台，这是一系列人工智能分析平台的基础，AI-Quiz是基于这个平台打造的一款心理评测和趣味测试小程序，通过科学的量表帮助您熟悉自己，了解自己，同时引入了AI接口，帮助您分析目前现状，为迷茫的你指引方向</h4>
<p align="center">
	<a href="https://github.com/reddts/AI-Quiz"><img src="https://img.shields.io/github/stars/reddts/AI-Quiz?style=social"></a>
	<a href="https://github.com/reddts/AI-Quiz"><img src="https://img.shields.io/badge/AI__Quiz-v1.0.0-brightgreen.svg"></a>
	<a href="https://github.com/reddts/AI-Quiz/blob/main/LICENSE"><img src="https://img.shields.io/github/license/mashape/apistatus.svg"></a>
    <img src="https://img.shields.io/badge/python-≥3.10.15-blue">
    <img src="https://img.shields.io/badge/MySQL-≥5.7-blue">
</p>

## 平台简介

本平台是一款基于 Python 开发的通用人工智能平台，采用 FastAPI 框架，专注于智能分析功能的构建，是未来多款智能产品的技术基础。AI-Quiz 是平台上推出的一款核心应用，定位于心理测试与趣味测试领域，通过科学化和智能化的方式，帮助用户更好地了解自己。

### 心理测试
AI-Quiz 通过整合专业的心理学量表和严谨的数据分析模型，提供多种科学心理评测，例如人格测试、情绪状态评估、压力与应对能力分析等。这些测试基于心理学研究和权威数据支持，精准解析用户的心理状态。通过回答量身定制的问题，用户可以深入探索自己的内在性格、潜在优势与改善方向。AI 还可以根据评测结果提供具体建议，帮助用户制定发展目标或应对策略。

### 趣味测试
在提供科学评测的基础上，AI-Quiz 还加入了多种趣味测试功能，让用户在娱乐中发现自我。这些测试涵盖职业匹配、性格色彩、社交能力评估等轻松主题，结果生动有趣，容易被理解和分享。通过趣味化的内容设计，平台降低了心理测试的门槛，让测试过程更加贴近日常生活，同时激发用户的探索欲望。

### 技术架构与用户体验
AI-Quiz 的后端基于 FastAPI 开发，通过高效 API 服务支撑心理与趣味测试功能，支持与多种 AI 接口对接，提升分析精度和个性化体验。管理端同样采用 Python 构建，便于后台数据管理与扩展。用户端采用 UniApp 开发，支持小程序与 H5 平台，随时随地接入服务。
UI 设计结合了图鸟 UI 和 Tailwind CSS，界面清新简约，注重用户体验，既具有专业性又不失趣味性。

AI-Quiz 以科学的心理学基础、智能化的分析方式和趣味化的内容设计，为用户提供一个自我探索和成长的全新途径，是心理测试与趣味测试领域的创新产品。

* 管理前端采用Dash、feffery-antd-components、feffery-utils-components。
* 后端采用FastAPI、sqlalchemy、MySQL（PostgreSQL）、Redis、OAuth2 & Jwt。
* 权限认证使用OAuth2 & Jwt，支持多终端认证系统。
* 支持加载动态权限菜单，多方式轻松权限控制。
* 前端采用uniapp
* 支持多种AI接口，目前支持openai等，更多的ai接口接入中
* 支持多种测试量表，量表也在不断添加中。
* 特别鸣谢：<u>[insistence](https://github.com/insistence/Dash-FastAPI-Admin)</u> 提供的底盘，以及造轮子的前辈们 。

## 版本更迭记录
* v1.0.0 完成基本框架
* v1.0.1 完成后台量表数据管理


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
16. 会员管理：使用系统的会员进行管理
17. 量表管理：管理量表，增加修改删除量表及其关联的表单项

## 前端uniapp功能
开发中

## 开发进度
| 序号 | 开发内容 | 完成情况 | 备注 |
| --- | --- | --- | --- |
| 1 | 后台框架的修改适配 | 已完成 |   |
| 2 | 会员管理功能 | 开发中 |   |
| 3 | 量表管理功能 | 待开发 |   |
| 4 | AI接口的配置 | 待开发 |   |
| 5 | AI接口的开发 | 待开发 |   |
| 6 | 支付功能的开发 | 待开发 |   |
| 7 | 前端API接口框架开发 | 待开发 |   |
| 8 | 前端API接口功能开发 | 待开发 |   |
| 9 | 前端界面的开发 | 待开发 |   |


## 演示图

<table>
    <tr>
        <td><img src="https://github.com/reddts/AI-Quiz/blob/main/show_pic/logo_120.png"/></td>
        <td><img src="https://github.com/reddts/AI-Quiz/blob/main/show_pic/logo_120.png"/></td>
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
1.新建数据库ai-quiz(默认，可修改)
2.如果使用的是MySQL数据库，使用命令或数据库连接工具运行sql文件夹下的ai-quiz.sql；如果使用的是PostgreSQL数据库，使用命令或数据库连接工具运行sql文件夹下的ai-quiz-pg.sql

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
cd fastapi-backend

# 配置环境
1.在.env.prod文件中配置生产模式的数据库环境
2.在.env.prod文件中配置生产模式的redis环境

# 运行sql文件
1.新建数据库ai-quiz(默认，可修改)
2.如果使用的是MySQL数据库，使用命令或数据库连接工具运行sql文件夹下的ai-quiz.sql；如果使用的是PostgreSQL数据库，使用命令或数据库连接工具运行sql文件夹下的ai-quiz-pg.sql

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
        <td style="width: 50%"><img alt="wx" src="https://github.com/reddts/AI-Quiz/blob/main/show_pic/wx.jpg"></td>
        <td style="width: 50%"><img alt="zfb" src="https://github.com/reddts/AI-Quiz/blob/main/show_pic/zfb.jpg"></td>
    </tr>
</table>