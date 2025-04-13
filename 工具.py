import chardet
print(chardet.__version__)

# 动态获取支持的编码格式
try:
    supported_encodings = chardet.universaldetector.UniversalDetector.SUPPORTED_ENCODINGS
    print("chardet 支持的编码格式:")
    for encoding in supported_encodings:
        print(encoding)
except AttributeError:
    print("当前版本的 chardet 不支持 SUPPORTED_ENCODINGS 属性，请手动定义编码格式列表。")