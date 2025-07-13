import os

def batch_rename_files(file_paths, src_exts, target_ext, output_folder=None, delete_original=False):
    """
    批量重命名文件后缀
    :param file_paths: 文件路径列表
    :param src_exts: 源文件后缀列表 (如 ['txt', '_utf-8.txt'])
    :param target_ext: 目标文件后缀 (如 '.txt')
    :param output_folder: 输出文件夹路径
    :return: (成功列表, 失败列表)
    """
    success_files = []
    failed_files = []
    
    # 只处理目标后缀的点号
    target_ext = target_ext if target_ext.startswith('.') else f'.{target_ext}'
    
    for file_path in file_paths:
        try:
            # 检查文件是否存在
            if not os.path.isfile(file_path):
                failed_files.append((file_path, "文件不存在"))
                continue
                
            # 获取文件名
            file_dir = output_folder if output_folder else os.path.dirname(file_path)
            file_name = os.path.basename(file_path)
            
            # 检查文件名是否以任一源后缀结尾（不区分大小写）
            matched_ext = None
            for ext in sorted(src_exts, key=len, reverse=True):  # 按长度降序排序，优先匹配最长的后缀
                # 处理后缀中的点号
                check_ext = ext[1:] if ext.startswith('.') else ext
                if file_name.lower().endswith(check_ext.lower()):
                    matched_ext = check_ext
                    break
            
            # 如果没有匹配的后缀，跳过该文件
            if not matched_ext:
                continue
                
            # 获取基本文件名（不含匹配的后缀）
            base_name = file_name[:-len(matched_ext)]
            # 如果基本文件名以点结尾且目标后缀以点开始，去掉一个点
            if base_name.endswith('.') and target_ext.startswith('.'):
                base_name = base_name[:-1]
                
            # 构造新文件名
            new_file_name = f"{base_name}{target_ext}"
            new_file_path = os.path.join(file_dir, new_file_name)
            
            # 检查目标文件是否已存在
            if os.path.exists(new_file_path):
                counter = 1
                while os.path.exists(new_file_path):
                    new_file_name = f"{base_name}_{counter}{target_ext}"
                    new_file_path = os.path.join(file_dir, new_file_name)
                    counter += 1
            
            # 复制文件内容并创建新文件
            with open(file_path, 'rb') as src_file:
                with open(new_file_path, 'wb') as dst_file:
                    dst_file.write(src_file.read())
            if delete_original:
                try:
                    os.remove(file_path)
                except Exception as e:
                    failed_files.append((file_path, f"删除原文件失败: {str(e)}"))
            
            success_files.append((file_path, new_file_path))
            
        except Exception as e:
            failed_files.append((file_path, str(e)))
    
    return success_files, failed_files
