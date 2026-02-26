# TFMS Forum

一个功能完善的论坛系统for TFMS，支持用户认证、帖子管理、评论系统、点赞功能和主题切换等功能。

该项目已运行在DCP Studios服务器上，地址为：https://tfms.forum.dcpstudios.top

本项目全程Vibe Coding，AI恐怖如斯

## 功能特性

### 用户功能
- 用户注册和登录
- 个人信息管理（实名、学号、入学年份）
- 发布帖子（支持Markdown格式）
- 浏览和搜索帖子
- 评论帖子
- 点赞帖子和评论
- 查看通知
- 主题切换（亮色/暗色）

### 管理员功能
- 帖子审核管理
- 用户管理（修改用户信息、删除用户）
- 分类管理（增删改分类）
- 查看所有待审核帖子

### 其他特性
- 响应式设计，支持移动端
- 实时更新帖子列表
- 热门帖子和最新帖子推荐
- 分类浏览
- 分页功能

## 技术栈

### 后端
- **框架**: Flask
- **数据库**: MySQL
- **ORM**: SQLAlchemy
- **认证**: JWT + Session
- **跨域**: Flask-CORS

### 前端
- **框架**: Vue 3
- **路由**: Vue Router
- **状态管理**: Vuex
- **HTTP客户端**: Axios
- **Markdown渲染**: Marked
- **样式**: CSS3 + CSS变量

## 项目结构

```
TFMSForum/
├── backend/                 # 后端Flask应用
│   ├── app/
│   │   ├── __init__.py     # 应用初始化
│   │   ├── config.py        # 配置文件
│   │   ├── models.py        # 数据库模型
│   │   ├── routes/          # 路由模块
│   │   │   ├── auth.py      # 认证路由
│   │   │   ├── posts.py     # 帖子路由
│   │   │   ├── comments.py  # 评论路由
│   │   │   ├── categories.py # 分类路由
│   │   │   ├── admin.py     # 管理员路由
│   │   │   └── notifications.py # 通知路由
│   │   └── services/       # 业务逻辑层
│   │       └── post_service.py
│   ├── init_db.py          # 数据库初始化脚本
│   └── requirements.txt     # Python依赖
├── frontend/               # 前端Vue应用
│   ├── src/
│   │   ├── api/            # API调用封装
│   │   ├── components/      # Vue组件
│   │   │   └── Layout/    # 布局组件
│   │   ├── router/          # 路由配置
│   │   ├── store/           # Vuex状态管理
│   │   ├── views/           # 页面组件
│   │   ├── App.vue          # 根组件
│   │   └── main.js          # 入口文件
│   ├── package.json        # Node依赖
│   └── vite.config.js     # Vite配置
└── README.md              # 项目说明文档
```

## 安装和运行

### 后端安装

1. 克隆项目
```bash
git clone https://github.com/xksnetcbs/TFMSForum.git
cd TFMSForum/backend
```

2. 创建虚拟环境并安装依赖
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

3. 配置数据库
编辑 `app/config.py` 文件，设置数据库连接：
```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost:3306/tfms_forum"
```

4. 初始化数据库
```bash
python init_db.py
```

5. 启动后端服务
```bash
python run.py
```

后端服务将在 `http://localhost:5000` 运行。

### 前端安装

1. 进入前端目录
```bash
cd frontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
npm run dev
```

前端服务将在 `http://localhost:5173` 运行。

## 配置说明

### 环境变量

后端支持以下环境变量：

- `TFMSFORUM_SECRET_KEY`: Flask密钥（默认: dev-secret-key）
- `TFMSFORUM_DATABASE_URI`: 数据库连接字符串

### CORS配置

默认情况下，后端配置为接受来自 `https://tfms.fback.dcpstudios.top` 的请求。如需修改，请编辑 `backend/app/__init__.py`：

```python
CORS(app, resources={r"/api/*": {"origins": "your-domain.com"}}, supports_credentials=True)
```

