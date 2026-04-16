from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from os import urandom
from encoding import *

def aes_encrypt_bytes(plaintext: bytes, key: bytes) -> bytes:
    """
    AES 加密，直接返回二进制密文（IV + 密文）

    :param plaintext: 明文字节串
    :param key: 密钥（16/24/32 字节）
    :return: 加密结果（IV(16字节) + 密文），bytes 类型
    """
    iv = urandom(16)
    key = key_pad(b"niuwerqewew")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return iv+ciphertext

def aes_decrypt_bytes(encrypted_data: bytes, key: bytes) -> bytes:
    """
    AES 解密，直接处理二进制密文（IV + 密文）

    :param encrypted_data: 加密结果（IV(16字节) + 密文）
    :param key: 密钥（必须与加密时相同）
    :return: 明文字节串
    """
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    key = key_pad(b"niuwerqewew")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted_padded, AES.block_size)
    return plaintext

if __name__ == "__main__":
    C = aes_encrypt_bytes(b"deaedcaeda", b"niuwerqewew")
    print(C)
    M = aes_decrypt_bytes(C,b"niuwerqewew")
    print(M)
