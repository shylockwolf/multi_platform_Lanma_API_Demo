# 澜码API Demo - Web版本

一个基于HTML、CSS和JavaScript的Web应用，用于与澜码（Lanma）API进行交互，实现智能体问答功能。

## 🌐 项目概述

这是一个纯前端的Web应用，提供现代化的用户界面来与RAG 1.0交通法规智能体进行实时对话。应用采用响应式设计，支持桌面和移动设备。

## 📁 文件结构

```
HTML/
├── index.html                 # 主页面文件
├── script.js                  # JavaScript核心逻辑
├── styles.css                 # CSS样式文件
├── lanma_api_simple.py        # Python后端辅助脚本（可选）
└── README.md                  # 本文件
```

## ✨ 功能特性

- 🎯 **自动连接管理**：应用启动后自动与智能体建立会话连接
- 💬 **实时对话交互**：支持流式响应，实时显示智能体回复
- 📱 **响应式设计**：适配桌面、平板和手机等多种设备
- 🎨 **现代UI界面**：简洁美观的用户界面，支持主题色彩
- ⌨️ **快捷操作**：支持回车键快速发送消息
- 🔄 **状态监控**：实时显示API连接状态和会话信息

## 🚀 快速开始

### 1. 直接在浏览器中打开

```bash
# 克隆或下载项目
cd HTML

# 使用浏览器打开index.html
open index.html
# 或者双击index.html文件
```

### 2. 使用本地服务器（推荐）

```bash
# 使用Python内置服务器
python3 -m http.server 8000

# 或者使用Node.js服务器
npx serve .

# 然后访问 http://localhost:8000
```

### 3. 使用Python辅助脚本

```bash
# 运行Python GUI版本（作为备选方案）
python3 lanma_api_simple.py
```

## 💻 技术实现

### 核心技术栈
- **HTML5**：语义化标记和现代Web标准
- **CSS3**：Flexbox布局、响应式设计、CSS动画
- **JavaScript ES6+**：现代JavaScript语法和API
- **Fetch API**：异步HTTP请求处理
- **Stream API**：流式响应数据处理

### 关键功能实现

#### API连接管理
```javascript
async function handshakeWithAgent() {
    // 自动建立会话连接
    // 获取sessionSn并更新界面状态
}
```

#### 流式响应处理
```javascript
async function processStreamResponse(body) {
    const reader = body.getReader();
    // 实时处理流式数据
    // 逐步显示智能体回复
}
```

#### 状态管理
```javascript
const appState = {
    apiKey: "26ae4908-ec15-49fb-bd4f-9181bfc3bd71",
    agentSn: "agent-4778817f457648b09e50e",
    verSn: "ver-26178f53ed4548bebad6f",
    sessionSn: "NA",
    // ...
};
```

## 🎨 界面设计

### 布局结构
1. **页面标题**：应用名称和品牌标识
2. **会话信息区域**：显示API连接状态和会话详情
3. **操作区域**：
   - 输入框：用户问题输入
   - 发送按钮：提交问题到智能体
   - 输出日志：显示对话历史和智能体回复

### 响应式特性
- **桌面端**：最大宽度800px，居中布局
- **平板端**：自适应宽度，保持良好阅读体验
- **移动端**：全屏布局，垂直堆叠元素

### 视觉效果
- 🎨 现代化配色方案
- ✨ 平滑的过渡动画
- 🔍 清晰的状态指示
- 📱 触摸友好的交互元素

## 🔧 配置说明

### API配置（可选修改）
```javascript
const appState = {
    apiKey: "26ae4908-ec15-49fb-bd4f-9181bfc3bd71",
    agentSn: "agent-4778817f457648b09e50e",
    verSn: "ver-26178f53ed4548bebad6f"
};
```

### 自定义样式
修改 `styles.css` 中的CSS变量：
```css
:root {
    --primary-color: #3498db;
    --success-color: #27ae60;
    --error-color: #e74c3c;
    --background-color: #f5f5f5;
}
```

## 📱 兼容性

### 浏览器支持
- ✅ Chrome 90+
- ✅ Safari 14+
- ✅ Firefox 88+
- ✅ Edge 90+

### 移动设备
- ✅ iOS Safari 14+
- ✅ Chrome Mobile 90+
- ✅ Samsung Internet 15+

## 🔒 安全注意事项

⚠️ **重要提醒**：
- 当前版本中API密钥直接写在JavaScript代码中
- 生产环境中应考虑以下安全措施：
  - 使用后端代理API请求
  - 实施密钥轮换机制
  - 添加请求频率限制
  - 考虑使用环境变量配置

## 🐛 常见问题

### 1. 页面无法连接API
- 检查网络连接是否正常
- 确认API密钥是否有效
- 查看浏览器控制台错误信息

### 2. 流式响应显示异常
- 刷新页面重新建立连接
- 检查浏览器是否支持Stream API
- 确认服务器响应格式正确

### 3. 移动端显示问题
- 确保使用现代浏览器
- 尝试强制刷新页面
- 检查viewport设置

## 🚀 部署选项

### 静态网站托管
- **GitHub Pages**：免费静态托管
- **Netlify**：自动部署和CDN
- **Vercel**：现代前端部署平台
- **Firebase Hosting**：Google静态托管服务

### 服务器部署
```bash
# Nginx配置示例
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/HTML;
    index index.html;
}
```

## 📈 性能优化

- ✅ 异步加载和渲染
- ✅ 流式数据处理
- ✅ 事件委托和防抖
- ✅ CSS硬件加速
- ✅ 响应式图片和字体

## 🔮 未来规划

- [ ] 添加用户认证功能
- [ ] 支持多智能体切换
- [ ] 实现对话历史持久化
- [ ] 添加文件上传功能
- [ ] 集成语音输入/输出
- [ ] PWA支持（离线使用）

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](../LICENSE) 文件了解详情。

---

**最后更新**：2025年12月11日  
**版本**：v1.0.0  
**平台**：Web (HTML5/CSS3/JavaScript)