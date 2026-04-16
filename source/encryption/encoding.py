import base64

def base64_encode(text: str) -> bytes:
    """
    Base64 编码

    :param text: 原始字符串（UTF-8）
    :return: Base64 编码后的字节串（bytes 类型）
    """
    bytes_data = text.encode('utf-8')
    base64_bytes = base64.b64encode(bytes_data)
    return base64_bytes

def base64_decode(base64_bytes: bytes) -> str:
    """
    Base64 解码

    :param base64_bytes: Base64 编码的字节串
    :return: 解码后的原始字符串（UTF-8）
    """
    decoded_bytes = base64.b64decode(base64_bytes)
    decoded_text = decoded_bytes.decode('utf-8')
    return decoded_text

def key_pad(key: bytes) -> bytes:
    """
    将任意长度的密钥填充/截断到 AES 支持的密钥长度（16、24 或 32 字节）

    规则：
    - 如果 len(key) < 16：在末尾补 b'\x00' 直到长度为 16
    - 如果 16 <= len(key) < 24：补零到 24 字节
    - 如果 24 <= len(key) < 32：补零到 32 字节
    - 如果 len(key) >= 32：截断前 32 字节

    :param key: 原始密钥字节串
    :return: 长度恰好为 16、24 或 32 字节的密钥
    """
    if len(key) < 16:
        return key + b'\x00' * (16 - len(key))
    elif len(key) < 24:
        return key + b'\x00' * (24 - len(key))
    elif len(key) < 32:
        return key + b'\x00' * (32 - len(key))
    else:
        return key[:32]

if __name__ == "__main__":
    text = "asdiaosfjsa"

    print(base64_encode(text))
    print(base64_decode(base64_encode(text)))