package com.example.api_demo

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.InfiniteRepeatableSpec
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Refresh
import androidx.compose.material.icons.filled.Send
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.api_demo.ui.theme.API_DemoTheme
import androidx.compose.ui.tooling.preview.Preview

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            API_DemoTheme {
                TrafficLawAgentScreen()
            }
        }
    }
}

@Composable
fun TrafficLawAgentScreen() {
    val backgroundColor = Color(0xFFF7F9FC)
    val primaryBlue = Color(0xFF2F80ED)
    val primaryBlueGradient = Brush.linearGradient(
        colors = listOf(Color(0xFF2F80ED), Color(0xFF56CCF2)),
        start = Offset.Zero,
        end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
    )
    val successGreen = Color(0xFF28C76F)
    val textColor = Color(0xFF1A1A2E)
    val grayTextColor = Color(0xFF6C757D)
    val lightGrayColor = Color(0xFFE9ECEF)
    val whiteColor = Color.White
    val cardShadow = 4.dp
    
    // 应用启动时清空对话记录，使用可变列表以便动态添加内容
    val conversationList = remember {
        mutableStateListOf<ConversationItem>()
    }
    
    // 连接状态相关变量
    var connectionStatusText by remember { mutableStateOf("正在与智能体握手") }
    var connectionIndicatorText by remember { mutableStateOf("断开") }
    var connectionColor by remember { mutableStateOf(Color.Red) }
    var str_session_sn by remember { mutableStateOf("") }
    
    // 应用启动时自动执行HTTP请求
    val coroutineScope = rememberCoroutineScope()
    remember {
        coroutineScope.launch(Dispatchers.IO) {
            try {
                // 设置请求URL
                val url = java.net.URL("https://api.xbotspace.com/agent-api/v1/open/sessions")
                
                // 打开连接
                val connection = url.openConnection() as java.net.HttpURLConnection
                
                // 设置请求方法和头信息
                connection.requestMethod = "POST"
                connection.setRequestProperty("Authorization", "26ae4908-ec15-49fb-bd4f-9181bfc3bd71")
                connection.setRequestProperty("Content-Type", "application/json")
                connection.doOutput = true
                
                // 设置请求体
                val requestBody = "{\"agentSn\":\"agent-4778817f457648b09e50e\",\"verSn\":\"ver-26178f53ed4548bebad6f\"}"
                val outputStream = connection.outputStream
                outputStream.write(requestBody.toByteArray())
                outputStream.flush()
                outputStream.close()
                
                // 获取响应
                val responseCode = connection.responseCode
                val responseBody = if (responseCode == java.net.HttpURLConnection.HTTP_OK) {
                    connection.inputStream.bufferedReader().use { it.readText() }
                } else {
                    "请求失败，响应码: $responseCode"
                }
                
                // 关闭连接
                connection.disconnect()
                
                // 在主线程更新UI
                coroutineScope.launch(Dispatchers.Main) {
                    // 添加请求命令到对话记录
                    conversationList.add(
                        ConversationItem(
                            type = ConversationType.SYSTEM_RESPONSE,
                            content = """curl -X POST 'https://api.xbotspace.com/agent-api/v1/open/sessions' 
--header 'Authorization: 26ae4908-ec15-49fb-bd4f-9181bfc3bd71' 
--header 'Content-Type: application/json' 
--data-raw '{"agentSn":"agent-4778817f457648b09e50e","verSn":"ver-26178f53ed4548bebad6f"}'""",
                            time = "刚刚"
                        )
                    )
                    // 添加响应结果到对话记录
                    conversationList.add(
                        ConversationItem(
                            type = ConversationType.SUCCESS,
                            content = responseBody,
                            time = "刚刚"
                        )
                    )
                    
                    // 解析JSON响应，提取sessionSn并更新连接状态
                    try {
                        val jsonResponse = org.json.JSONObject(responseBody)
                        if (jsonResponse.getBoolean("success")) {
                            val data = jsonResponse.getJSONObject("data")
                            str_session_sn = data.getString("sessionSn")
                            
                            // 更新连接状态
                            connectionStatusText = "RAG 1.0 交通法规智能体握手成功"
                            connectionIndicatorText = "连接"
                            connectionColor = successGreen
                        }
                    } catch (e: Exception) {
                        // JSON解析失败，添加异常信息到对话记录
                        conversationList.add(
                            ConversationItem(
                                type = ConversationType.SYSTEM_RESPONSE,
                                content = "JSON解析异常: ${e.message}",
                                time = "刚刚"
                            )
                        )
                    }
                }
            } catch (e: Exception) {
                // 处理异常
                coroutineScope.launch(Dispatchers.Main) {
                    conversationList.add(
                        ConversationItem(
                            type = ConversationType.SYSTEM_RESPONSE,
                            content = "请求异常: ${e.message}",
                            time = "刚刚"
                        )
                    )
                }
            }
        }
    }
    
    var inputText by remember { mutableStateOf("") }
    val listState = rememberLazyListState()
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundColor)
            .padding(16.dp)
    ) {
        // 顶部应用栏
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(60.dp)
                .align(Alignment.CenterHorizontally),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                // 蓝色大脑图标
                Surface(
                    modifier = Modifier
                        .size(40.dp)
                        .shadow(4.dp, CircleShape),
                    shape = CircleShape,
                    color = primaryBlue
                ) {
                    Box(modifier = Modifier.padding(8.dp)) {
                        Text(
                            text = "⚖️",
                            fontSize = 22.sp,
                            textAlign = TextAlign.Center
                        )
                    }
                }
                Spacer(modifier = Modifier.width(12.dp))
                Text(
                    text = "交通法规智能体",
                    fontSize = 22.sp,
                    fontWeight = FontWeight.Bold,
                    color = textColor
                )
            }
            
            // 刷新按钮
            Surface(
                modifier = Modifier
                    .size(44.dp)
                    .shadow(2.dp, CircleShape),
                shape = CircleShape,
                color = whiteColor
            ) {
                IconButton(
                    onClick = { /* 刷新逻辑 */ },
                    modifier = Modifier.size(44.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.Refresh,
                        contentDescription = "刷新",
                        tint = primaryBlue,
                        modifier = Modifier.size(24.dp)
                    )
                }
            }
        }
        
        Spacer(modifier = Modifier.height(28.dp))
        
        // 主图标区
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.CenterHorizontally),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // 蓝色地球图标
            Surface(
                modifier = Modifier
                    .size(130.dp)
                    .shadow(8.dp, CircleShape),
                shape = CircleShape,
                color = whiteColor
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(
                    brush = Brush.radialGradient(
                        colors = listOf(primaryBlue.copy(alpha = 0.4f), Color.Transparent),
                        center = Offset(0.5f, 0.5f)
                    )
                )
                        .padding(20.dp)
                ) {
                    Surface(
                        modifier = Modifier
                            .fillMaxSize()
                            .shadow(4.dp, CircleShape),
                        shape = CircleShape,
                        color = whiteColor
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxSize()
                                .padding(24.dp)
                                .border(2.dp, primaryBlue, CircleShape)
                        ) {
                            Text(
                                text = "🌐",
                                fontSize = 56.sp,
                                textAlign = TextAlign.Center,
                                modifier = Modifier.fillMaxSize()
                            )
                        }
                    }
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Text(
                text = "API Demo",
                fontSize = 32.sp,
                fontWeight = FontWeight.Bold,
                color = textColor,
                letterSpacing = 0.5.sp
            )
        }
        
        Spacer(modifier = Modifier.height(28.dp))
        
        // 连接状态卡片
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .height(90.dp)
                .shadow(cardShadow, RoundedCornerShape(20.dp)),
            shape = RoundedCornerShape(20.dp),
            elevation = CardDefaults.cardElevation(defaultElevation = cardShadow)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(20.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                // 左侧：图标和状态信息
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(40.dp)
                            .background(primaryBlue.copy(alpha = 0.1f), shape = CircleShape)
                            .padding(8.dp)
                    ) {
                        Text(
                            text = "🌐",
                            fontSize = 20.sp
                        )
                    }
                    Spacer(modifier = Modifier.width(12.dp))
                    Column {
                        Text(
                            text = "连接状态",
                            fontSize = 16.sp,
                            fontWeight = FontWeight.SemiBold,
                            color = textColor
                        )
                        Text(
                            text = connectionStatusText,
                            fontSize = 14.sp,
                            color = grayTextColor,
                            modifier = Modifier.padding(top = 2.dp)
                        )
                    }
                }
                
                // 右侧：连接状态指示器
                Row(verticalAlignment = Alignment.CenterVertically) {
                    // 脉动动画效果
                    val pulseSize by animateDpAsState(
                        targetValue = 12.dp,
                        animationSpec = InfiniteRepeatableSpec(
                            animation = tween(durationMillis = 1000),
                            repeatMode = RepeatMode.Reverse
                        )
                    )
                    Box(
                        modifier = Modifier
                            .size(pulseSize)
                            .background(connectionColor, shape = CircleShape)
                    )
                    Spacer(modifier = Modifier.width(10.dp))
                    Text(
                        text = connectionIndicatorText,
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Medium,
                        color = connectionColor
                    )
                }
            }
        }
        
        Spacer(modifier = Modifier.height(20.dp))
        
        // 对话记录卡片 - 添加很细的边框和不同的底色
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(3f) // 大幅增加权重，让对话记录占据更多空间
                .background(
                    color = Color(0xFFF7F9FF), // 淡淡的蓝色底色
                    shape = RoundedCornerShape(16.dp)
                )
                .border(
                    width = 0.5.dp, // 很细的边框
                    color = Color(0xFFE3E8FF), // 淡蓝色边框
                    shape = RoundedCornerShape(16.dp)
                )
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .background(
                        brush = Brush.verticalGradient(
                            colors = listOf(
                                Color.White,
                                Color(0xFFF8FAFF)
                            ),
                            startY = 0f,
                            endY = Float.POSITIVE_INFINITY
                        )
                    )
                    .padding(24.dp)
            ) {
                // 简洁的标题 - 无边框设计
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 8.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // 简化的标题
                    Row(
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = "💬 对话记录",
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold,
                            color = textColor
                        )
                    }
                    
                    // 简化的数字徽章
                    Box(
                        modifier = Modifier
                            .background(
                                color = primaryBlue.copy(alpha = 0.1f),
                                shape = RoundedCornerShape(12.dp)
                            )
                            .padding(horizontal = 8.dp, vertical = 4.dp)
                    ) {
                        Text(
                            text = "${conversationList.size}",
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold,
                            color = primaryBlue,
                            textAlign = TextAlign.Center
                        )
                    }
                }
                
                Spacer(modifier = Modifier.height(20.dp))
                
                // 对话列表 - 可滚动，优化间距和背景
                LazyColumn(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                    state = listState,
                    verticalArrangement = Arrangement.spacedBy(8.dp), // 减少间距
                    contentPadding = androidx.compose.foundation.layout.PaddingValues(vertical = 6.dp) // 减少内边距
                ) {
                    items(conversationList) { item ->
                        ConversationItemView(
                            item = item,
                            primaryBlue = primaryBlue,
                            successGreen = successGreen,
                            textColor = textColor,
                            grayTextColor = grayTextColor,
                            whiteColor = whiteColor
                        )
                    }
                }
            }
        }
        
        Spacer(modifier = Modifier.height(20.dp))
        
        // 底部输入栏
        Surface(
            modifier = Modifier
                .fillMaxWidth()
                .shadow(cardShadow, RoundedCornerShape(24.dp)),
            shape = RoundedCornerShape(24.dp),
            color = whiteColor
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(8.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // 文本输入框
                val focusRequester = remember { FocusRequester() }
                TextField(
                    value = inputText,
                    onValueChange = { inputText = it },
                    placeholder = { 
                        Text(
                            text = "输入您的问题...",
                            color = grayTextColor
                        ) 
                    },
                    keyboardOptions = KeyboardOptions.Default.copy(
                        keyboardType = KeyboardType.Text
                    ),
                    modifier = Modifier
                        .weight(1f)
                        .height(56.dp)
                        .focusRequester(focusRequester),
                    shape = RoundedCornerShape(20.dp),
                    colors = TextFieldDefaults.colors(
                        unfocusedContainerColor = Color.Transparent,
                        focusedContainerColor = Color.Transparent,
                        unfocusedIndicatorColor = Color.Transparent,
                        focusedIndicatorColor = Color.Transparent,
                        cursorColor = primaryBlue
                    )
                )
                LaunchedEffect(Unit) {
                    focusRequester.requestFocus()
                }
                
                // 发送按钮 - 带有按压动画
                val interactionSource = remember { MutableInteractionSource() }
                val isPressed by interactionSource.collectIsPressedAsState()
                val buttonScale by animateDpAsState(
                    targetValue = if (isPressed) 52.dp else 56.dp,
                    animationSpec = tween(durationMillis = 150)
                )
                
                Surface(
                    modifier = Modifier
                        .size(buttonScale)
                        .shadow(4.dp, RoundedCornerShape(16.dp)),
                    shape = RoundedCornerShape(16.dp),
                    color = primaryBlue
                ) {
                    Box(
                        modifier = Modifier
                            .clickable(interactionSource = interactionSource, indication = null) {
                                // 保存用户输入并清空输入框
                                val userInput = inputText
                                if (userInput.isNotEmpty()) {
                                    inputText = ""
                                    // 调用发送按钮处理函数
                                    handleSendButtonClick(userInput, str_session_sn, conversationList, coroutineScope)
                                }
                            }
                            .padding(16.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.Send,
                            contentDescription = "发送",
                            tint = whiteColor,
                            modifier = Modifier.size(24.dp)
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun ConversationItemView(
    item: ConversationItem,
    primaryBlue: Color,
    successGreen: Color,
    textColor: Color,
    grayTextColor: Color,
    whiteColor: Color
) {
    // 优化的颜色主题
    val (primaryColor, bgColor, borderColor, contentBgColor) = when (item.type) {
        ConversationType.USER -> Tuple4(
            primaryBlue,
            primaryBlue.copy(alpha = 0.03f),
            primaryBlue.copy(alpha = 0.15f),
            primaryBlue.copy(alpha = 0.08f)
        )
        ConversationType.SYSTEM_RESPONSE -> Tuple4(
            Color(0xFF6366F1),
            Color.White,
            Color(0xFFE5E7EB),
            Color(0xFFF9FAFB)
        )
        ConversationType.SUCCESS -> Tuple4(
            successGreen,
            successGreen.copy(alpha = 0.03f),
            successGreen.copy(alpha = 0.15f),
            successGreen.copy(alpha = 0.08f)
        )
        ConversationType.ERROR -> Tuple4(
            Color(0xFFEF4444),
            Color.Red.copy(alpha = 0.03f),
            Color.Red.copy(alpha = 0.15f),
            Color.Red.copy(alpha = 0.08f)
        )
    }
    
    val icon = when (item.type) {
        ConversationType.USER -> "👤"
        ConversationType.SYSTEM_RESPONSE -> "🤖"
        ConversationType.SUCCESS -> "✨"
        ConversationType.ERROR -> "⚠️"
    }
    
    val title = when (item.type) {
        ConversationType.USER -> "用户"
        ConversationType.SYSTEM_RESPONSE -> "AI助手"
        ConversationType.SUCCESS -> "成功响应"
        ConversationType.ERROR -> "错误信息"
    }
    
    Card(
        modifier = Modifier
            .fillMaxWidth(),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(
            containerColor = bgColor
        )
        // 完全移除边框和阴影
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp), // 减少内边距
            horizontalArrangement = Arrangement.Start
        ) {
            // 优化的图标区域 - 更紧凑设计
            Box(
                modifier = Modifier.size(42.dp) // 减小尺寸
            ) {
                // 外圈装饰
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    shape = CircleShape,
                    color = primaryColor.copy(alpha = 0.08f)
                ) {}
                
                // 内圈背景
                Surface(
                    modifier = Modifier
                        .size(38.dp) // 减小尺寸
                        .align(Alignment.Center),
                    shape = CircleShape,
                    shadowElevation = 2.dp,
                    tonalElevation = 1.dp
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxSize()
                            .background(
                                brush = Brush.radialGradient(
                                    colors = listOf(
                                        primaryColor,
                                        primaryColor.copy(alpha = 0.8f)
                                    )
                                ),
                                shape = CircleShape
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = icon,
                            fontSize = 20.sp, // 减小字体
                            textAlign = TextAlign.Center
                        )
                    }
                }
            }
            
            Spacer(modifier = Modifier.width(12.dp)) // 减少间距
            
            // 优化的内容区域
            Column(
                modifier = Modifier.weight(1f)
            ) {
                // 标题和时间
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // 标题区域
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = title,
                            fontSize = 15.sp, // 稍微减小字体
                            fontWeight = FontWeight.Bold,
                            color = primaryColor,
                            letterSpacing = 0.2.sp
                        )
                        
                        Spacer(modifier = Modifier.width(6.dp)) // 减少间距
                        
                        // 状态指示器
                        Box(
                            modifier = Modifier
                                .size(5.dp) // 减小尺寸
                                .background(primaryColor, shape = CircleShape)
                        )
                    }
                    
                    // 时间标签
                    Surface(
                        shape = RoundedCornerShape(6.dp), // 减少圆角
                        color = primaryColor.copy(alpha = 0.08f) // 降低透明度
                    ) {
                        Text(
                            text = item.time,
                            fontSize = 10.sp,
                            color = primaryColor.copy(alpha = 0.8f),
                            fontWeight = FontWeight.Medium,
                            modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp) // 进一步减少内边距
                        )
                    }
                }
                
                Spacer(modifier = Modifier.height(8.dp)) // 减少间距
                
                // 优化的内容背景 - 完全移除边框效果
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(
                            color = contentBgColor,
                            shape = RoundedCornerShape(8.dp)
                        )
                ) {
                    Column(
                        modifier = Modifier.padding(10.dp) // 进一步减少内边距
                    ) {
                        // 内容类型标签
                        Surface(
                            modifier = Modifier.padding(bottom = 4.dp), // 进一步减少间距
                            shape = RoundedCornerShape(4.dp), // 减少圆角
                            color = primaryColor.copy(alpha = 0.08f) // 降低透明度
                        ) {
                            Text(
                                text = when (item.type) {
                                    ConversationType.USER -> "用户输入"
                                    ConversationType.SYSTEM_RESPONSE -> "系统消息"
                                    ConversationType.SUCCESS -> "API响应"
                                    ConversationType.ERROR -> "错误详情"
                                },
                                fontSize = 9.sp, // 减小字体
                                color = primaryColor,
                                fontWeight = FontWeight.SemiBold,
                                modifier = Modifier.padding(horizontal = 4.dp, vertical = 1.dp) // 进一步减少内边距
                            )
                        }
                        
                        // 主要内容
                        Text(
                            text = item.content,
                            fontSize = 12.sp, // 减小字体以节省空间
                            color = textColor,
                            fontFamily = androidx.compose.ui.text.font.FontFamily.Monospace,
                            lineHeight = 16.sp, // 减少行高
                            overflow = TextOverflow.Visible
                        )
                    }
                }
            }
        }
    }
}

