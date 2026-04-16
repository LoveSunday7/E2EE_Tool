import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding, serialization
from cryptography.hazmat.primitives.asymmetric import dh, rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


from .encoding import * 

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

def generate_rsa_key_pair(key_size: int = 2048) -> bytes:
    """
    生成 RSA 密钥对，返回 (私钥PEM字节串, 公钥PEM字节串)

    :param key_size: 密钥长度，推荐 2048 或 3072
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_pem, public_pem

def rsa_encrypt_bytes(plaintext: bytes, public_key_pem: bytes) -> bytes:
    """
    使用 RSA 公钥加密短数据（OAEP 填充，SHA-256）

    :param plaintext: 明文字节串（长度受密钥限制，例如 2048 位密钥最多加密 190 字节）
    :param public_key_pem: 公钥 PEM 格式字节串
    :return: 密文字节串
    """
    public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def rsa_decrypt_bytes(ciphertext: bytes, private_key_pem: bytes) -> bytes:
    """
    使用 RSA 私钥解密数据

    :param ciphertext: 密文字节串
    :param private_key_pem: 私钥 PEM 格式字节串
    :return: 明文字节串
    """
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None,
        backend=default_backend()
    )
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext

if __name__ == "__main__":
    pass