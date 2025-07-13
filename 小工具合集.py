import sys
import os
import logging
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, 
    QHBoxLayout, QStackedWidget, QFrame,
    QMessageBox  # 添加QMessageBox用于显示错误信息
)
from 编码转换_ui import EncodingConverterUI
from 重命名_ui import RenameToolUI  # 新增导入
import configparser

__version__ = "0.0.2"

# 配置日志系统
log_file = os.path.join(os.path.dirname(sys.argv[0]), 'app.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 在主程序入口添加
CONFIG_FILE = os.path.join(os.path.dirname(sys.argv[0]), "tool_config.ini")
if not os.path.exists(CONFIG_FILE):
    config = configparser.ConfigParser()
    config["main"] = {}
    config["encoding"] = {}
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        config.write(f)

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        logger.info("MainUI 初始化开始")
        self.setWindowTitle('我的小工具合集')
        self.setGeometry(100, 100, 800, 500)
        self.current_tool = None
        self.init_ui()
        logger.info("MainUI 初始化完成")

    def init_ui(self):
        logger.info("init_ui 开始")
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # 左侧菜单
        left_panel = QFrame()
        left_panel.setMaximumWidth(200)
        left_panel.setMinimumWidth(200)
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        self.encoding_tool_button = QPushButton('编码转换工具')
        self.encoding_tool_button.setMinimumHeight(40)
        self.encoding_tool_button.clicked.connect(self.show_encoding_tool)
        left_layout.addWidget(self.encoding_tool_button)

        self.rename_tool_button = QPushButton('文件重命名工具')
        self.rename_tool_button.setMinimumHeight(40)
        self.rename_tool_button.clicked.connect(self.show_rename_tool)
        left_layout.addWidget(self.rename_tool_button)

        left_layout.addStretch()

        # 右侧内容
        self.right_panel = QFrame()
        self.right_layout = QHBoxLayout()
        self.right_panel.setLayout(self.right_layout)

        self.stacked_widget = QStackedWidget()
        self.right_layout.addWidget(self.stacked_widget)

        self.main_page = QWidget()
        self.stacked_widget.addWidget(self.main_page)

        # 工具实例只创建一次，不销毁
        self.encoding_tool = EncodingConverterUI()
        self.encoding_tool.back_button.setText('关闭')
        self.encoding_tool.back_button.clicked.connect(self.hide_encoding_tool)
        self.stacked_widget.addWidget(self.encoding_tool)

        self.rename_tool = RenameToolUI()
        self.rename_tool.back_button.setText('关闭')
        self.rename_tool.back_button.clicked.connect(self.hide_rename_tool)
        self.stacked_widget.addWidget(self.rename_tool)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(self.right_panel)
        logger.info("init_ui 完成")

    def show_encoding_tool(self):
        logger.info("show_encoding_tool 被调用")
        self.stacked_widget.setCurrentWidget(self.encoding_tool)
        self.current_tool = self.encoding_tool

    def hide_encoding_tool(self):
        logger.info("hide_encoding_tool 被调用")
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.current_tool = None

    def show_rename_tool(self):
        logger.info("show_rename_tool 被调用")
        self.stacked_widget.setCurrentWidget(self.rename_tool)
        self.current_tool = self.rename_tool

    def hide_rename_tool(self):
        logger.info("hide_rename_tool 被调用")
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.current_tool = None

# 主程序入口
if __name__ == "__main__":
    try:
        logger.info("程序启动")
        app = QApplication(sys.argv)
        main_window = MainUI()
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        logger.critical("发生了一个致命错误：", exc_info=True)
        # 弹出错误信息
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("发生了一个错误：")
        msg.setInformativeText(str(e))
        msg.setWindowTitle("错误")
        msg.exec_()