#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

def main():
    # 创建 TCP 套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 设置地址重用，避免重启时端口被占用
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 绑定到本地地址和端口
    host = '127.0.0.1'
    port = 12345
    server_socket.bind((host, port))
    
    # 开始监听，最大等待连接数为5
    server_socket.listen(5)
    print(f"服务器启动，监听 {host}:{port}")
    
    while True:
        # 接受客户端连接
        client_socket, client_addr = server_socket.accept()
        print(f"接受连接来自 {client_addr}")
        
        # 处理客户端请求（简单回显）
        try:
            while True:
                # 接收数据，最大1024字节
                data = client_socket.recv(1024)
                if not data:
                    break  # 客户端关闭连接
                print(f"收到数据: {data.decode('utf-8')}")
                # 将数据原样发送回去
                client_socket.sendall(data)
        except (ConnectionResetError, BrokenPipeError):
            print(f"客户端 {client_addr} 异常断开")
        finally:
            client_socket.close()
            print(f"连接 {client_addr} 已关闭")

if __name__ == "__main__":
    main()