from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt

class Ui_MainWindow:
    def setupUi(self, MainWindow):
        # 设置主窗口
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        
        # 创建中央窗口部件
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        
        # 创建主布局
        self.main_layout = QVBoxLayout(self.centralwidget)
        
        # 创建顶部工具栏
        self.toolbar_layout = QHBoxLayout()
        
        # 搜索框
        self.lbl_search = QLabel("搜索:")
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("输入药品名称或厂商进行搜索")
        self.btn_search = QPushButton("搜索")
        
        self.toolbar_layout.addWidget(self.lbl_search)
        self.toolbar_layout.addWidget(self.txt_search)
        self.toolbar_layout.addWidget(self.btn_search)
        
        # 添加到主布局
        self.main_layout.addLayout(self.toolbar_layout)
        
        # 创建表格
        self.table_medicines = QTableWidget()
        self.table_medicines.setColumnCount(7)
        self.table_medicines.setHorizontalHeaderLabels(["ID", "药品名称", "厂商", "生产日期", "截止日期", "最少保有量", "现有数量"])
        
        # 设置表格列宽
        header = self.table_medicines.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID列
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # 药品名称列
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # 厂商列
        
        # 添加到主布局
        self.main_layout.addWidget(self.table_medicines)
        
        # 创建底部按钮栏
        self.button_layout = QHBoxLayout()
        
        # 创建按钮
        self.btn_select_all = QPushButton("全选")  # 添加全选按钮
        self.btn_import = QPushButton("导入Excel")
        self.btn_export = QPushButton("导出Excel")
        self.btn_add = QPushButton("添加药品")
        self.btn_edit = QPushButton("编辑药品")
        self.btn_delete = QPushButton("删除药品")
        self.btn_reduce = QPushButton("核减数量")
        
        # 添加按钮到布局
        self.button_layout.addWidget(self.btn_select_all)  # 添加全选按钮到布局
        self.button_layout.addWidget(self.btn_import)
        self.button_layout.addWidget(self.btn_export)
        self.button_layout.addWidget(self.btn_add)
        self.button_layout.addWidget(self.btn_edit)
        self.button_layout.addWidget(self.btn_delete)
        self.button_layout.addWidget(self.btn_reduce)
        
        # 添加到主布局
        self.main_layout.addLayout(self.button_layout)
        
        # 设置状态栏
        MainWindow.statusBar()