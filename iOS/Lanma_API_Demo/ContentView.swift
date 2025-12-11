//
//  ContentView.swift
//  Lanma_API_Demo
//
//  Created by noone on 2025/12/11.
//

import SwiftUI
import Combine

struct ContentView: View {
    @State private var inputText = ""
    @State private var isConnected = false
    @State private var isLoading = false
    @State private var str_session_sn = ""
    @State private var agentReplies: [String] = [
        "等待连接API服务...",
        "系统未连接",
        "⚠️ 请检查网络连接",
        "🔌 点击右上角刷新按钮连接"
    ]
    
    // MARK: - 辅助计算属性
    
    // 用于标记最新消息的 ID，通常是数组的最后一个索引
    private var lastReplyID: Int {
        return agentReplies.count > 0 ? agentReplies.count - 1 : 0
    }
    
    // 连接状态文本和颜色
    private var connectionStatusColor: Color {
        isConnected ? .green : .red
    }
    
    private var connectionStatusText: Text {
        Text(isConnected ? "已连接" : "未连接")
            .font(.caption)
            .foregroundColor(connectionStatusColor)
            .fontWeight(.medium)
    }
    
    // 连接卡片副标题
    private var connectionSubtitle: String {
        if isLoading {
            return "正在连接API服务..."
        } else if isConnected {
            return "RAG 1.0 交通法规智能体连接成功"
        } else {
            return "RAG 1.0 - 智能查询服务"
        }
    }
    
    // MARK: - View Body
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // 顶部欢迎区域
                VStack(spacing: 16) {
                    Image(systemName: "globe")
                        .font(.system(size: 60))
                        .foregroundColor(.blue)
                        .padding()
                        .background(Circle().fill(Color.blue.opacity(0.1)))
                        .shadow(radius: 10)
                    
                    Text("API Demo")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                }
                .padding(.top, 20)
                .padding(.bottom, 20)
                
                // 主要内容区域
                ScrollView {
                    VStack(spacing: 16) {
                        // 连接状态卡片
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                Image(systemName: "network")
                                    .foregroundColor(.blue)
                                    .font(.title2)
                                
                                Text("连接状态")
                                    .font(.headline)
                                    .fontWeight(.semibold)
                                
                                Spacer()
                                
                                HStack(spacing: 6) {
                                    Circle()
                                        .fill(connectionStatusColor)
                                        .frame(width: 8, height: 8)
                                    
                                    connectionStatusText
                                    
                                    if isLoading {
                                        ProgressView()
                                            .scaleEffect(0.6)
                                    }
                                }
                            }
                            
                            Text(connectionSubtitle)
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                        .padding()
                        .background(Color(.systemBackground))
                        .cornerRadius(12)
                        .shadow(color: .black.opacity(0.05), radius: 5)
                        
                        // 对话记录卡片 (已加入自动回滚 ScrollViewReader)
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                Image(systemName: "message.text")
                                    .foregroundColor(.blue)
                                    .font(.title2)
                                
                                Text("对话记录")
                                    .font(.headline)
                                    .fontWeight(.semibold)
                                
                                Spacer()
                                
                                if !agentReplies.isEmpty {
                                    Text("\(agentReplies.count)")
                                        .font(.caption)
                                        .fontWeight(.medium)
                                        .foregroundColor(.white)
                                        .padding(.horizontal, 8)
                                        .padding(.vertical, 4)
                                        .background(Color.blue)
                                        .clipShape(Circle())
                                }
                            }
                            
