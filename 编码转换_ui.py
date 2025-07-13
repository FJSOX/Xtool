# 导入必要的模块
import os
import configparser
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QFileDialog, QHBoxLayout, QMessageBox, QComboBox, QCheckBox
)
from PyQt5.QtGui import QColor
from 编码转换 import detect_encoding, convert_file  # 引入编码转换模块

# 配置文件路径（与重命名 UI 共用）
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "tool_config.ini")

# 定义常用编码格式列表
SUPPORTED_ENCODINGS = [
    'utf-8',
    'gbk',
    'gb2312',
    'big5',
    'ascii',
    'latin1',
    'utf-16',
    'utf-32',
    'euc-jp',
    'shift-jis',
    'iso-8859-1'
]

class EncodingConverterUI(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        # 创建布局
        layout = QVBoxLayout()

        # 添加关闭按钮并调整样式
        close_layout = QHBoxLayout()
        self.back_button = QPushButton('关闭')
        self.back_button.setMaximumWidth(100)  # 设置按钮宽度
        close_layout.addStretch()  # 添加弹性空间将按钮推到右侧
        close_layout.addWidget(self.back_button)
        layout.addLayout(close_layout)

        # 创建控件
        label = QLabel('欢迎使用编码转换工具！')
        layout.addWidget(label)

        # 修改文件选择部分
        file_label = QLabel('选择源文件(支持多选):')
        self.file_input = QLineEdit()
        file_button = QPushButton('浏览...')
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(file_button)
        layout.addLayout(file_layout)

        # 源编码选择
        src_encoding_label = QLabel('源文件编码:')
        src_encoding_layout = QHBoxLayout()
        self.src_encoding_combo = QComboBox()
        self.src_encoding_combo.addItem('自动检测')  # 默认选项
        self.src_encoding_combo.addItems(SUPPORTED_ENCODINGS)
        self.src_encoding_input = QLineEdit()  # 新增：手动输入框
        self.src_encoding_input.setPlaceholderText('自定义编码格式')
        src_encoding_layout.addWidget(self.src_encoding_combo)
        src_encoding_layout.addWidget(self.src_encoding_input)
        layout.addWidget(src_encoding_label)
        layout.addLayout(src_encoding_layout)

        # 目标编码选择
        target_encoding_label = QLabel('目标文件编码:')
        target_encoding_layout = QHBoxLayout()
        self.target_encoding_combo = QComboBox()
        self.target_encoding_combo.addItems(SUPPORTED_ENCODINGS)
        self.target_encoding_combo.setCurrentText('utf-8')  # 设置默认值
        self.target_encoding_input = QLineEdit()  # 新增：手动输入框
        self.target_encoding_input.setPlaceholderText('自定义编码格式')
        target_encoding_layout.addWidget(self.target_encoding_combo)
        target_encoding_layout.addWidget(self.target_encoding_input)
        layout.addWidget(target_encoding_label)
        layout.addLayout(target_encoding_layout)

        # 目标文件夹选择
        output_folder_label = QLabel('选择目标文件夹(默认为源文件夹):')
        self.output_folder_input = QLineEdit()
        output_folder_button = QPushButton('浏览...')
        output_folder_layout = QHBoxLayout()
        output_folder_layout.addWidget(self.output_folder_input)
        output_folder_layout.addWidget(output_folder_button)
        layout.addLayout(output_folder_layout)

        # 添加“删除源文件”复选框
        self.delete_original_checkbox = QCheckBox("转换后删除原文件")
        layout.addWidget(self.delete_original_checkbox)

        # 转换按钮
        convert_button = QPushButton('开始转换')
        layout.addWidget(convert_button)

        # 结果显示
        self.result_label = QLabel('')
        layout.addWidget(self.result_label)

        # 设置窗口布局
        self.setLayout(layout)

        # 绑定按钮事件
        file_button.clicked.connect(self.select_file)
        output_folder_button.clicked.connect(self.select_output_folder)
        convert_button.clicked.connect(self.start_conversion)
        self.src_encoding_input.textChanged.connect(self.update_style)
        self.target_encoding_input.textChanged.connect(self.update_style)
        self.delete_original_checkbox.stateChanged.connect(self.on_delete_checkbox_changed)
        self.update_style()

    def on_delete_checkbox_changed(self, state):
        if state == 2:  # 勾选
            reply = QMessageBox.question(
                self, "确认删除", "确定要在转换后删除原文件吗？此操作不可恢复！",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                self.delete_original_checkbox.setChecked(False)

    def load_settings(self):
        config = configparser.ConfigParser()
        # 断开信号，防止加载时弹窗
        try:
            self.delete_original_checkbox.stateChanged.disconnect(self.on_delete_checkbox_changed)
        except Exception:
            pass
        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE, encoding="utf-8")
            # 恢复输出文件夹
            output_folder = config.get("encoding", "output_folder", fallback="")
            self.output_folder_input.setText(output_folder)
            # 恢复自定义源编码
            self.src_encoding_input.setText(config.get("encoding", "src_encoding_input", fallback=""))
            # 恢复自定义目标编码
            self.target_encoding_input.setText(config.get("encoding", "target_encoding_input", fallback=""))
            # 恢复下拉选项
            self.src_encoding_combo.setCurrentText(config.get("encoding", "src_encoding_combo", fallback="自动检测"))
            self.target_encoding_combo.setCurrentText(config.get("encoding", "target_encoding_combo", fallback="utf-8"))
            # 恢复上次源文件夹
            last_source_folder = config.get("encoding", "last_source_folder", fallback="")
            self.last_source_folder = last_source_folder
            if last_source_folder:
                self.file_input.setText(f"上次源文件夹: {last_source_folder}")
            # 恢复删除源文件复选框
            delete_original = config.getboolean("encoding", "delete_original", fallback=False)
            self.delete_original_checkbox.setChecked(delete_original)
        else:
            self.output_folder_input.setText("")
            self.src_encoding_input.setText("")
            self.target_encoding_input.setText("")
            self.src_encoding_combo.setCurrentText("自动检测")
            self.target_encoding_combo.setCurrentText("utf-8")
            self.last_source_folder = ""
            self.delete_original_checkbox.setChecked(False)
        # 恢复信号连接
        self.delete_original_checkbox.stateChanged.connect(self.on_delete_checkbox_changed)

    def save_settings(self):
        config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            config.read(CONFIG_FILE, encoding="utf-8")
        config["encoding"] = {
            "output_folder": self.output_folder_input.text(),
            "src_encoding_input": self.src_encoding_input.text(),
            "target_encoding_input": self.target_encoding_input.text(),
            "src_encoding_combo": self.src_encoding_combo.currentText(),
            "target_encoding_combo": self.target_encoding_combo.currentText(),
            "last_source_folder": getattr(self, "last_source_folder", ""),
            "delete_original": str(self.delete_original_checkbox.isChecked()),
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            config.write(f)

    def showEvent(self, event):
        self.load_settings()
        super().showEvent(event)

    def hideEvent(self, event):
        self.save_settings()
        super().hideEvent(event)

    def select_file(self):
        start_dir = getattr(self, "last_source_folder", "")
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            '选择源文件', 
            start_dir, 
            '文本文件 (*.txt);;所有文件 (*)'
        )
        if files:
            # 显示选中的文件数量和第一个文件的路径
            self.file_input.setText(f"已选择 {len(files)} 个文件: {files[0]}...")
            # 保存文件列表
            self.selected_files = files
            # 保存当前源文件夹
            self.last_source_folder = os.path.dirname(files[0])
            # 设置默认输出文件夹为第一个文件所在文件夹
            default_output_folder = os.path.dirname(files[0])
            self.output_folder_input.setText(default_output_folder)

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择目标文件夹')
        if folder_path:
            self.output_folder_input.setText(folder_path)

    def start_conversion(self):
        try:
            if not hasattr(self, 'selected_files') or not self.selected_files:
                QMessageBox.warning(self, '错误', '请选择要转换的文件！')
                return

            # 获取编码设置
            src_encoding = self.src_encoding_input.text() or self.src_encoding_combo.currentText()
            target_encoding = self.target_encoding_input.text() or self.target_encoding_combo.currentText()
            output_folder = self.output_folder_input.text()

            if not output_folder or not os.path.isdir(output_folder):
                QMessageBox.warning(self, '错误', '请提供有效的目标文件夹路径！')
                return

            delete_original = self.delete_original_checkbox.isChecked()

            success_count = 0
            failed_files = []
            for file_path in self.selected_files:
                try:
                    current_src_encoding = src_encoding
                    if src_encoding == '自动检测':
                        detected_encoding, confidence = detect_encoding(file_path)
                        if not detected_encoding:
                            failed_files.append(f"{file_path} (无法检测编码)")
                            continue
                        current_src_encoding = detected_encoding

                    # 转换文件
                    base_name = os.path.basename(file_path)
                    name, ext = os.path.splitext(base_name)
                    new_file_path = os.path.join(output_folder, f"{name}_{target_encoding}{ext}")
                    convert_file(file_path, current_src_encoding, target_encoding)
                    # 删除原文件
                    if delete_original:
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            failed_files.append(f"{file_path} (删除原文件失败: {str(e)})")
                            continue
                    success_count += 1

                except Exception as e:
                    failed_files.append(f"{file_path} ({str(e)})")

            result_message = f"转换完成！\n成功：{success_count}/{len(self.selected_files)} 个文件"
            if failed_files:
                result_message += "\n\n转换失败的文件："
                for failed_file in failed_files:
                    result_message += f"\n- {failed_file}"
            
            self.result_label.setText(result_message)
            QMessageBox.information(self, '转换结果', result_message)
            self.save_settings()  # 操作后也保存一次

        except Exception as e:
            QMessageBox.critical(self, '错误', f'发生错误：{str(e)}')

    def update_style(self):
        # 判断自定义源编码
        if self.src_encoding_input.text().strip():
            self.src_encoding_input.setStyleSheet("color: black; background: #fffbe6;")
            self.src_encoding_combo.setStyleSheet("color: gray;")
        else:
            self.src_encoding_input.setStyleSheet("color: gray; background: #f0f0f0;")
            self.src_encoding_combo.setStyleSheet("color: black;")

        # 判断自定义目标编码
        if self.target_encoding_input.text().strip():
            self.target_encoding_input.setStyleSheet("color: black; background: #fffbe6;")
            self.target_encoding_combo.setStyleSheet("color: gray;")
        else:
            self.target_encoding_input.setStyleSheet("color: gray; background: #f0f0f0;")
            self.target_encoding_combo.setStyleSheet("color: black;")
