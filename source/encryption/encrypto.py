from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
from os import urandom
from .encoding import *

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

def string_to_sha256(text:str) -> str:
    """
    sha64 加密小块数据

    :param text:原字符串
    :return: 加密后的字符串
    """
    base64_bytes = base64_encode(text)
    hash_obj = SHA256.new()
    hash_obj.update(base64_bytes)
    hash_hex = hash_obj.hexdigest()

    return hash_hex

if __name__ == "__main__":
    # C = aes_encrypt_bytes(b"deaedcaeda", b"niuwerqewew")
    # print(C)
    # M = aes_decrypt_bytes(C,b"niuwerqewew")
    # print(M)

    print(string_to_sha256("你好"))