// 辅助数据类，用于存储颜色组合
data class Tuple4<A, B, C, D>(
    val first: A,
    val second: B,
    val third: C,
    val fourth: D
)

// 处理发送按钮点击事件的函数
private fun handleSendButtonClick(
    inputText: String,
    sessionSn: String,
    conversationList: MutableList<ConversationItem>,
    coroutineScope: kotlinx.coroutines.CoroutineScope
) {
    if (inputText.isNotEmpty() && sessionSn.isNotEmpty()) {
        val userInput = inputText
        
        // 在UI线程添加用户问题到对话记录
        coroutineScope.launch(kotlinx.coroutines.Dispatchers.Main) {
            conversationList.add(
                ConversationItem(
                    type = ConversationType.USER,
                    content = userInput,
                    time = "刚刚"
                )
            )
        }
        
        // 使用协程在后台线程发送API请求
        coroutineScope.launch(kotlinx.coroutines.Dispatchers.IO) {
            try {
                // 设置请求URL
                val url = java.net.URL("https://api.xbotspace.com/agent-api/v1/open/knowledge/chat?agentType=doc")
                
                // 打开连接
                val connection = url.openConnection() as java.net.HttpURLConnection
                
                // 设置请求方法和头信息
                connection.requestMethod = "POST"
                connection.setRequestProperty("Authorization", "26ae4908-ec15-49fb-bd4f-9181bfc3bd71")
                connection.setRequestProperty("Content-Type", "application/json")
                connection.doOutput = true
                
                // 设置请求体
                val requestBody = "{\"sessionSn\":\"$sessionSn\",\"msgContent\":\"$userInput\",\"msgType\":\"text\",\"stream\":true}"
                val outputStream = connection.outputStream
                outputStream.write(requestBody.toByteArray())
                outputStream.flush()
                outputStream.close()
                
                // 获取响应
                val responseCode = connection.responseCode
                if (responseCode == java.net.HttpURLConnection.HTTP_OK) {
                    // 处理流式响应
                    val reader = connection.inputStream.bufferedReader()
                    val answerList = mutableListOf<String>()
                    var lastAnswer = ""
                    
                    try {
                        var line: String?
                        while (reader.readLine().also { line = it } != null) {
                            if (line?.startsWith("data:") == true) {
                                // 去掉开头的"data:"
                                val jsonStr = line?.substring(5)?.trim()
                                if (jsonStr != null && jsonStr.isNotEmpty()) {
                                    try {
                                        // 解析JSON
                                        val jsonObject = org.json.JSONObject(jsonStr)
                                        val dataObject = jsonObject.optJSONObject("data")
                                        if (dataObject != null) {
                                            val contentObject = dataObject.optJSONObject("content")
                                            if (contentObject != null) {
                                                val answer = contentObject.optString("answer", "")
                                                answerList.add(answer)
                                                lastAnswer = answer
                                            }
                                        }
                                    } catch (e: org.json.JSONException) {
                                        // 忽略JSON解析错误
                                    }
                                }
                            }
                        }
                    } finally {
                        reader.close()
                        connection.disconnect()
                    }
                    
                    // 处理答案
                    val finalAnswer = if (answerList.isNotEmpty()) {
                        // 抛弃最后一个数据包
                        val filteredAnswers = answerList.subList(0, answerList.size - 1)
                        // 拼接所有提取的字符串
                        val concatenated = filteredAnswers.joinToString("")
                        // 如果拼接结果为空，输出最后一个answer字段
                        if (concatenated.isEmpty()) {
                            lastAnswer
                        } else {
                            concatenated
                        }
                    } else {
                        ""
                    }
                    
                    // 在主线程更新UI
                    coroutineScope.launch(kotlinx.coroutines.Dispatchers.Main) {
                        // 添加API请求命令到对话记录
                        conversationList.add(
                            ConversationItem(
                                type = ConversationType.SYSTEM_RESPONSE,
                                content = "curl --location --request POST '`https://api.xbotspace.com/agent-api/v1/open/knowledge/chat?agentType=doc`' \\n" +
                                        "--header 'Authorization: 26ae4908-ec15-49fb-bd4f-9181bfc3bd71' \\n" +
                                        "--header 'Content-Type: application/json' \\n" +
                                        "--data-raw '{\\n" +
                                        "    \"sessionSn\": \"str_session_sn\", \\n" +
                                        "    \"msgContent\": \"输入字符串\", \\n" +
                                        "    \"msgType\": \"text\", \\n" +
                                        "    \"stream\": true \\n" +
                                        "}\\'",
                                time = "刚刚"
                            )
                        )
                        // 添加API响应到对话记录
                        conversationList.add(
                            ConversationItem(
                                type = ConversationType.SUCCESS,
                                content = finalAnswer,
                                time = "刚刚"
                            )
                        )
                    }
                } else {
                    // 关闭连接
                    connection.disconnect()
                    
                    // 在主线程更新UI
                    coroutineScope.launch(kotlinx.coroutines.Dispatchers.Main) {
                        // 添加API请求命令到对话记录
                        conversationList.add(
                            ConversationItem(
                                type = ConversationType.SYSTEM_RESPONSE,
                                content = "curl --location --request POST '`https://api.xbotspace.com/agent-api/v1/open/knowledge/chat?agentType=doc`' \\n" +
                                        "--header 'Authorization: 26ae4908-ec15-49fb-bd4f-9181bfc3bd71' \\n" +
                                        "--header 'Content-Type: application/json' \\n" +
                                        "--data-raw '{\\n" +
                                        "    \"sessionSn\": \"str_session_sn\", \\n" +
                                        "    \"msgContent\": \"输入字符串\", \\n" +
                                        "    \"msgType\": \"text\", \\n" +
                                        "    \"stream\": true \\n" +
                                        "}\\'",
                                time = "刚刚"
                            )
                        )
                        // 添加错误信息到对话记录
                        conversationList.add(
                            ConversationItem(
                                type = ConversationType.ERROR,
                                content = "请求失败，响应码: $responseCode",
                                time = "刚刚"
                            )
                        )
                    }
                }
            } catch (e: Exception) {
                // 处理异常
                coroutineScope.launch(kotlinx.coroutines.Dispatchers.Main) {
                    conversationList.add(
                        ConversationItem(
                            type = ConversationType.SYSTEM_RESPONSE,
                            content = "API请求异常: ${e.message}",
                            time = "刚刚"
                        )
                    )
                }
            }
        }
    } else if (sessionSn.isEmpty()) {
        // sessionSn为空时的提示
        coroutineScope.launch(kotlinx.coroutines.Dispatchers.Main) {
            conversationList.add(
                ConversationItem(
                    type = ConversationType.SYSTEM_RESPONSE,
                    content = "系统提示: 连接尚未建立，请等待智能体握手完成",
                    time = "刚刚"
                )
            )
        }
    }
}

// 对话类型枚举
enum class ConversationType {
    USER,
    SYSTEM_RESPONSE,
    SUCCESS,
    ERROR
}

// 对话数据类
data class ConversationItem(
    val type: ConversationType,
    val content: String,
    val time: String
)

@Preview(showBackground = true)
@Composable
fun TrafficLawAgentScreenPreview() {
    API_DemoTheme {
        TrafficLawAgentScreen()
    }
}