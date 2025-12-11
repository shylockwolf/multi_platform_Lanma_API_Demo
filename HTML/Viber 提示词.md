您好，您是要我生成将您提供的 Python/Tkinter 桌面程序 移植到 Web 界面 的提示词（Prompt）吗？
由于您最初要求的是移植到 iOS (Viber Coding)，如果您改变主意想移植到 Web，我需要知道您希望使用哪种 Web 技术栈。
最常见的选择是：
1. React / Vue / Angular (前端框架) + Node.js / Python Flask/Django (后端)
2. 纯 HTML/CSS/JavaScript (通常搭配 Fetch API 进行交互)

📝 Web 移植提示词（通用 Web 前端）
如果我假设您希望使用现代前端框架（如 React/Vue/Svelte）配合 原生 Fetch API 来实现所有交互逻辑，以下是详细的提示词：
请为我生成一个详细的提示词，要求使用现代 Web 前端技术栈（例如 React, Vue 或 Svelte，任选一个）和原生 Fetch API，复刻这个名为 "澜码API Demo" 的应用程序。
目标: 将原始 Python/Tkinter 应用程序的功能和用户界面完全移植到 Web 浏览器界面。

💻 Web 应用复刻要求
1. 技术栈要求
* 使用 [指定前端框架，如 React] 框架构建单页应用（SPA）。
* 使用 原生 Fetch API 执行所有异步网络请求。
* 使用 CSS Flexbox/Grid 或 [框架对应的样式库，如 Tailwind CSS] 来实现布局和响应式设计。
2. 核心功能复刻 (API 交互)
必须实现以下两个核心 API 交互，保持与原始 Python 脚本中的 curl 命令完全一致的逻辑：
A. 握手功能（Handshake）
* 目的: 获取 sessionSn。
* API URL: https://api.xbotspace.com/agent-api/v1/open/sessions
* 方法: POST
* Headers: 必须包含 Authorization: <apiKey> 和 Content-Type: application/json。
* Body: 必须发送 JSON 负载 {"agentSn":"<agentSn>","verSn":"<verSn>"}。
* 逻辑: 页面加载完成后（例如在 React 的 useEffect 中）自动执行。成功后，更新状态显示，并在日志区打印连接成功信息。
B. 知识查询功能（Chat）
* 目的: 发送用户问题并获取智能体回答。
* API URL: https://api.xbotspace.com/agent-api/v1/open/knowledge/chat?agentType=doc
* 方法: POST
* Headers: 必须包含 Authorization: <apiKey> 和 Content-Type: application/json。
* Body: 必须发送 JSON 负载 {"sessionSn":"<sessionSn>","msgContent":"<用户输入>","msgType":"text","stream":true}。
* 流式处理:
    * 必须使用 Fetch API 或其他兼容的技术（如 EventSource 或 WebSocket，如果 Fetch 不够用）来处理 API 返回的 流式响应。
    * 实时解析 响应流中的每一行 data:{...}，提取 data.content.answer 的值。
    * 将提取到的文本内容实时、逐字或逐块地追加到答案显示区域，模拟打字机效果或流式输出。
3. 数据与状态管理
应用程序必须管理以下核心状态：
* apiKey, agentSn, verSn：存储在组件状态中，使用 Python 脚本中的默认值。
* sessionSn：存储当前有效的会话 ID（初始为 "NA"）。
* connectionStatus：显示连接状态（例如："正在连接中..."，"【RAG 1.0】 智能查询 连结成功"）。
* inputMessage：存储用户在输入框中键入的内容。
* outputLog：存储所有历史交互记录（包括用户问题、系统消息和智能体回答）。
4. UI/UX 界面复刻
设计一个简洁的单栏布局，复刻 Tkinter 程序的结构：
1. 顶部：API 状态显示
    * 显示 "API 连结状态:"。
    * 紧随其后是一个只读的文本区域，显示 connectionStatus。成功状态应使用绿色文本突出显示。
2. 中部：操作与输入区域
    * 显示 "和智能体问答:"。
    * 一个 input 文本框 绑定到 inputMessage，支持用户按 Enter 键 提交查询。
    * 要求: 在查询执行期间，输入框应被禁用，并显示加载指示器。
3. 底部：智能体回复/日志区域
    * 一个标题 "智能体回复:"。
    * 一个大型、可滚动的 textarea 或 div 用于显示完整的 outputLog。
    * 样式要求:
        * 用户问题和系统/连接消息使用 蓝色 字体。
        * 智能体的最终回答使用 黑色/默认 字体。
5. 错误处理
* 所有网络请求（握手和查询）必须包含健壮的 try...catch 错误处理。
* 任何网络失败、超时或 API 返回的错误信息（code 或 message）必须被捕获，并在 outputLog 中以红色或醒目颜色显示。
