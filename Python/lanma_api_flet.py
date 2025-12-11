#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
澜码API Demo
使用Flet框架重写的图形界面程序
"""

import flet as ft
import threading
import json
import requests
import asyncio
from requests.exceptions import RequestException

class LanmaAPIDemo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "澜码API Demo"
        self.page.window.width = 800
        self.page.window.height = 600
        
        # 变量定义
        self.apikey = "26ae4908-ec15-49fb-bd4f-9181bfc3bd71"
        self.agent_sn = "agent-4778817f457648b09e50e"
        self.versn = "ver-26178f53ed4548bebad6f"
        self.session_sn = "NA"
        
        # UI 元素引用
        self.status_text = None
        self.input_textfield = None
        self.output_text = None
        
        self.create_widgets()
        
        # 程序启动后自动执行握手
        print("初始化完成，准备执行握手...")
        self.handshake_with_agent()
    
    def create_widgets(self):
        # 主容器
        main_container = ft.Container(
            padding=10,
            expand=True
        )
        
        # 会话信息区域
        session_frame = ft.Container(
            content=ft.Column([
                ft.Text("会话信息", style=ft.TextThemeStyle.TITLE_MEDIUM),
                ft.Row([
                    ft.Text("API 连接状态: ", width=150),
                    ft.Container(
                        content=self.status_text if self.status_text else ft.Text("正在连接中...", color=ft.Colors.GREY),
                        expand=True,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=4,
                        padding=5
                    )
                ])
            ]),
            padding=10,
            margin=ft.Margin(0, 0, 0, 10),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8
        )
        
        # 操作区域
        operation_frame = ft.Container(
            content=ft.Column([
                ft.Text("操作区域", style=ft.TextThemeStyle.TITLE_MEDIUM),
                
                # 输入框区域
                ft.Row([
                    ft.Text("和智能体问答: ", width=150),
                    self.input_textfield if self.input_textfield else ft.TextField(
                        expand=True,
                        hint_text="请输入您的问题",
                        on_submit=lambda e: self.submit_input()
                    )
                ]),
                
                # 输出区域
                ft.Column([
                    ft.Text("智能体回复: ", width=150),
                    ft.Container(
                        content=self.output_text if self.output_text else ft.Text("正在等待连接..."),
                        expand=True,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=4,
                        padding=5,
                        margin=ft.Margin(0, 5, 0, 0),
                        bgcolor=ft.Colors.GREY_50
                    )
                ])
            ]),
            padding=10,
            expand=True,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8
        )
        
        # 更新UI元素引用
        print("更新UI元素引用...")
        print(f"Session frame controls: {len(session_frame.content.controls)}")
        print(f"Operation frame controls: {len(operation_frame.content.controls)}")
        
        if not self.status_text:
            self.status_text = session_frame.content.controls[1].controls[1].content
            print(f"Status text initialized: {self.status_text}")
        if not self.input_textfield:
            self.input_textfield = operation_frame.content.controls[1].controls[1]
            print(f"Input textfield initialized: {self.input_textfield}")
        if not self.output_text:
            self.output_text = operation_frame.content.controls[2].controls[1].content
            print(f"Output text initialized: {self.output_text}")
        
        # 将所有组件添加到主容器
        main_container.content = ft.Column([
            session_frame,
            operation_frame
        ], expand=True)
        
        # 将主容器添加到页面
        self.page.add(main_container)
    
    def handshake_with_agent(self):
        """和智能体握手"""
        print("开始执行握手...")
        print(f"API Key: {self.apikey}")
        print(f"Agent SN: {self.agent_sn}")
        print(f"Version SN: {self.versn}")
        
        if not self.apikey or not self.agent_sn or not self.versn:
            print("参数不完整")
            self.update_status("请填写完整的API Key、Agent sn和Agent version sn", ft.Colors.RED)
            return
        
        # 在新线程中执行握手操作
        def execute_handshake():
            try:
                print("开始执行网络请求...")
                self.update_output("正在与智能体握手...")
                
                # 使用requests库发送POST请求
                url = "https://api.xbotspace.com/agent-api/v1/open/sessions"
                headers = {
                    "Authorization": self.apikey,
                    "Content-Type": "application/json"
                }
                data = {
                    "agentSn": self.agent_sn,
                    "verSn": self.versn
                }
                
                print(f"请求URL: {url}")
                print(f"请求头: {headers}")
                print(f"请求数据: {data}")
                
                response = requests.post(url, headers=headers, json=data, timeout=30)
                print(f"响应状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                
                response.raise_for_status()  # 检查请求是否成功
                
                # 解析响应数据
                response_data = response.json()
                print(f"解析后的响应数据: {response_data}")
                
                # 提取sessionSn
                session_sn = None
                user_sn = None
                
                print("开始提取sessionSn...")
                
                if 'data' in response_data and isinstance(response_data['data'], dict):
                    print("响应数据包含data字段")
                    if 'sessionSn' in response_data['data']:
                        session_sn = response_data['data']['sessionSn']
                        print(f"从data中提取到sessionSn: {session_sn}")
                    if 'userSn' in response_data['data']:
                        user_sn = response_data['data']['userSn']
                        print(f"从data中提取到userSn: {user_sn}")
                elif 'sessionSn' in response_data:
                    session_sn = response_data['sessionSn']
                    print(f"直接从响应中提取到sessionSn: {session_sn}")
                if 'userSn' in response_data:
                    user_sn = response_data['userSn']
                    print(f"直接从响应中提取到userSn: {user_sn}")
                
                print(f"最终提取到的sessionSn: {session_sn}")
                print(f"最终提取到的userSn: {user_sn}")
                
                if session_sn:
                    print("sessionSn存在，准备更新状态...")
                    self.session_sn = session_sn
                    print(f"session_sn变量已更新: {self.session_sn}")
                    self.update_status("【RAG 1.0】 智能查询 连接成功", ft.Colors.GREEN)
                    print("状态已更新")
                    self.update_output(f"🎉 API连接成功！\n{'✅ 用户ID: ' + user_sn if user_sn else ''}\n✅ 可以开始智能查询了")
                    print("输出已更新")
                else:
                    self.update_status("API连接失败: 无法获取sessionSn", ft.Colors.RED)
                    self.update_output(f"API连接失败: 无法获取sessionSn\n响应内容: {response.text}")
                    
            except RequestException as e:
                print(f"RequestException: {str(e)}")
                self.update_status(f"API连接失败: {str(e)}", ft.Colors.RED)
                self.update_output(f"执行出错: {str(e)}")
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {str(e)}")
                self.update_status(f"API连接失败: 响应格式错误", ft.Colors.RED)
                self.update_output(f"JSON解析错误: {str(e)}")
            except Exception as e:
                print(f"Exception: {str(e)}")
                import traceback
                traceback.print_exc()
                self.update_status(f"API连接失败: {str(e)}", ft.Colors.RED)
                self.update_output(f"执行出错: {str(e)}")
        
        # 启动线程
        thread = threading.Thread(target=execute_handshake)
        thread.daemon = True
        thread.start()
    
    def submit_input(self):
        """处理输入按钮点击事件，发送知识查询请求"""
        input_text = self.input_textfield.value.strip()
        if not input_text:
            return
        
        if not self.session_sn or self.session_sn == "NA":
            self.update_output("请先获取sessionSn")
            return
        
        # 在新线程中执行查询操作
        def execute_query():
            try:
                self.update_output(f"用户问题：{input_text}\n")
                
                # 使用requests库发送POST请求
                url = "https://api.xbotspace.com/agent-api/v1/open/knowledge/chat?agentType=doc"
                headers = {
                    "Authorization": self.apikey,
                    "Content-Type": "application/json"
                }
                data = {
                    "sessionSn": self.session_sn,
                    "msgContent": input_text,
                    "msgType": "text",
                    "stream": True
                }
                
                # 发送请求并处理流式响应
                with requests.post(url, headers=headers, json=data, stream=True, timeout=120) as response:
                    response.raise_for_status()  # 检查请求是否成功
                    
                    # 处理流式响应
                    self.process_stream_response(response)
                    
            except RequestException as e:
                self.update_output(f"执行出错: {str(e)}")
            except Exception as e:
                self.update_output(f"执行出错: {str(e)}")
        
        # 清空输入框
        self.input_textfield.value = ""
        self.page.update()
        
        # 启动线程
        thread = threading.Thread(target=execute_query)
        thread.daemon = True
        thread.start()
    
    def process_stream_response(self, response):
        """处理流式响应，提取answer值并显示在输出区域"""
        answer_parts = []
        
        # 逐行读取流式响应
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8').strip()
                if line.startswith('data:{') and line.endswith('}'):
                    try:
                        # 提取JSON部分
                        json_str = line[5:]  # 去掉'data:'前缀
                        data = json.loads(json_str)
                        
                        # 提取answer值
                        if 'data' in data and 'content' in data['data']:
                            answer = data['data']['content'].get('answer', '')
                            if answer:  # 只添加非空answer
                                answer_parts.append(answer)
                                # 实时更新输出
                                self.update_output(f"智能体回答：{''.join(answer_parts)}")
                    
                    except json.JSONDecodeError:
                        continue
        
        # 最终处理：如果有多个部分，去掉最后一个（原始逻辑）
        if len(answer_parts) > 1:
            final_answer = ''.join(answer_parts[:-1])
        else:
            final_answer = ''.join(answer_parts)
        
        if final_answer:
            self.update_output(f"智能体回答：{final_answer}")
        else:
            self.update_output("智能体回答：未获取到有效答案")
    
    def update_status(self, text, color=ft.Colors.BLACK):
        """更新状态文本"""
        try:
            print(f"开始更新状态: {text}, 颜色: {color}")
            print(f"self.status_text: {self.status_text}")
            print(f"self.page: {self.page}")
            
            # 异步UI更新函数
            async def update_ui():
                print("在UI线程中更新状态...")
                self.status_text.value = text
                self.status_text.color = color
                self.page.update()
                print("UI更新完成")
            
            # 在主线程中执行UI更新
            self.page.run_task(update_ui)
                
        except Exception as e:
            print(f"更新状态时出错: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def update_output(self, text):
        """更新输出文本"""
        try:
            print(f"开始更新输出: {text}")
            print(f"self.output_text: {self.output_text}")
            print(f"self.page: {self.page}")
            
            # 异步UI更新函数
            async def update_ui():
                print("在UI线程中更新输出...")
                self.output_text.value = text
                self.page.update()
                print("UI更新完成")
            
            # 在主线程中执行UI更新
            self.page.run_task(update_ui)
                
        except Exception as e:
            print(f"更新输出时出错: {str(e)}")
            import traceback
            traceback.print_exc()

def main(page: ft.Page):
    app = LanmaAPIDemo(page)

if __name__ == "__main__":
    ft.app(target=main)