## API文档

### 认证接口
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `GET /api/auth/me` - 获取当前用户信息
- `PUT /api/auth/me` - 更新用户信息

### 帖子接口
- `GET /api/posts` - 获取帖子列表
- `POST /api/posts` - 创建帖子（需要登录）
- `GET /api/posts/:id` - 获取帖子详情
- `POST /api/posts/:id/like` - 点赞帖子（需要登录）
- `DELETE /api/posts/:id/like` - 取消点赞（需要登录）

### 评论接口
- `GET /api/posts/:post_id/comments` - 获取评论列表
- `POST /api/posts/:post_id/comments` - 创建评论（需要登录）
- `DELETE /api/comments/:id` - 删除评论（需要登录）
- `POST /api/comments/:id/like` - 点赞评论（需要登录）
- `DELETE /api/comments/:id/like` - 取消点赞（需要登录）

### 分类接口
- `GET /api/categories` - 获取分类列表
- `POST /api/categories` - 创建分类（需要管理员）
- `PUT /api/categories/:id` - 更新分类（需要管理员）
- `DELETE /api/categories/:id` - 删除分类（需要管理员）

### 管理员接口
- `GET /api/admin/posts/pending` - 获取待审核帖子
- `POST /api/admin/posts/:id/approve` - 审核通过帖子（需要管理员）
- `POST /api/admin/posts/:id/reject` - 拒绝帖子（需要管理员）
- `GET /api/admin/users` - 获取用户列表（需要管理员）
- `PUT /api/admin/users/:id` - 更新用户信息（需要管理员）
- `DELETE /api/admin/users/:id` - 删除用户（需要管理员）

### 通知接口
- `GET /api/notifications` - 获取通知列表
- `POST /api/notifications/:id/read` - 标记通知为已读
- `POST /api/notifications/read_all` - 标记所有通知为已读

## 数据库设计

### 用户表 (users)
- id: 主键
- username: 用户名（唯一）
- email: 邮箱（唯一）
- password_hash: 密码哈希
- real_name: 真实姓名
- student_id: 学号
- admission_year: 入学年份
- is_admin: 是否为管理员
- created_at: 创建时间
- updated_at: 更新时间

### 分类表 (categories)
- id: 主键
- name: 分类名称（唯一）
- slug: URL标识（唯一）
- order: 排序值

### 帖子表 (posts)
- id: 主键
- title: 标题
- content_markdown: Markdown内容
- content_excerpt: 内容摘要
- author_id: 作者ID（外键）
- category_id: 分类ID（外键）
- status: 状态（pending/approved/rejected）
- views: 浏览次数
- created_at: 创建时间
- updated_at: 更新时间

### 评论表 (comments)
- id: 主键
- post_id: 帖子ID（外键）
- author_id: 作者ID（外键）
- content: 评论内容
- created_at: 创建时间
- updated_at: 更新时间

### 点赞表 (post_likes, comment_likes)
- id: 主键
- user_id: 用户ID（外键）
- post_id/comment_id: 帖子/评论ID（外键）
- created_at: 创建时间

### 通知表 (notifications)
- id: 主键
- user_id: 用户ID（外键）
- title: 通知标题
- content: 通知内容
- is_read: 是否已读
- created_at: 创建时间

## 开发说明

### 代码规范
- 后端遵循PEP 8规范
- 前端遵循Vue 3 Composition API风格
- 使用有意义的变量和函数命名
- 添加适当的注释

### Git提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建/工具链相关

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交Issue和Pull Request来帮助改进项目。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至：xksnetcbs@qq.com

## 更新日志

### v1.0.0 (2026-02-27)
- 完成基础论坛功能
- 实现用户认证和授权
- 添加帖子和评论功能
- 实现点赞系统
- 添加主题切换功能
- 完成管理员管理界面
- 支持分类管理
