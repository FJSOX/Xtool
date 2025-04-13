import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, 
    QHBoxLayout, QStackedWidget, QFrame
)
from 编码转换_ui import EncodingConverterUI
from 重命名_ui import RenameToolUI  # 新增导入

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('我的小工具合集')
        self.setGeometry(100, 100, 800, 500)  # 调整窗口大小
        self.current_tool = None  # 记录当前显示的工具
        self.init_ui()

    def init_ui(self):
        # 创建主布局为水平布局
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # 创建左侧菜单面板
        left_panel = QFrame()
        left_panel.setMaximumWidth(200)  # 设置最大宽度
        left_panel.setMinimumWidth(200)  # 设置最小宽度
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)
        
        # 创建工具按钮
        self.encoding_tool_button = QPushButton('编码转换工具')
        self.encoding_tool_button.setMinimumHeight(40)  # 设置按钮高度
        self.encoding_tool_button.clicked.connect(self.show_encoding_tool)
        left_layout.addWidget(self.encoding_tool_button)
        
        # 新增重命名工具按钮
        self.rename_tool_button = QPushButton('文件重命名工具')
        self.rename_tool_button.setMinimumHeight(40)
        self.rename_tool_button.clicked.connect(self.show_rename_tool)
        left_layout.addWidget(self.rename_tool_button)
        
        left_layout.addStretch()  # 添加弹性空间
        
        # 创建右侧内容区域
        self.right_panel = QFrame()
        self.right_layout = QHBoxLayout()
        self.right_panel.setLayout(self.right_layout)
        
        # 创建堆叠窗口
        self.stacked_widget = QStackedWidget()
        self.right_layout.addWidget(self.stacked_widget)
        
        # 创建主页面
        self.main_page = QWidget()
        self.stacked_widget.addWidget(self.main_page)
        
        # 创建工具实例
        self.encoding_tool = EncodingConverterUI()
        self.encoding_tool.back_button.setText('关闭')  # 将返回按钮改为关闭按钮
        self.encoding_tool.back_button.clicked.connect(self.close_encoding_tool)
        self.stacked_widget.addWidget(self.encoding_tool)
        
        # 创建重命名工具界面
        self.rename_tool = RenameToolUI()
        self.rename_tool.back_button.setText('关闭')
        self.rename_tool.back_button.clicked.connect(self.close_rename_tool)
        self.stacked_widget.addWidget(self.rename_tool)
        
        # 将左侧面板和右侧内容区域添加到主布局
        main_layout.addWidget(left_panel)
        main_layout.addWidget(self.right_panel)

    def show_encoding_tool(self):
        # 如果有当前显示的工具，先隐藏它
        if self.current_tool:
            self.stacked_widget.setCurrentWidget(self.main_page)
        
        # 显示编码转换工具
        self.stacked_widget.setCurrentWidget(self.encoding_tool)
        self.current_tool = self.encoding_tool

    def close_encoding_tool(self):
        # 从堆叠窗口中移除并删除实例
        self.stacked_widget.removeWidget(self.encoding_tool)
        self.encoding_tool.deleteLater()
        # 创建新实例
        self.encoding_tool = EncodingConverterUI()
        self.encoding_tool.back_button.setText('关闭')
        self.encoding_tool.back_button.clicked.connect(self.close_encoding_tool)
        self.stacked_widget.addWidget(self.encoding_tool)
        # 切换到主页面
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.current_tool = None

    def show_rename_tool(self):
        # 如果有当前显示的工具，先隐藏它
        if self.current_tool:
            self.stacked_widget.setCurrentWidget(self.main_page)
        
        # 显示重命名工具
        self.stacked_widget.setCurrentWidget(self.rename_tool)
        self.current_tool = self.rename_tool

    def close_rename_tool(self):
        # 从堆叠窗口中移除并删除实例
        self.stacked_widget.removeWidget(self.rename_tool)
        self.rename_tool.deleteLater()
        # 创建新实例
        self.rename_tool = RenameToolUI()
        self.rename_tool.back_button.setText('关闭')
        self.rename_tool.back_button.clicked.connect(self.close_rename_tool)
        self.stacked_widget.addWidget(self.rename_tool)
        # 切换到主页面
        self.stacked_widget.setCurrentWidget(self.main_page)
        self.current_tool = None

# 主程序入口
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainUI()
    main_window.show()
    sys.exit(app.exec_())
