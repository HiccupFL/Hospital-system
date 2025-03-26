from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
                            QLabel, QLineEdit, QDateEdit, QSpinBox, QPushButton)
from PyQt5.QtCore import QDate

class MedicineDialog(QDialog):
    def __init__(self, parent=None, medicine=None):
        super().__init__(parent)
        self.medicine = medicine
        self.setWindowTitle("药品信息" if medicine else "添加新药品")
        self.setup_ui()
        
        if medicine:
            self.populate_form()
    
    def setup_ui(self):
        # 创建表单布局
        form_layout = QFormLayout()
        
        # 药品名称
        self.txt_name = QLineEdit()
        form_layout.addRow("药品名称:", self.txt_name)
        
        # 厂商
        self.txt_manufacturer = QLineEdit()
        form_layout.addRow("厂商:", self.txt_manufacturer)
        
        # 生产日期
        self.date_production = QDateEdit()
        self.date_production.setCalendarPopup(True)
        self.date_production.setDate(QDate.currentDate())
        form_layout.addRow("生产日期:", self.date_production)
        
        # 截止日期
        self.date_expiry = QDateEdit()
        self.date_expiry.setCalendarPopup(True)
        self.date_expiry.setDate(QDate.currentDate().addYears(1))  # 默认一年后过期
        form_layout.addRow("截止日期:", self.date_expiry)
        
        # 最少保有数量
        self.spin_min_quantity = QSpinBox()
        self.spin_min_quantity.setRange(0, 999999)
        form_layout.addRow("最少保有数量:", self.spin_min_quantity)
        
        # 现有数量
        self.spin_current_quantity = QSpinBox()
        self.spin_current_quantity.setRange(0, 999999)
        form_layout.addRow("现有数量:", self.spin_current_quantity)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        self.btn_save = QPushButton("保存")
        self.btn_cancel = QPushButton("取消")
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)
        
        # 连接信号
        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        self.resize(400, 300)
    
    def populate_form(self):
        # 填充表单数据
        self.txt_name.setText(self.medicine['name'])
        self.txt_manufacturer.setText(self.medicine['manufacturer'])
        
        # 设置日期
        production_date = QDate.fromString(self.medicine['production_date'], "yyyy-MM-dd")
        self.date_production.setDate(production_date)
        
        expiry_date = QDate.fromString(self.medicine['expiry_date'], "yyyy-MM-dd")
        self.date_expiry.setDate(expiry_date)
        
        # 设置数量
        self.spin_min_quantity.setValue(self.medicine['min_quantity'])
        self.spin_current_quantity.setValue(self.medicine['current_quantity'])
    
    def get_medicine_data(self):
        # 获取表单数据
        return {
            'name': self.txt_name.text(),
            'manufacturer': self.txt_manufacturer.text(),
            'production_date': self.date_production.date().toString("yyyy-MM-dd"),
            'expiry_date': self.date_expiry.date().toString("yyyy-MM-dd"),
            'min_quantity': self.spin_min_quantity.value(),
            'current_quantity': self.spin_current_quantity.value()
        }