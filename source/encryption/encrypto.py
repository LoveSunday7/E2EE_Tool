import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.backends import default_backend
from .encoding import *   # 保留原有的 base64_encode 等函数

def aes_encrypt_bytes(plaintext: bytes, key: bytes) -> bytes:
    """
    AES 加密，直接返回二进制密文（IV + 密文）

    :param plaintext: 明文字节串
    :param key: 密钥（16/24/32 字节，若长度不符需自行填充）
    :return: 加密结果（IV(16字节) + 密文），bytes 类型
    """
    iv = os.urandom(16)
    # 使用传入的 key，不再硬编码
    # 注意：如果 key 长度不是 16/24/32，需要提前处理（例如使用 key_pad 函数）
    # 这里假设 key 长度正确，或调用方已确保
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def aes_decrypt_bytes(encrypted_data: bytes, key: bytes) -> bytes:
    """
    AES 解密，直接处理二进制密文（IV + 密文）

    :param encrypted_data: 加密结果（IV(16字节) + 密文）
    :param key: 密钥（必须与加密时相同）
    :return: 明文字节串
    """
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext

def string_to_sha256(text: str) -> str:
    """
    对字符串先进行 base64 编码，再计算 SHA-256 哈希

    :param text: 原字符串
    :return: 加密后的十六进制字符串
    """
    # 假设 base64_encode 函数来自 .encoding 模块，返回 bytes
    base64_bytes = base64_encode(text)   # 保持原有逻辑
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(base64_bytes)
    hash_hex = digest.finalize().hex()
    return hash_hex

if __name__ == "__main__":
    # 测试：使用一个正确的密钥（16字节）
    key = b'1234567890123456'   # 16字节 AES-128
    plain = b"deaedcaeda"
    encrypted = aes_encrypt_bytes(plain, key)
    print("密文:", encrypted.hex())
    decrypted = aes_decrypt_bytes(encrypted, key)
    print("解密:", decrypted)

    print(string_to_sha256("你好"))