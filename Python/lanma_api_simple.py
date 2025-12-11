#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
澜码API Demo
图形界面程序，用于生成和测试澜码API命令
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import json
import subprocess
import os

class LanmaAPIDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("澜码API Demo")
        self.root.geometry("450x350")
        
        # 变量定义
        self.str_apikey = tk.StringVar(value="26ae4908-ec15-49fb-bd4f-9181bfc3bd71")
        self.str_agent_sn = tk.StringVar(value="agent-4778817f457648b09e50e")
        self.str_versn = tk.StringVar(value="ver-26178f53ed4548bebad6f")
        self.str_session_sn = tk.StringVar(value="NA")
        self.str_command_init = tk.StringVar()

        self.str_input = tk.StringVar()
        self.str_output = tk.StringVar()
        self.str_processed = tk.StringVar()
        
        # 历史记录
        self.output_history = []
        self.processed_history = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 第一部分：API配置（隐藏输入框，保留功能）
        api_frame = ttk.Frame(main_frame)
        api_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        api_frame.columnconfigure(0, weight=1)
        
        # sessionSn显示窗口（只读，移动到操作区域上方）
        session_frame = ttk.LabelFrame(main_frame, text="会话信息", padding="10")
        session_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        session_frame.columnconfigure(1, weight=1)
        
        ttk.Label(session_frame, text="API 连结状态:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.session_sn_entry = tk.Entry(session_frame, width=50, state="readonly", fg="gray")
        self.session_sn_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        # 初始显示为等待状态
        self.session_sn_entry.config(state='normal')
        self.session_sn_entry.insert(0, "正在连接中...")
        self.session_sn_entry.config(fg="gray", state='readonly')
        

        
        session_frame.columnconfigure(1, weight=1)
        

        

        
        # 第二部分：操作区域
        operation_frame = ttk.LabelFrame(main_frame, text="操作区域", padding="10")
        operation_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        operation_frame.columnconfigure(1, weight=1)
        operation_frame.rowconfigure(1, weight=1)
        
        # 第一行：输入框
        ttk.Label(operation_frame, text="和智能体问答:").grid(row=0, column=0, sticky=tk.W, pady=2)
        # 创建输入框并赋值给变量，以便绑定事件
        self.input_entry = ttk.Entry(operation_frame, textvariable=self.str_input, width=60)
        self.input_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        # 绑定回车键到submit_input函数
        self.input_entry.bind('<Return>', lambda event: self.submit_input())
        

        
        # Output
        ttk.Label(operation_frame, text="智能体回复:").grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(10, 0))
        self.output_frame = ttk.Frame(operation_frame)
        self.output_frame.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0), padx=(10, 0))
        self.output_frame.columnconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(self.output_frame, height=16, width=70)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置蓝色文本标签
        self.output_text.tag_configure("blue", foreground="blue")
        
        output_button_frame = ttk.Frame(self.output_frame)
        output_button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        

        


        
        # 配置主框架网格权重
        main_frame.rowconfigure(2, weight=1)
        
        # 程序启动后自动执行握手
        self.root.after(500, self.handshake_with_agent)  # 延迟500ms执行，确保界面完全加载
    
    def handshake_with_agent(self):
        """和智能体握手"""
        apikey = self.str_apikey.get().strip()
        agent_sn = self.str_agent_sn.get().strip()
        versn = self.str_versn.get().strip()
        
        if not apikey or not agent_sn or not versn:
            messagebox.showwarning("警告", "请填写完整的API Key、Agent sn和Agent version sn")
            return
        
        command = f"""curl -X POST 'https://api.xbotspace.com/agent-api/v1/open/sessions' \\
--header 'Authorization: {apikey}' \\
--header 'Content-Type: application/json' \\
--data-raw '{{"agentSn":"{agent_sn}","verSn":"{versn}"}}'"""
        
        # 在新线程中执行命令
        def execute_handshake_command():
            try:
                # 清空Output窗口，准备显示握手结果
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "正在与智能体握手...\n", "blue")
                self.root.update()
                
                # 将curl命令转换为适合subprocess执行的格式
                command_lines = [line.strip().rstrip('\\') for line in command.split('\n') if line.strip()]
                clean_command = ' '.join(command_lines)
                
                # 执行命令并实时显示结果
                process = subprocess.Popen(clean_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)
                
                # 读取输出，但不显示原始数据
                output_buffer = ""
                while True:
                    # 逐行读取
                    line = process.stdout.readline()
                    if line == '' and process.poll() is not None:
                        break
                    if line:
                        output_buffer += line
                
                # 确保没有遗漏的输出
                remaining_output = process.stdout.read()
                if remaining_output:
                    output_buffer += remaining_output
                
                # 从output_buffer中解析JSON响应，提取session信息
                if output_buffer:
                    # 按行分割，查找JSON格式
                    lines = output_buffer.strip().split('\n')
                    response_data = None
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('{') and line.endswith('}'):
                            try:
                                # 去掉末尾可能的%符号
                                json_str = line.rstrip('%')
                                response_data = json.loads(json_str)
                                break
                            except json.JSONDecodeError:
                                continue
                    
                    if response_data is None:
                        # 如果单行没有找到，尝试在整个buffer中查找JSON
                        json_start = output_buffer.find('{')
                        if json_start != -1:
                            json_end = output_buffer.rfind('}') + 1
                            if json_end > json_start:
                                try:
                                    json_str = output_buffer[json_start:json_end]
                                    json_str = json_str.rstrip('%')
                                    response_data = json.loads(json_str)
                                except json.JSONDecodeError:
                                    pass
                
                if response_data:
                    # 提取sessionSn
                    session_sn = None
                    user_sn = None
                        
                    # 优先从data对象中提取sessionSn
                    if 'data' in response_data and isinstance(response_data['data'], dict):
                        if 'sessionSn' in response_data['data']:
                            session_sn = response_data['data']['sessionSn']
                        if 'userSn' in response_data['data']:
                            user_sn = response_data['data']['userSn']
                    # 备用：直接从根对象提取sessionSn
                    elif 'sessionSn' in response_data:
                        session_sn = response_data['sessionSn']
                    if 'userSn' in response_data:
                        user_sn = response_data['userSn']
                    
                    if session_sn:
                        # 使用多种方式确保更新
                        self.str_session_sn.set(session_sn)
                        self.root.update_idletasks()
                        
                        # 更新API连接状态显示为成功消息
                        if hasattr(self, 'session_sn_entry'):
                            self.session_sn_entry.config(state='normal')
                            self.session_sn_entry.delete(0, tk.END)
                            self.session_sn_entry.insert(0, "【RAG 1.0】 智能查询 连结成功")
                            self.session_sn_entry.config(fg="green", state='readonly')
                        
                        self.root.update()
                        # 再次强制刷新界面显示
                        self.root.update_idletasks()
                        
                        # 在Output窗口显示连接成功信息
                        self.output_text.insert(tk.END, f"\n\n🎉 API连接成功！", "blue")
                        if user_sn:
                            self.output_text.insert(tk.END, f"\n✅ 用户ID: {user_sn}", "blue")
                        self.output_text.insert(tk.END, f"\n✅ 可以开始智能查询了", "blue")
                        self.output_text.insert(tk.END, "\n", "blue")
                        self.root.update()
                        # 再次强制刷新界面显示
                        self.root.update_idletasks()
                
            except Exception as e:
                self.output_text.insert(tk.END, f"\n执行出错: {str(e)}", "blue")
                self.root.update()
        
        # 启动线程
        thread = threading.Thread(target=execute_handshake_command)
        thread.daemon = True
        thread.start()
    

    def submit_input(self):
        """处理输入按钮点击事件，发送知识查询请求"""
        input_text = self.str_input.get().strip()
        if not input_text:
            messagebox.showwarning("警告", "请输入内容")
            return
        
        session_sn = self.str_session_sn.get().strip()
        if not session_sn or session_sn == "NA":
            messagebox.showwarning("警告", "请先点击'和智能体握手'获取sessionSn")
            return
        
        # 使用知识查询的JSON格式
        chat_command = f"""curl --location --request POST 'https://api.xbotspace.com/agent-api/v1/open/knowledge/chat?agentType=doc' \\
--header 'Authorization: {self.str_apikey.get()}' \\
--header 'Content-Type: application/json' \\
--data-raw '{{"sessionSn":"{session_sn}","msgContent":"{input_text}","msgType":"text","stream":true}}'"""
        
        # 在新线程中执行命令
        def execute_chat_command():
            try:
                # 清空Output窗口并显示新的内容
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f"用户问题：{input_text}\n")
                self.root.update()
                
                # 将curl命令转换为适合subprocess执行的格式
                command_lines = [line.strip().rstrip('\\') for line in chat_command.split('\n') if line.strip()]
                clean_command = ' '.join(command_lines)
                
                # 知识查询使用subprocess.run方式
                result = subprocess.run(clean_command, shell=True, capture_output=True, text=True, timeout=120)  # 增加超时时间到120秒
                
                # 处理流式响应，提取answer值
                if result.stdout:
                    # 解析流式响应，提取answer值（不在Output窗口显示原始响应）
                    self.process_stream_response(result.stdout)
                    self.root.update()  # 立即更新界面
                
            except subprocess.TimeoutExpired:
                self.output_text.insert(tk.END, "\n命令执行超时（等待时间超过120秒）", "blue")
                self.root.update()
            except Exception as e:
                self.output_text.insert(tk.END, f"\n执行出错: {str(e)}", "blue")
                self.root.update()
        
        # 清空输入框
        self.str_input.set("")
        
        # 启动线程
        thread = threading.Thread(target=execute_chat_command)
        thread.daemon = True
        thread.start()
    
    def process_stream_response(self, response_text):
        """处理流式响应，提取answer值并显示在Processed窗口"""
        import re
        
        # 按行分割响应
        lines = response_text.strip().split('\n')
        answer_parts = []
        
        # 解析每一行
        for line in lines:
            line = line.strip()
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
                            
                except json.JSONDecodeError:
                    continue
        
        # 抛弃最后一个answer值，拼接剩余的answer
        if len(answer_parts) > 1:
            processed_answer = ''.join(answer_parts[:-1])  # 去掉最后一个
        else:
            processed_answer = ''.join(answer_parts)  # 如果只有一个，就使用它
        
        # 在Output窗口显示结果
        if processed_answer:
            self.output_text.insert(tk.END, f"\n\n智能体回答：\n{processed_answer}\n", "blue")
        else:
            self.output_text.insert(tk.END, "\n\n智能体回答：未获取到有效答案\n", "blue")
    

    



def main():
    root = tk.Tk()
    app = LanmaAPIDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main()