import base64

def base64_encode(text:str) -> str:
    
    bytes_data = text.encode('utf-8')
    base64_bytes = base64.b64encode(bytes_data)
    base64_str = base64_bytes.decode('utf-8')

    return base64_str

def base64_decode(base64_str:str) -> str:

    decoded_bytes = base64.b64decode(base64_str)
    decoded_text = decoded_bytes.decode('utf-8')

    return decoded_text

if __name__ == "__main__":
    text = "你好，世界！"
    a = base64_encode(text)
    print(type(base64_encode(text)),base64_encode(text))
    print(type(base64_decode(a)),base64_decode(a))