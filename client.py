#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

def main():
    # 创建 TCP 套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 连接服务器
    host = '192.168.56.1'
    port = 12345
    try:
        client_socket.connect((host, port))
        print(f"已连接到服务器 {host}:{port}")
    except ConnectionRefusedError:
        print("连接失败，请确保服务器已启动")
        return

    try:
        while True:
            # 从键盘输入消息
            message = input("请输入要发送的消息 (输入 'quit' 退出): ")
            if message.lower() == 'quit':
                break
            
            # 发送消息（编码为字节）
            client_socket.sendall(message.encode('utf-8'))
            
            # 接收服务器回显的数据
            data = client_socket.recv(1024)
            if not data:
                print("服务器已关闭连接")
                break
            print(f"服务器回显: {data.decode('utf-8')}")
    except (ConnectionResetError, BrokenPipeError):
        print("服务器连接已断开")
    finally:
        client_socket.close()
        print("客户端退出")

if __name__ == "__main__":
    main()