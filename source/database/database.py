import os
import sqlite3

from DB_settings import SERVER_DB_PATH,CLIENT_DB_PATH

def init_server_database():
    '''初始化服务器数据库'''

    if not os.path.exists(SERVER_DB_PATH):

        # 文件不存在 → 创建并初始化
        conn = sqlite3.connect(SERVER_DB_PATH)

        # 创建数据库
        cursor = conn.cursor()
        cursor.execute(
                'CREATE TABLE users (               ' \
                '   id INTEGER PRIMARY KEY,         ' \
                '   username CHAR(20) UNIQUE,       ' \
                '   ip CHAR(15),                    ' \
                '   port CHAR(5),                   ' \
                '   is_active BOOL DEFAULT false    ' \
                ')                                  '
            )
        
        conn.commit()
        conn.close()

    else:
        pass

def init_client_database():
    '''初始化用户数据库'''

    if not os.path.exists(CLIENT_DB_PATH):

        # 文件不存在 → 创建并初始化
        conn = sqlite3.connect(CLIENT_DB_PATH)

        # 创建数据库
        cursor = conn.cursor()
        cursor.execute(
                'CREATE TABLE friends (             ' \
                '   id INTEGER PRIMARY KEY,         ' \
                '   username CHAR(20) UNIQUE        ' \
                ')                                  ' 
            )
        cursor.execute(
                'CREATE TABLE chat_template (       ' \
                '   id INTEGER PRIMARY KEY,         ' \
                '   username CHAR(20) UNIQUE,       ' \
                '   context VARCHAR(20) NOT NULL    ' \
                ')                                  ' 
            )
        
        conn.commit()
        conn.close()
        
    else:
        pass

if __name__ == "__main__":
    init_server_database()
    init_client_database()