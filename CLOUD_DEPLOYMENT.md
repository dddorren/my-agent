# 小红书内容生成Agent - 云端部署指南

## 架构概览

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Vercel   │ --> │   Railway   │ --> │  Supabase   │
│  (前端)    │     │  (后端API)  │     │   (数据库)  │
└─────────────┘     └─────────────┘     └─────────────┘
   免费计划            免费额度            免费套餐
```

## 部署步骤

### 第一步：准备代码仓库

1. 将项目代码推送到GitHub仓库
2. 确保项目结构如下：
```
xiaohongshu-agent/
├── app/
│   ├── static/
│   │   └── index.html      # 前端页面
│   └── ...
├── Dockerfile              # Railway部署用
├── railway.json          # Railway配置
├── requirements.txt       # Python依赖
└── vercel.json           # Vercel配置
```

### 第二步：部署后端到 Railway

1. **注册Railway账号**
   - 访问 https://railway.app
   - 使用GitHub账号登录

2. **创建新项目**
   - 点击 "New Project" → "Deploy from GitHub repo"
   - 选择你的仓库

3. **配置环境变量**
   在 Railway 项目设置中添加：
   ```
   DASHSCOPE_API_KEY = your_dashscope_api_key
   OPENAI_API_KEY = your_openai_api_key
   PORT = 8000
   ```

4. **获取后端URL**
   部署成功后，Railway会分配一个URL，例如：
   `https://xiaohongshu-api.up.railway.app`

### 第三步：部署前端到 Vercel

1. **注册Vercel账号**
   - 访问 https://vercel.com
   - 使用GitHub账号登录

2. **导入项目**
   - 点击 "Add New" → "Project"
   - 选择你的GitHub仓库

3. **配置框架**
   - Framework Preset: Other
   - Root Directory: ./

4. **设置环境变量**
   ```
   BACKEND_URL = https://your-railway-app.up.railway.app
   ```

5. **部署**
   - 点击 "Deploy"
   - 等待部署完成

6. **获取前端URL**
   Vercel会分配一个域名，例如：
   `https://xiaohongshu-agent.vercel.app`

### 第四步：配置Supabase（可选）

如果需要存储用户数据和生成记录：

1. **注册Supabase账号**
   - 访问 https://supabase.com
   - 创建新项目

2. **获取配置信息**
   - Project URL
   - anon/public key
   - service role key

3. **在Railway中配置环境变量**
   ```
   SUPABASE_URL = your_supabase_url
   SUPABASE_KEY = your_supabase_anon_key
   SUPABASE_SERVICE_KEY = your_service_role_key
   ```

### 第五步：更新前端API地址

部署完成后，修改前端代码中的API地址：

```javascript
// 原来的配置
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? ''
    : `https://${window.location.hostname}`;

// 修改为你的Railway后端地址
const API_BASE_URL = 'https://your-railway-app.up.railway.app';
```

或者在Vercel中设置环境变量 `BACKEND_URL`。

## 免费额度说明

| 服务 | 免费额度 | 说明 |
|------|---------|------|
| Vercel | 100GB带宽/月 | 足够个人使用 |
| Railway | 500小时/月 | 每月重新部署 |
| Supabase | 500MB数据库 | 免费套餐 |
| DashScope | 有免费额度 | 通义千问API |

## 移动端适配

部署到云端后，天然支持移动端访问：

- 响应式设计已内置
- 支持iOS和Android浏览器
- 一键复制功能在移动端可用

## 访问方式

部署成功后，可以：

1. **电脑访问**
   - 直接打开 Vercel 分配的域名

2. **手机访问**
   - 打开相同的域名
   - 登录后即可使用

3. **分享给他人**
   - 只需分享 Vercel 域名即可

## 常见问题

### Q: Railway部署失败？
A: 检查Dockerfile和requirements.txt是否正确配置

### Q: 前端无法调用后端API？
A: 确保Railway允许外部访问，检查CORS配置

### Q: 如何更新代码？
A: 推送代码到GitHub，Railway和Vercel会自动重新部署

### Q: 免费额度用完怎么办？
A: Railway可以升级付费计划，或等待下月额度重置

## 部署检查清单

- [ ] GitHub仓库已创建
- [ ] Railway后端已部署
- [ ] Railway环境变量已配置
- [ ] Railway后端URL已获取
- [ ] Vercel前端已部署
- [ ] 前端API地址已更新
- [ ] 移动端访问测试通过
