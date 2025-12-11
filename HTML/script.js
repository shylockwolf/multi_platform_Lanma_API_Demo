// 应用状态管理
const appState = {
    apiKey: "26ae4908-ec15-49fb-bd4f-9181bfc3bd71",
    agentSn: "agent-4778817f457648b09e50e",
    verSn: "ver-26178f53ed4548bebad6f",
    sessionSn: "NA",
    connectionStatus: "正在连接中...",
    inputMessage: "",
    outputLog: ""
};

// DOM元素引用
const connectionStatusElement = document.getElementById('connectionStatus');
const userInputElement = document.getElementById('userInput');
const submitBtnElement = document.getElementById('submitBtn');
const outputLogElement = document.getElementById('outputLog');

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    // 设置初始状态
    updateConnectionStatus();
    
    // 绑定事件
    bindEvents();
    
    // 自动执行握手
    setTimeout(() => {
        handshakeWithAgent();
    }, 500);
});

// 绑定事件函数
function bindEvents() {
    // 输入框回车键发送
    userInputElement.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            submitInput();
        }
    });
    
    // 提交按钮点击事件
    submitBtnElement.addEventListener('click', () => {
        submitInput();
    });
}

// 更新连接状态显示
function updateConnectionStatus() {
    connectionStatusElement.value = appState.connectionStatus;
    connectionStatusElement.style.color = appState.sessionSn !== "NA" ? "#27ae60" : "#95a5a6";
}

// 更新输出日志
function updateOutputLog(message, color = null) {
    if (color) {
        outputLogElement.innerHTML += `<span style="color: ${color};">${message}</span>`;
    } else {
        outputLogElement.innerHTML += message;
    }
    // 滚动到底部
    outputLogElement.scrollTop = outputLogElement.scrollHeight;
}

// 清空输出日志
function clearOutputLog() {
    outputLogElement.innerHTML = "";
}

// 和智能体握手
async function handshakeWithAgent() {
    const { apiKey, agentSn, verSn } = appState;
    
    if (!apiKey || !agentSn || !verSn) {
        alert("请填写完整的API Key、Agent sn和Agent version sn");
        return;
    }
    
    const url = 'https://api.xbotspace.com/agent-api/v1/open/sessions';
    const options = {
        method: 'POST',
        headers: {
            'Authorization': apiKey,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            agentSn: agentSn,
            verSn: verSn
        })
    };
    
    try {
        // 清空输出日志并显示握手信息
        clearOutputLog();
        updateOutputLog("正在与智能体握手...\n", "#3498db");
        
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`握手失败: ${response.statusText}`);
        }
        
        const responseData = await response.json();
        
        if (responseData.success && responseData.data) {
            const sessionSn = responseData.data.sessionSn;
            const userSn = responseData.data.userSn;
            
            if (sessionSn) {
                appState.sessionSn = sessionSn;
                appState.connectionStatus = "【RAG 1.0】 智能查询 连结成功";
                updateConnectionStatus();
                
                updateOutputLog("\n🎉 API连接成功！\n", "#3498db");
                if (userSn) {
                    updateOutputLog(`✅ 用户ID: ${userSn}\n`, "#3498db");
                }
                updateOutputLog("✅ 可以开始智能查询了\n", "#3498db");
            }
        } else {
            throw new Error(`握手失败: ${responseData.message || '未知错误'}`);
        }
    } catch (error) {
        updateOutputLog(`\n执行出错: ${error.message}\n`, "#e74c3c");
        console.error("握手错误:", error);
    }
}

// 处理用户输入
function submitInput() {
    const inputText = userInputElement.value.trim();
    
    if (!inputText) {
        alert("请输入内容");
        return;
    }
    
    if (!appState.sessionSn || appState.sessionSn === "NA") {
        alert("请先与智能体握手获取sessionSn");
        return;
    }
    
    // 禁用输入框和按钮
    userInputElement.disabled = true;
    submitBtnElement.disabled = true;
    
    // 清空输出日志并显示用户问题
    clearOutputLog();
    updateOutputLog(`用户问题：${inputText}\n`);
    
    // 发送知识查询请求
    sendKnowledgeQuery(inputText);
}

// 发送知识查询请求
async function sendKnowledgeQuery(inputText) {
    const { apiKey, sessionSn } = appState;
    
    const url = 'https://api.xbotspace.com/agent-api/v1/open/knowledge/chat?agentType=doc';
    const options = {
        method: 'POST',
        headers: {
            'Authorization': apiKey,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sessionSn: sessionSn,
            msgContent: inputText,
            msgType: "text",
            stream: true
        })
    };
    
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`请求失败: ${response.statusText}`);
        }
        
        // 处理流式响应
        await processStreamResponse(response.body);
        
    } catch (error) {
        updateOutputLog(`\n执行出错: ${error.message}\n`, "#e74c3c");
        console.error("知识查询错误:", error);
    } finally {
        // 启用输入框和按钮
        userInputElement.disabled = false;
        submitBtnElement.disabled = false;
        userInputElement.value = "";
        userInputElement.focus();
    }
}

// 处理流式响应
async function processStreamResponse(body) {
    const reader = body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';
    let answerParts = [];
    
    updateOutputLog("\n\n智能体回答：\n");
    
    try {
        while (true) {
            const { done, value } = await reader.read();
            
            if (done) {
                break;
            }
            
            // 解码新获取的数据
            buffer += decoder.decode(value, { stream: true });
            
            // 按行分割数据
            let lines = buffer.split('\n');
            buffer = lines.pop(); // 保存不完整的最后一行
            
            // 处理每一行
            for (const line of lines) {
                if (line.trim().startsWith('data:{')) {
                    try {
                        // 提取JSON部分
                        const jsonStr = line.trim().slice(5);
                        const data = JSON.parse(jsonStr);
                        
                        if (data.data && data.data.content && data.data.content.answer) {
                            const answer = data.data.content.answer;
                            if (answer) {
                                answerParts.push(answer);
                                // 实时更新显示
                                updateOutputLog(answer);
                            }
                        }
                    } catch (e) {
                        console.error("解析JSON错误:", e);
                    }
                }
            }
        }
        
        // 处理剩余的缓冲数据
        if (buffer.trim()) {
            if (buffer.trim().startsWith('data:{')) {
                try {
                    const jsonStr = buffer.trim().slice(5);
                    const data = JSON.parse(jsonStr);
                    
                    if (data.data && data.data.content && data.data.content.answer) {
                        const answer = data.data.content.answer;
                        if (answer) {
                            answerParts.push(answer);
                            updateOutputLog(answer);
                        }
                    }
                } catch (e) {
                    console.error("解析剩余JSON错误:", e);
                }
            }
        }
        
        // 如果没有获取到有效答案
        if (answerParts.length === 0) {
            updateOutputLog("未获取到有效答案\n", "#e74c3c");
        }
        
    } catch (error) {
        updateOutputLog(`\n流式响应处理错误: ${error.message}\n`, "#e74c3c");
        console.error("流式响应错误:", error);
    } finally {
        reader.releaseLock();
    }
}
