#!/usr/bin/env python3
import os
import argparse
import chardet

def detect_encoding(file_path):
    """
    自动检测文件编码格式，返回编码名称和置信度
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    encoding = result.get('encoding')
    confidence = result.get('confidence')
    return encoding, confidence

def convert_file(file_path, src_encoding, target_encoding):
    """
    读取原文件内容，并转换为目标编码，生成新文件，新文件名在原文件名后加上源编码后缀
    """
    # 获取路径和文件名信息
    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    # 构造新文件名
    new_filename = f"{name}_{target_encoding}{ext}"
    new_file_path = os.path.join(dir_name, new_filename)

    # 读取内容并写入新文件
    with open(file_path, 'r', encoding=src_encoding, errors='replace') as f:
        content = f.read()
    with open(new_file_path, 'w', encoding=target_encoding) as f:
        f.write(content)

    print(f"转换成功！\n原编码：{src_encoding}\n目标编码：{target_encoding}\n新文件：{new_file_path}")

def main():
    parser = argparse.ArgumentParser(description="自动识别并转换TXT文件编码格式")
    parser.add_argument("file", help="TXT 文件路径")
    parser.add_argument("-s", "--src", help="手动指定原文件编码格式，如果不指定则自动检测")
    parser.add_argument("-t", "--target", default="utf-8", help="目标编码格式，默认为 utf-8")
    args = parser.parse_args()

    file_path = args.file
    target_encoding = args.target

    # 检查文件是否存在
    if not os.path.isfile(file_path):
        print(f"错误：文件 {file_path} 不存在！")
        return

    # 获取源编码
    if args.src:
        src_encoding = args.src
        print(f"手动指定原编码格式为：{src_encoding}")
    else:
        src_encoding, confidence = detect_encoding(file_path)
        if not src_encoding:
            print("无法检测文件编码，请尝试手动指定。")
            return
        print(f"自动检测到的原编码格式为：{src_encoding}，置信度：{confidence:.2f}")

    # 转换文件编码
    convert_file(file_path, src_encoding, target_encoding)

if __name__ == "__main__":
    main()
