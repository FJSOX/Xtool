import os
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, 
    QFileDialog, QHBoxLayout, QMessageBox, QComboBox, QListWidget
)
from 重命名 import batch_rename_files

# 定义常用文件格式
COMMON_EXTENSIONS = [
    '.txt', '.md', '.doc', '.docx', '.pdf',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp',
    '.mp3', '.mp4', '.avi', '.mov', '.wav',
    '.zip', '.rar', '.7z',
    '.py', '.java', '.cpp', '.cs',
    '.html', '.css', '.js', '.json',
    '.csv', '.xlsx', '.xls',
    '.lrc', '.srt',
    '_utf-8.txt', '_gbk.txt'  # 添加常见的编码后缀
]

class RenameToolUI(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_files = []  # 初始化文件列表
        self.init_ui()

    def init_ui(self):
        # 创建布局
        layout = QVBoxLayout()

        # 添加关闭按钮
        close_layout = QHBoxLayout()
        self.back_button = QPushButton('关闭')
        self.back_button.setMaximumWidth(100)
        close_layout.addStretch()
        close_layout.addWidget(self.back_button)
        layout.addLayout(close_layout)

        # 创建控件
        label = QLabel('欢迎使用文件重命名工具！')
        layout.addWidget(label)

        # 文件选择部分
        file_label = QLabel('选择要重命名的文件(支持多选):')
        self.file_input = QLineEdit()
        file_button = QPushButton('浏览...')
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(file_button)
        layout.addWidget(file_label)
        layout.addLayout(file_layout)

        # 源文件后缀选择部分
        src_ext_label = QLabel('选择源文件后缀(支持多选):')
        layout.addWidget(src_ext_label)
        
        # 创建源文件后缀列表
        self.src_ext_list = QListWidget()
        self.src_ext_list.addItems(COMMON_EXTENSIONS)
        self.src_ext_list.setSelectionMode(QListWidget.MultiSelection)
        self.src_ext_list.setMaximumHeight(150)  # 设置最大高度
        layout.addWidget(self.src_ext_list)
        
        # 自定义源文件后缀输入
        src_custom_label = QLabel('自定义源文件后缀(用空格分隔，如: .rar.txt _utf-8.txt):')
        self.src_ext_input = QLineEdit()
        self.src_ext_input.setPlaceholderText('例如: .rar.txt _utf-8.txt')
        layout.addWidget(src_custom_label)
        layout.addWidget(self.src_ext_input)

        # 目标文件后缀选择
        target_ext_label = QLabel('目标文件后缀:')
        target_ext_layout = QHBoxLayout()
        
        # 目标后缀下拉列表
        self.target_ext_combo = QComboBox()
        self.target_ext_combo.addItems(COMMON_EXTENSIONS)
        
        # 自定义目标后缀输入
        self.target_ext_input = QLineEdit()
        self.target_ext_input.setPlaceholderText('自定义后缀(如 .xyz)')
        
        target_ext_layout.addWidget(self.target_ext_combo)
        target_ext_layout.addWidget(self.target_ext_input)
        layout.addWidget(target_ext_label)
        layout.addLayout(target_ext_layout)

        # 添加输出文件夹选择
        output_folder_label = QLabel('选择目标文件夹(默认为源文件夹):')
        self.output_folder_input = QLineEdit()
        output_folder_button = QPushButton('浏览...')
        output_folder_layout = QHBoxLayout()
        output_folder_layout.addWidget(self.output_folder_input)
        output_folder_layout.addWidget(output_folder_button)
        layout.addWidget(output_folder_label)
        layout.addLayout(output_folder_layout)

        # 重命名按钮
        rename_button = QPushButton('开始重命名')
        layout.addWidget(rename_button)

        # 结果显示
        self.result_label = QLabel('')
        layout.addWidget(self.result_label)

        # 设置窗口布局
        self.setLayout(layout)

        # 绑定按钮事件
        file_button.clicked.connect(self.select_files)
        rename_button.clicked.connect(self.start_rename)
        output_folder_button.clicked.connect(self.select_output_folder)

    def get_selected_extensions(self):
        """获取所有选中的源文件后缀"""
        # 获取列表中选中的后缀
        selected_exts = [item.text() for item in self.src_ext_list.selectedItems()]
        
        # 获取自定义输入的后缀
        custom_exts = self.src_ext_input.text().strip()
        if custom_exts:
            # 直接分割自定义后缀，不做点号处理
            custom_exts = custom_exts.split()
            selected_exts.extend(custom_exts)
        
        return selected_exts

    def get_target_extension(self):
        """获取目标文件后缀"""
        # 优先使用自定义输入的后缀
        custom_ext = self.target_ext_input.text().strip()
        if custom_ext:
            return custom_ext if custom_ext.startswith('.') else f'.{custom_ext}'
        return self.target_ext_combo.currentText()

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择目标文件夹')
        if folder_path:
            self.output_folder_input.setText(folder_path)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            '选择要重命名的文件', 
            '', 
            '所有文件 (*.*)'
        )
        if files:
            self.file_input.setText(f"已选择 {len(files)} 个文件: {files[0]}...")
            self.selected_files = files
            # 设置默认输出文件夹为第一个文件所在文件夹
            default_output_folder = os.path.dirname(files[0])
            self.output_folder_input.setText(default_output_folder)

    def start_rename(self):
        try:
            # 检查是否有选择文件
            if not hasattr(self, 'selected_files') or not self.selected_files:
                QMessageBox.warning(self, '错误', '请选择要重命名的文件！')
                return

            # 获取源文件后缀列表
            src_exts = self.get_selected_extensions()
            if not src_exts:
                QMessageBox.warning(self, '错误', '请选择或输入源文件后缀！')
                return

            # 获取目标后缀
            target_ext = self.get_target_extension()
            if not target_ext:
                QMessageBox.warning(self, '错误', '请选择或输入目标文件后缀！')
                return

            # 获取输出文件夹
            output_folder = self.output_folder_input.text()
            if not output_folder:
                # 使用源文件所在文件夹
                output_folder = os.path.dirname(self.selected_files[0])
            elif not os.path.isdir(output_folder):
                QMessageBox.warning(self, '错误', '目标文件夹不存在！')
                return

            # 执行重命名
            success_files, failed_files = batch_rename_files(
                self.selected_files, src_exts, target_ext, output_folder
            )

            # 显示结果
            result_message = f"重命名完成！\n成功：{len(success_files)}/{len(self.selected_files)} 个文件"
            if success_files:
                result_message += "\n\n成功重命名的文件："
                for old_path, new_path in success_files:
                    result_message += f"\n{os.path.basename(old_path)} -> {os.path.basename(new_path)}"
            
            if failed_files:
                result_message += "\n\n失败的文件："
                for file_path, error in failed_files:
                    result_message += f"\n{os.path.basename(file_path)}: {error}"

            self.result_label.setText(result_message)
            QMessageBox.information(self, '重命名结果', result_message)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'发生错误：{str(e)}')
