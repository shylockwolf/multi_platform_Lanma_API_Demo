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
        self.root.geometry("900x700")
        
        # 变量定义
        self.str_apikey = tk.StringVar(value="26ae4908-ec15-49fb-bd4f-9181bfc3bd71")
        self.str_agent_sn = tk.StringVar(value="agent-239adfced8584969be508")
        self.str_versn = tk.StringVar(value="ver-a180cc852eab45ce8c471")
        self.str_session_sn = tk.StringVar(value="NA")
        self.str_command_init = tk.StringVar()
        self.str_agent_type = tk.StringVar(value="知识查询")
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
        
        # 第一部分：API密钥和基本信息
        api_frame = ttk.LabelFrame(main_frame, text="API配置", padding="10")
        api_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        api_frame.columnconfigure(1, weight=1)
        
        # 窗口1: API Key
        ttk.Label(api_frame, text="API Key*:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(api_frame, textvariable=self.str_apikey, width=30).grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # sessionSn显示窗口（只读）
        ttk.Label(api_frame, text="sessionSn:").grid(row=0, column=2, sticky=tk.W, pady=2, padx=(20, 0))
        self.session_sn_entry = ttk.Entry(api_frame, textvariable=self.str_session_sn, width=30, state="readonly")
        self.session_sn_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        # 窗口2和3并排: Agent sn 和 Agent version sn
        ttk.Label(api_frame, text="Agent sn*:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(api_frame, textvariable=self.str_agent_sn, width=30).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        ttk.Label(api_frame, text="Agent version sn*:").grid(row=1, column=2, sticky=tk.W, pady=2, padx=(20, 0))
        ttk.Entry(api_frame, textvariable=self.str_versn, width=30).grid(row=1, column=3, sticky=(tk.W, tk.E), pady=2, padx=(10, 0))
        
        api_frame.columnconfigure(1, weight=1)
        api_frame.columnconfigure(3, weight=1)
        
        # 和智能体握手按钮
        ttk.Button(api_frame, text="和智能体握手", command=self.handshake_with_agent).grid(row=2, column=0, columnspan=4, pady=(10, 0))
        

        

        
        # 第二部分：操作区域
        operation_frame = ttk.LabelFrame(main_frame, text="操作区域", padding="10")
        operation_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        operation_frame.columnconfigure(1, weight=1)
        operation_frame.rowconfigure(1, weight=1)
        operation_frame.rowconfigure(2, weight=1)
        
        # 第一行：Agent Type 和 Input
        # Agent Type
        ttk.Label(operation_frame, text="Agent Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        agent_type_combo = ttk.Combobox(operation_frame, textvariable=self.str_agent_type, values=["知识查询", "对话流"], state="readonly", width=20)
        agent_type_combo.grid(row=0, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        
        # Input
        ttk.Label(operation_frame, text="和智能体问答:").grid(row=0, column=2, sticky=tk.W, pady=2, padx=(50, 0))
        # 创建输入框并赋值给变量，以便绑定事件
        self.input_entry = ttk.Entry(operation_frame, textvariable=self.str_input, width=40)
        self.input_entry.grid(row=0, column=3, sticky=tk.W, pady=2, padx=(10, 0))
        # 绑定回车键到submit_input函数
        self.input_entry.bind('<Return>', lambda event: self.submit_input())
        

        
        # Output
        ttk.Label(operation_frame, text="Output:").grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(10, 0))
        self.output_frame = ttk.Frame(operation_frame)
        self.output_frame.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0), padx=(10, 0))
        self.output_frame.columnconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(self.output_frame, height=16, width=70)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置蓝色文本标签
        self.output_text.tag_configure("blue", foreground="blue")
        
        output_button_frame = ttk.Frame(self.output_frame)
        output_button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        

        
        # Processed
        ttk.Label(operation_frame, text="Processed:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=(10, 0))
        self.processed_frame = ttk.Frame(operation_frame)
        self.processed_frame.grid(row=2, column=1, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0), padx=(10, 0))
        self.processed_frame.columnconfigure(0, weight=1)
        
        self.processed_text = scrolledtext.ScrolledText(self.processed_frame, height=8, width=70)
        self.processed_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        processed_button_frame = ttk.Frame(self.processed_frame)
        processed_button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        

        
        # 配置主框架网格权重
        main_frame.rowconfigure(1, weight=1)
    
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
                # 在Output窗口显示执行的命令
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f"和智能体握手 - 执行命令:\n{command}\n\n")
                self.output_text.insert(tk.END, "执行结果:\n", "blue")
                self.root.update()
                
                # 将curl命令转换为适合subprocess执行的格式
                command_lines = [line.strip().rstrip('\\') for line in command.split('\n') if line.strip()]
                clean_command = ' '.join(command_lines)
                
                # 执行命令并实时显示结果
                process = subprocess.Popen(clean_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)
                
                # 流式读取输出，按行显示
                output_buffer = ""
                update_counter = 0
                while True:
                    # 逐行读取
                    line = process.stdout.readline()
                    if line == '' and process.poll() is not None:
                        break
                    if line:
                        output_buffer += line
                        # 实时显示每行（蓝色）
                        self.output_text.insert(tk.END, line, "blue")
                        self.output_text.see(tk.END)  # 自动滚动到底部
                        update_counter += 1
                        # 每3行更新一次UI
                        if update_counter % 3 == 0:
                            self.root.update()
                
                # 确保没有遗漏的输出
                remaining_output = process.stdout.read()
                if remaining_output:
                    output_buffer += remaining_output
                    # 批量显示剩余内容
                    self.output_text.insert(tk.END, remaining_output, "blue")
                    self.output_text.see(tk.END)
                
                # 解析JSON响应，提取session信息
                full_output = self.output_text.get(1.0, tk.END)
                
                # 尝试提取JSON部分（找到"执行结果:"后的JSON）
                result_marker = "执行结果:"
                result_start = full_output.find(result_marker)
                if result_start != -1:
                    json_start = full_output.find('{', result_start)
                else:
                    json_start = full_output.find('{')
                
                if json_start != -1:
                    try:
                        json_end = full_output.rfind('}') + 1
                        json_str = full_output[json_start:json_end]
                        # 去掉末尾可能的%符号
                        json_str = json_str.rstrip('%')
                        response_data = json.loads(json_str)
                        
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
                            
                            # 强制重新配置sessionSn输入框
                            if hasattr(self, 'session_sn_entry'):
                                self.session_sn_entry.config(state='normal')
                                self.session_sn_entry.delete(0, tk.END)
                                self.session_sn_entry.insert(0, session_sn)
                                self.session_sn_entry.config(state='readonly')
                            
                            self.root.update()
                            # 再次强制刷新界面显示
                            self.root.update_idletasks()
                            
                            # 在Output窗口显示提取的session信息
                            self.output_text.insert(tk.END, f"\n\n✅ 成功提取sessionSn: {session_sn}", "blue")
                            if user_sn:
                                self.output_text.insert(tk.END, f"\n✅ 成功提取userSn: {user_sn}", "blue")
                            self.output_text.insert(tk.END, f"\n✅ sessionSn已更新到界面显示框", "blue")
                            self.output_text.insert(tk.END, "\n", "blue")
                            self.root.update()
                            # 再次强制刷新界面显示
                            self.root.update_idletasks()
                    except json.JSONDecodeError:
                        pass  # 静默处理JSON解析错误
                
            except Exception as e:
                self.output_text.insert(tk.END, f"\n执行出错: {str(e)}", "blue")
                self.root.update()
        
        # 启动线程
        thread = threading.Thread(target=execute_handshake_command)
        thread.daemon = True
        thread.start()
    

    def submit_input(self):
        """处理输入按钮点击事件，发送聊天请求"""
        input_text = self.str_input.get().strip()
        if not input_text:
            messagebox.showwarning("警告", "请输入内容")
            return
        
        session_sn = self.str_session_sn.get().strip()
        if not session_sn or session_sn == "NA":
            messagebox.showwarning("警告", "请先点击'继续取得信息'获取sessionSn")
            return
        
        # 根据agent type选择不同的命令模板
        if self.str_agent_type.get() == "对话流":
            # 对话流使用form表单格式
            chat_command = f"""curl -X POST 'https://api.xbotspace.com/agent-api/v1/open/agents/chat' \\
--header 'Authorization: {self.str_apikey.get()}' \\
--form 'sessionSn="{session_sn}"' \\
--form 'msgContent="{input_text}"' \\
--form 'msgType="text"' \\
--form 'delayInMs=20' \\
--form 'stream=true' \\
--form 'streamMode="delta"'"""
        else:
            # 知识查询使用原来的JSON格式
            chat_command = f"""curl --location --request POST 'https://api.xbotspace.com/agent-api/v1/open/knowledge/chat?agentType=doc' \\
--header 'Authorization: {self.str_apikey.get()}' \\
--header 'Content-Type: application/json' \\
--data-raw '{{"sessionSn":"{session_sn}","msgContent":"{input_text}","msgType":"text","stream":true}}'"""
        
        # 在新线程中执行命令
        def execute_chat_command():
            try:
                # 清空Output和Processed窗口并显示新的内容
                self.output_text.delete(1.0, tk.END)
                self.processed_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f"用户输入: {input_text}")
                self.output_text.insert(tk.END, f"\n执行命令:\n{chat_command}\n\n")
                self.output_text.insert(tk.END, "API响应:\n", "blue")
                self.root.update()
                
                # 将curl命令转换为适合subprocess执行的格式
                command_lines = [line.strip().rstrip('\\') for line in chat_command.split('\n') if line.strip()]
                clean_command = ' '.join(command_lines)
                
                # 根据agent type选择不同的执行方式
                if self.str_agent_type.get() == "对话流":
                    # 对话流使用流式处理
                    process = subprocess.Popen(clean_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)
                    
                    # 流式读取输出
                    output_buffer = ""
                    update_counter = 0
                    while True:
                        # 逐行读取
                        line = process.stdout.readline()
                        if line == '' and process.poll() is not None:
                            break
                        if line:
                            output_buffer += line
                            # 实时显示每行（蓝色）
                            self.output_text.insert(tk.END, line, "blue")
                            self.output_text.see(tk.END)  # 自动滚动到底部
                            update_counter += 1
                            # 每5行更新一次UI，避免过度刷新
                            if update_counter % 5 == 0:
                                self.root.update()
                    
                    # 解析流式响应，提取answer值
                    if output_buffer:
                        self.process_chat_stream_response(output_buffer)
                else:
                    # 知识查询使用原来的方式
                    result = subprocess.run(clean_command, shell=True, capture_output=True, text=True, timeout=120)  # 增加超时时间到120秒
                    
                    # 处理流式响应，提取answer值
                    if result.stdout:
                        # 在Output窗口显示原始响应
                        self.output_text.insert(tk.END, result.stdout, "blue")
                        self.root.update()
                        
                        # 解析流式响应，提取answer值
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
        
        # 在Processed窗口显示结果
        if processed_answer:
            self.processed_text.delete(1.0, tk.END)
            self.processed_text.insert(1.0, processed_answer)
    
    def process_chat_stream_response(self, response_text):
        """处理对话流的流式响应，提取所有信息的output字段并显示在Processed窗口"""
        # 按行分割响应
        lines = response_text.strip().split('\n')
        output_parts = []
        
        # 解析每一行
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 处理data:开头的JSON格式
            if line.startswith('data:'):
                try:
                    # 提取JSON部分（去掉'data:'前缀）
                    json_str = line[5:].strip()
                    if not json_str:
                        continue
                    data = json.loads(json_str)
                    
                    # 提取output字段
                    if 'data' in data and isinstance(data['data'], dict):
                        data_content = data['data']
                        if 'content' in data_content and isinstance(data_content['content'], dict):
                            content = data_content['content']
                            
                            # 优先从outputs数组中提取
                            if 'outputs' in content and isinstance(content['outputs'], list):
                                for output_item in content['outputs']:
                                    if isinstance(output_item, dict) and 'output' in output_item:
                                        output = output_item.get('output', '')
                                        if output:  # 只添加非空output
                                            output_parts.append(output)
                            # 备用：直接从content的output字段提取
                            elif 'output' in content:
                                output = content.get('output', '')
                                if output:  # 只添加非空output
                                    output_parts.append(output)
                            
                except json.JSONDecodeError as e:
                    # 在Output窗口显示解析错误，便于调试
                    self.output_text.insert(tk.END, f"\nJSON解析错误: {line}\n", "blue")
                    continue
            # 处理纯JSON格式（不以data:开头）
            elif line.startswith('{') and line.endswith('}'):
                try:
                    data = json.loads(line)
                    
                    # 提取output字段
                    if 'data' in data and isinstance(data['data'], dict):
                        data_content = data['data']
                        if 'content' in data_content and isinstance(data_content['content'], dict):
                            content = data_content['content']
                            
                            # 优先从outputs数组中提取
                            if 'outputs' in content and isinstance(content['outputs'], list):
                                for output_item in content['outputs']:
                                    if isinstance(output_item, dict) and 'output' in output_item:
                                        output = output_item.get('output', '')
                                        if output:  # 只添加非空output
                                            output_parts.append(output)
                            # 备用：直接从content的output字段提取
                            elif 'output' in content:
                                output = content.get('output', '')
                                if output:  # 只添加非空output
                                    output_parts.append(output)
                            
                except json.JSONDecodeError as e:
                    # 在Output窗口显示解析错误，便于调试
                    self.output_text.insert(tk.END, f"\nJSON解析错误: {line}\n", "blue")
                    continue
        
        # 在Output窗口显示提取到的output数量，便于调试
        self.output_text.insert(tk.END, f"\n\n=== 调试信息 ===\n", "blue")
        self.output_text.insert(tk.END, f"提取到 {len(output_parts)} 个output内容\n", "blue")
        for i, part in enumerate(output_parts):
            self.output_text.insert(tk.END, f"Output {i+1}: '{part}'\n", "blue")
        
        # 抛弃最后一个output值，拼接剩余的output
        if len(output_parts) > 1:
            processed_answer = ''.join(output_parts[:-1])  # 去掉最后一个
        elif len(output_parts) == 1:
            processed_answer = output_parts[0]  # 如果只有一个，就使用它
        else:
            processed_answer = ""  # 没有提取到内容
        
        # 在Output窗口显示最终结果，便于调试
        self.output_text.insert(tk.END, f"\n最终Processed结果: '{processed_answer}'\n", "blue")
        
        # 在Processed窗口显示结果
        self.processed_text.delete(1.0, tk.END)
        if processed_answer:
            self.processed_text.insert(1.0, processed_answer)
        else:
            self.processed_text.insert(1.0, "未提取到有效内容")
    



def main():
    root = tk.Tk()
    app = LanmaAPIDemo(root)
    root.mainloop()

if __name__ == "__main__":
    main()