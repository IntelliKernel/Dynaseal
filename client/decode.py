import json
import base64

# 解码eyJhcGkta2V5IjoiNjcxMjIzYzVjYTYzZjNkNWY1Mjc1NjM2IiwibW9kZWwiOiJkZWVwc2Vlay1jaGF0IiwibWF4X3Rva2VuIjoxMDAsImV4cGlyaW5nIjoxNzI5MjQ4Nzk2Ljg0NjQ4NjZ9


def decode_base64url(data):
    """将 Base64URL 解码成正常的字符串"""
    # Base64URL 是 Base64 的一种变种，"-" 替换为 "+", "_" 替换为 "/"
    data = data.replace("-", "+").replace("_", "/")
    # 修正可能缺少的 padding
    missing_padding = len(data) % 4
    if missing_padding:
        data += "=" * (4 - missing_padding)
    return base64.b64decode(data)


to_decoded = "eyJhcGkta2V5IjoiNjcxMjQ5YTkzZjFjZjJmOGJmOWIyYjgyIiwibW9kZWwiOiJkZWVwc2Vlay1jaGF0IiwibWF4X3Rva2VuIjoxMDAsImV4cGlyaW5nIjoxNzI5MjUzNTQwLjk4NDYwNTYsImV2ZW50X2lkIjoiODMyYThmZDEtNWFhNi00MzY2LWFiZjEtMmE1YjA4M2IyY2Y4In0"
print(len(to_decoded))
# base64解码
data = decode_base64url(to_decoded)

# json格式化
data = json.loads(data)
print(data)
