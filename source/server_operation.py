import sqlite3
from database.DB_settings import SERVER_DB_PATH
from encryption.encrypto  import string_to_sha256

def add_user(username):
    '''
    """
    服务器添加用户函数,

    :param username: 用户原始输入的用户名
    :return: 返回一个bool数，插入成功返回True,插入失败返回False
    '''

    # 对用户输入的用户名进行hash，防止sql注入
    username = string_to_sha256(username)

    try:
        # 插入用户名
        conn = sqlite3.connect(SERVER_DB_PATH)
        conn.execute(f"INSERT INTO users (username) VALUES (\"{username}\")")
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        # 插入失败
        return False


if __name__ == "__main__":
    print(add_user("LoveSuday"))
