# 交通法规智能体 API Demo

这是一个基于Android平台的交通法规智能体API演示应用，使用Jetpack Compose构建。

## 功能特性

- 与交通法规智能体API进行实时通信
- 显示对话记录
- 可视化连接状态
- 支持发送和接收消息

## 技术栈

- Kotlin
- Jetpack Compose
- Android Gradle Plugin
- HTTP API调用

## 编译和运行

### 前提条件

- Android Studio Hedgehog或更高版本
- Android SDK API 33或更高
- JDK 17

### 编译命令

```bash
./gradlew build
```

### 安装和运行

```bash
./gradlew installDebug
```

或者使用提供的启动脚本：

```bash
./start_emulator.sh
```

## 项目结构

```
Android/
├── app/
│   ├── src/main/
│   │   ├── java/com/example/api_demo/
│   │   ├── res/
│   │   └── AndroidManifest.xml
│   └── build.gradle.kts
├── gradle/
├── build.gradle.kts
├── settings.gradle.kts
├── gradlew
└── README.md
```

## API配置

应用连接到以下API：
- 端点：https://api.xbotspace.com/agent-api/v1/open/sessions
- Agent ID: agent-4778817f457648b09e50e
- Version: ver-26178f53ed4548bebad6f

## 许可证

MIT License
