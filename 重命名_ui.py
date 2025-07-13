import os
import configparser
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, 
    QFileDialog, QHBoxLayout, QMessageBox, QComboBox, QListWidget, QCheckBox
)
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QPalette, QColor
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
    CONFIG_FILE = os.path.join(os.path.dirname(__file__), "rename_config.ini")

    def __init__(self):
        super().__init__()
        self.selected_files = []  # 初始化文件列表
        self._initialized = False  # 添加初始化标志
        self.init_ui()
        self.load_settings()
        self._initialized = True  # 初始化完成

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

        # 添加“是否删除原文件”复选框
        self.delete_original_checkbox = QCheckBox("重命名后删除原文件")
        layout.addWidget(self.delete_original_checkbox)

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
        self.delete_original_checkbox.stateChanged.connect(self.on_delete_checkbox_changed)

        # 在输入框内容变化时调用
        self.src_ext_input.textChanged.connect(self.update_style)
        self.target_ext_input.textChanged.connect(self.update_style)
        # 初始化时也调用一次
        self.update_style()

    def load_settings(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.CONFIG_FILE):
            config.read(self.CONFIG_FILE, encoding="utf-8")
            # 恢复复选框状态
            delete_original = config.getboolean("main", "delete_original", fallback=False)
            self.delete_original_checkbox.setChecked(delete_original)
            # 恢复输出文件夹
            output_folder = config.get("main", "output_folder", fallback="")
            self.output_folder_input.setText(output_folder)
            # 恢复上次源文件夹
            last_source_folder = config.get("main", "last_source_folder", fallback="")
            self.last_source_folder = last_source_folder
            if last_source_folder:
                self.file_input.setText(f"上次源文件夹: {last_source_folder}")
        else:
            self.delete_original_checkbox.setChecked(False)
            self.output_folder_input.setText("")
            self.last_source_folder = ""

        # 恢复自定义源文件后缀
        self.src_ext_input.setText(config.get("main", "src_ext_input", fallback=""))
        # 恢复自定义目标后缀
        self.target_ext_input.setText(config.get("main", "target_ext_input", fallback=""))

    def save_settings(self):
        config = configparser.ConfigParser()
        config["main"] = {
            "delete_original": str(self.delete_original_checkbox.isChecked()),
            "output_folder": self.output_folder_input.text(),
            "last_source_folder": getattr(self, "last_source_folder", ""),
            "src_ext_input": self.src_ext_input.text(),
            "target_ext_input": self.target_ext_input.text(),
        }
        with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
            config.write(f)

    def showEvent(self, event):
        self.load_settings()
        super().showEvent(event)

    def hideEvent(self, event):
        self.save_settings()
        super().hideEvent(event)

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
        # 使用上次的源文件夹作为默认打开路径
        start_dir = getattr(self, "last_source_folder", "")
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            '选择要重命名的文件', 
            start_dir, 
            '所有文件 (*.*)'
        )
        if files:
            self.file_input.setText(f"已选择 {len(files)} 个文件: {files[0]}...")
            self.selected_files = files
            # 保存当前源文件夹
            self.last_source_folder = os.path.dirname(files[0])
            # 设置默认输出文件夹为第一个文件所在文件夹
            default_output_folder = os.path.dirname(files[0])
    def on_delete_checkbox_changed(self, state):
        if not getattr(self, '_initialized', False):
            return
        if state == 2:  # 勾选
            reply = QMessageBox.question(
                self, "确认删除", "确定要在重命名后删除原文件吗？此操作不可恢复！",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                self.delete_original_checkbox.setChecked(False)
            if reply != QMessageBox.Yes:
                self.delete_original_checkbox.setChecked(False)

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

            # 获取删除原文件的选项
            delete_original = self.delete_original_checkbox.isChecked()

            # 执行重命名
            success_files, failed_files = batch_rename_files(
                self.selected_files, src_exts, target_ext, output_folder, delete_original
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
            
            self.save_settings()  # 操作后也保存一次
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'发生错误：{str(e)}')

    def update_style(self):
        # 判断自定义源后缀
        if self.src_ext_input.text().strip():
            # 输入框高亮
            self.src_ext_input.setStyleSheet("color: black; background: #fffbe6;")
            # 列表灰色
            self.src_ext_list.setStyleSheet("color: gray;")
        else:
            # 输入框灰色
            self.src_ext_input.setStyleSheet("color: gray; background: #f0f0f0;")
            # 列表高亮
            self.src_ext_list.setStyleSheet("color: black;")

        # 判断自定义目标后缀
        if self.target_ext_input.text().strip():
            self.target_ext_input.setStyleSheet("color: black; background: #fffbe6;")
            self.target_ext_combo.setStyleSheet("color: gray;")
        else:
            self.target_ext_input.setStyleSheet("color: gray; background: #f0f0f0;")
            self.target_ext_combo.setStyleSheet("color: black;")