                            // *** 启用自动回滚的关键区域 ***
                            ScrollViewReader { proxy in
                                ScrollView {
                                    VStack(spacing: 12) {
                                        ForEach(Array(agentReplies.enumerated()), id: \.offset) { index, reply in
                                            HStack(alignment: .top, spacing: 8) {
                                                Image(systemName: reply.contains("用户问题") ? "person.circle.fill" : "brain.head.profile")
                                                    .foregroundColor(reply.contains("用户问题") ? .blue : .green)
                                                    .font(.system(size: 20))
                                                    .frame(width: 24)
                                                
                                                VStack(alignment: .leading, spacing: 4) {
                                                    Text(reply)
                                                        .font(.system(size: 14))
                                                    
                                                    // 简化时间显示逻辑
                                                    Text(index == lastReplyID ? "刚刚" : "\((lastReplyID - index) * 2)秒前")
                                                        .font(.caption2)
                                                        .foregroundColor(.secondary)
                                                }
                                                
                                                Spacer()
                                            }
                                            .padding(.vertical, 4)
                                            .id(index) // 添加 ID 用于滚动
                                        }
                                    }
                                    .padding(.vertical, 8)
                                }
                                .frame(height: 250) // 固定高度确保滚动区域
                                .clipped()
                                // 修复 DEPRACTED 警告，使用新的 onChange 语法 (iOS 17+)
                                .onChange(of: agentReplies.count) {
                                    withAnimation {
                                        proxy.scrollTo(lastReplyID, anchor: .bottom)
                                    }
                                }
                                // 初始加载时滚动到底部
                                .onAppear {
                                    proxy.scrollTo(lastReplyID, anchor: .bottom)
                                }
                            }
                            // **********************************
                        }
                        .padding()
                        .background(Color(.systemBackground))
                        .cornerRadius(12)
                        .shadow(color: .black.opacity(0.05), radius: 5)
                        
                        Spacer(minLength: 120)
                    }
                    .padding(.horizontal, 20)
                }
                
                // 底部输入区域
                VStack(spacing: 0) {
                    Divider()
                    
                    HStack(spacing: 12) {
                        TextField("输入您的问题...", text: $inputText)
                            .textFieldStyle(RoundedBorderTextFieldStyle())
                        
                        Button("发送") {
                            sendMessage()
                        }
                        .foregroundColor(.white)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 8)
                        .background(Color.blue)
                        .cornerRadius(8)
                        .disabled(inputText.isEmpty)
                    }
                    .padding()
                }
                .background(Color(.systemBackground))
            }
            .background(Color(.systemGray6))
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .principal) {
                    HStack(spacing: 8) {
                        Image(systemName: "brain.head.profile")
                            .foregroundColor(.blue)
                        Text("交通法规智能体")
                            .fontWeight(.semibold)
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button {
                        connectToAPI()
                    } label: {
                        Image(systemName: "arrow.clockwise")
                            .foregroundColor(.blue)
                    }
                }
            }
        }
        .onAppear {
            // 开机后自动连接API
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                connectToAPI()
            }
        }
    }
    
    // MARK: - 逻辑方法
    
    private func connectToAPI() {
        guard !isLoading else { return }
        
        isLoading = true
        isConnected = false
        
        // 清空之前的消息，显示连接过程
        agentReplies = [
            "🔌 正在初始化API连接...",
            "📡 执行命令: curl -X POST 'https://api.xbotspace.com/agent-api/v1/open/sessions'",
            "🔑 使用授权密钥: 26ae4908-****-****-****-bfc3bd71",
            "🤖 智能体编号: agent-4778817f457648b09e50e",
            "📋 版本编号: ver-26178f53ed4548bebad6f",
            "✨ 你现在可以和智能体进行互动了"
        ]
        
        // 执行实际的API请求
        performAPISessionRequest()
    }
    
    private func performAPISessionRequest() {
        // 构建URL
        guard let url = URL(string: "https://api.xbotspace.com/agent-api/v1/open/sessions") else {
            DispatchQueue.main.async {
                self.agentReplies.append("❌ 无效的URL")
                self.isLoading = false
            }
            return
        }
        
        // 构建请求
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("26ae4908-ec15-49fb-bd4f-9181bfc3bd71", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // 构建请求体
        let requestBody = [
            "agentSn": "agent-4778817f457648b09e50e",
            "verSn": "ver-26178f53ed4548bebad6f"
        ]
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: requestBody)
        } catch {
            DispatchQueue.main.async {
                self.agentReplies.append("❌ JSON序列化失败: \(error.localizedDescription)")
                self.isLoading = false
            }
            return
        }
        
        // 执行请求
        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self.agentReplies.append("❌ 网络请求失败: \(error.localizedDescription)")
                    self.isLoading = false
                    return
                }
                
                // 显示响应状态
                if let httpResponse = response as? HTTPURLResponse {
                    self.agentReplies.append("📡 HTTP状态码: \(httpResponse.statusCode)")
                }
                
                // 直接显示原始响应数据，不做任何处理
                if let data = data {
                    if let responseString = String(data: data, encoding: .utf8) {
                        self.agentReplies.append("📥 系统原始响应:")
                        self.agentReplies.append(responseString)
                        
                        // 解析JSON并提取sessionSn
                        self.extractSessionSn(from: data)
                    } else {
                        self.agentReplies.append("📥 系统原始响应 (二进制数据):")
                        self.agentReplies.append(data.base64EncodedString())
                    }
                } else {
                    self.agentReplies.append("📥 系统响应: 无数据返回")
                }
                
                self.isLoading = false
                self.isConnected = true
                
                // 触觉反馈
                let impactFeedback = UIImpactFeedbackGenerator(style: .medium)
                impactFeedback.impactOccurred()
            }
        }.resume()
    }
    
    private func extractSessionSn(from data: Data) {
        do {
            if let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
               let dataDict = json["data"] as? [String: Any],
               let sessionSn = dataDict["sessionSn"] as? String {
                
                str_session_sn = sessionSn
                agentReplies.append("✅ 提取sessionSn成功: \(str_session_sn)")
            } else {
                agentReplies.append("❌ 无法解析sessionSn")
            }
        } catch {
            agentReplies.append("❌ JSON解析失败: \(error.localizedDescription)")
        }
    }
    
    private func sendMessage() {
        guard !inputText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { return }
        
        let userQuery = inputText.trimmingCharacters(in: .whitespacesAndNewlines)
        inputText = ""
        
        // 添加用户消息
        agentReplies.append("用户问题: \(userQuery)")
        
        // 构建并显示curl命令，使用真实的sessionSn
        let jsonPayload = """
{
    "sessionSn": "\(str_session_sn)",
    "msgContent": "\(userQuery)",
    "msgType": "text",
    "stream": true
}
"""
        
        let curlCommand = """
curl --location --request POST 'https://api.xbotspace.com/agent-api/v1/open/knowledge/chat?agentType=doc' \\
--header 'Authorization: 26ae4908-****-****-****-bfc3bd71' \\
--header 'Content-Type: application/json' \\
--data-raw '\(jsonPayload)'
"""
        
        // 直接执行实际请求，不显示curl命令
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            self.performChatAPIRequest(with: userQuery)
        }
    }
    
    private func performChatAPIRequest(with userQuery: String) {
        // 构建URL
        guard let url = URL(string: "https://api.xbotspace.com/agent-api/v1/open/knowledge/chat?agentType=doc") else {
            agentReplies.append("❌ 无效的聊天API URL")
            return
        }
        
        // 构建请求
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("26ae4908-ec15-49fb-bd4f-9181bfc3bd71", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // 构建请求体
        let requestBody = [
            "sessionSn": str_session_sn,
            "msgContent": userQuery,
            "msgType": "text",
            "stream": true
        ] as [String : Any]
        
        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: requestBody, options: .prettyPrinted)
        } catch {
            agentReplies.append("❌ JSON序列化失败: \(error.localizedDescription)")
            return
        }
        
        // 添加等待消息
        agentReplies.append("🤖 智能体正在查询思考...")
        
        // 执行请求
        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                if let error = error {
                    self.agentReplies.append("❌ 聊天请求失败: \(error.localizedDescription)")
                    return
                }
                
                // 不显示聊天HTTP状态码
                
                // 处理流式响应数据
                if let data = data {
                    if let responseString = String(data: data, encoding: .utf8) {
                        // 只解析流式数据并提取answer字段，不显示原始响应
                        self.processStreamResponse(responseString)
                    }
                }
            }
        }.resume()
        
        // 触觉反馈
        let impactFeedback = UIImpactFeedbackGenerator(style: .light)
        impactFeedback.impactOccurred()
    }
    
    private func processStreamResponse(_ responseString: String) {
        // 分割数据包（每个数据包以 "data:" 开头）
        let dataPackets = responseString.components(separatedBy: "data:")
        
        var allAnswers: [String] = []
        
        // 处理每个数据包
        for packet in dataPackets {
            let trimmedPacket = packet.trimmingCharacters(in: .whitespacesAndNewlines)
            if trimmedPacket.isEmpty { continue }
            
            // 解析JSON
            if let jsonData = trimmedPacket.data(using: .utf8) {
                do {
                    if let json = try JSONSerialization.jsonObject(with: jsonData) as? [String: Any],
                       let data = json["data"] as? [String: Any],
                       let content = data["content"] as? [String: Any],
                       let answer = content["answer"] as? String {
                        
                        allAnswers.append(answer)
                    }
                } catch {
                    // 忽略解析错误，继续处理下一个数据包
                    continue
                }
            }
        }
        
        // 如果没有数据包，直接返回
        guard !allAnswers.isEmpty else { return }
        
        // 检查除了最后一个以外的所有answer是否都是空的
        let allExceptLast = Array(allAnswers.dropLast())
        let allExceptLastAreEmpty = allExceptLast.allSatisfy { $0.isEmpty }
        
        if allExceptLastAreEmpty && !allAnswers.last!.isEmpty {
            // 如果除了最后一个都是空的，且最后一个不为空，则输出最后一个answer
            agentReplies.append(allAnswers.last!)
        } else {
            // 否则，放弃最后一个数据包，组合其余的answer
            allAnswers.removeLast()
            let combinedAnswer = allAnswers.joined()
            if !combinedAnswer.isEmpty {
                agentReplies.append(combinedAnswer)
            }
        }
    }
}

#Preview {
    ContentView()
}
