import sys
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QFileDialog, 
                            QTableWidgetItem, QInputDialog)
from PyQt5.QtCore import QTimer, QDate
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap  # 添加QPixmap导入
from ui_main import Ui_MainWindow
from database import Database
from medicine_dialog import MedicineDialog
from utils import import_excel, export_excel

class MedicineManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 获取应用程序根目录
        if getattr(sys, 'frozen', False):
            # 如果是打包后的程序
            self.app_path = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            self.app_path = os.path.dirname(os.path.abspath(__file__))
        
        # 确保数据目录存在
        data_backup_dir = os.path.join(self.app_path, 'data', 'backup')
        os.makedirs(data_backup_dir, exist_ok=True)
        
        # 初始化数据库
        self.db = Database()
        
        # 设置信号和槽
        self.setup_connections()
        
        # 加载数据
        self.load_data()
        self.check_warnings()
        
        # 设置应用图标
        icon_path = os.path.join(self.app_path, 'icon.jpg')
        if os.path.exists(icon_path):
            # 创建一个更大的图标
            pixmap = QPixmap(icon_path)
            # 将图标放大到原来的两倍大小
            pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
        
        # 设置窗口标题
        self.setWindowTitle("新乐中医院郭神医专属")
        
        # 调整窗口大小为原来的两倍
        current_size = self.size()
        self.resize(current_size.width() * 2, current_size.height() * 2)
        
        # 美化按钮样式
        self.setup_button_styles()
    
    def setup_button_styles(self):
        """设置按钮样式，使界面更加美观"""
        # 定义不同功能按钮的样式 - 使用更柔和的蓝绿色调
        add_style = """
            QPushButton {
                background-color: #4DB6AC;
                color: white;
                border-radius: 4px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #26A69A;
            }
            QPushButton:pressed {
                background-color: #00897B;
            }
        """
        
        edit_style = """
            QPushButton {
                background-color: #5C6BC0;
                color: white;
                border-radius: 4px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3F51B5;
            }
            QPushButton:pressed {
                background-color: #303F9F;
            }
        """
        
        delete_style = """
            QPushButton {
                background-color: #EF5350;
                color: white;
                border-radius: 4px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E53935;
            }
            QPushButton:pressed {
                background-color: #D32F2F;
            }
        """
        
        search_style = """
            QPushButton {
                background-color: #78909C;
                color: white;
                border-radius: 4px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #607D8B;
            }
            QPushButton:pressed {
                background-color: #546E7A;
            }
        """
        
        import_export_style = """
            QPushButton {
                background-color: #7986CB;
                color: white;
                border-radius: 4px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5C6BC0;
            }
            QPushButton:pressed {
                background-color: #3F51B5;
            }
        """
        
        # 应用样式到对应按钮
        self.ui.btn_add.setStyleSheet(add_style)
        self.ui.btn_edit.setStyleSheet(edit_style)
        self.ui.btn_delete.setStyleSheet(delete_style)
        self.ui.btn_reduce.setStyleSheet(delete_style)
        self.ui.btn_search.setStyleSheet(search_style)
        self.ui.btn_import.setStyleSheet(import_export_style)
        self.ui.btn_export.setStyleSheet(import_export_style)
        self.ui.btn_select_all.setStyleSheet(edit_style)
    
    def setup_connections(self):
        # 连接按钮信号
        self.ui.btn_select_all.clicked.connect(self.select_all_medicines)  # 连接全选按钮
        self.ui.btn_import.clicked.connect(self.import_data)
        self.ui.btn_export.clicked.connect(self.export_data)
        self.ui.btn_add.clicked.connect(self.add_medicine)
        self.ui.btn_edit.clicked.connect(self.edit_medicine)
        self.ui.btn_delete.clicked.connect(self.delete_medicine)
        self.ui.btn_reduce.clicked.connect(self.reduce_quantity)
        self.ui.btn_search.clicked.connect(self.search_medicine)
        self.ui.txt_search.returnPressed.connect(self.search_medicine)
    
    def load_data(self):
        # 从数据库加载数据并显示在表格中
        medicines = self.db.get_all_medicines()
        self.update_table(medicines)
        self.check_warnings()
    
    def update_table(self, medicines):
        # 清空表格
        self.ui.table_medicines.setRowCount(0)
        
        # 添加数据到表格
        for row, medicine in enumerate(medicines):
            self.ui.table_medicines.insertRow(row)
            self.ui.table_medicines.setItem(row, 0, QTableWidgetItem(str(medicine['id'])))
            self.ui.table_medicines.setItem(row, 1, QTableWidgetItem(medicine['name']))
            self.ui.table_medicines.setItem(row, 2, QTableWidgetItem(medicine['manufacturer']))
            self.ui.table_medicines.setItem(row, 3, QTableWidgetItem(medicine['production_date']))
            self.ui.table_medicines.setItem(row, 4, QTableWidgetItem(medicine['expiry_date']))
            self.ui.table_medicines.setItem(row, 5, QTableWidgetItem(str(medicine['min_quantity'])))
            self.ui.table_medicines.setItem(row, 6, QTableWidgetItem(str(medicine['current_quantity'])))
    
    def import_data(self):
        # 导入Excel数据
        file_path, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            try:
                medicines = import_excel(file_path)
                imported_count = 0
                updated_count = 0
                
                for new_medicine in medicines:
                    # 检查是否存在相同药品（名称、厂家、生产日期和截止日期都相同）
                    existing_medicines = self.db.search_medicines(new_medicine['name'])
                    found_match = False
                    
                    for existing in existing_medicines:
                        if (existing['name'] == new_medicine['name'] and
                            existing['manufacturer'] == new_medicine['manufacturer'] and
                            existing['production_date'] == new_medicine['production_date'] and
                            existing['expiry_date'] == new_medicine['expiry_date']):
                            
                            # 找到匹配的药品，更新库存数量
                            updated_medicine = existing.copy()
                            updated_medicine['current_quantity'] += new_medicine['current_quantity']
                            self.db.update_medicine(updated_medicine)
                            found_match = True
                            updated_count += 1
                            break
                    
                    if not found_match:
                        # 没有找到匹配的药品，添加新药品
                        self.db.add_medicine(new_medicine)
                        imported_count += 1
                
                self.load_data()
                QMessageBox.information(self, "导入成功", 
                                       f"成功导入 {imported_count} 条新药品记录\n更新 {updated_count} 条已有药品库存")
            except Exception as e:
                QMessageBox.critical(self, "导入失败", f"导入过程中发生错误: {str(e)}")
    
    def export_data(self):
        # 导出数据到Excel
        file_path, _ = QFileDialog.getSaveFileName(self, "保存Excel文件", "", "Excel Files (*.xlsx)")
        if file_path:
            try:
                medicines = self.db.get_all_medicines()
                export_excel(medicines, file_path)
                QMessageBox.information(self, "导出成功", f"成功导出 {len(medicines)} 条药品记录")
            except Exception as e:
                QMessageBox.critical(self, "导出失败", f"导出过程中发生错误: {str(e)}")
    
    def add_medicine(self):
        # 添加新药品
        dialog = MedicineDialog(self)
        if dialog.exec_():
            medicine = dialog.get_medicine_data()
            self.db.add_medicine(medicine)
            self.load_data()
            QMessageBox.information(self, "添加成功", "药品添加成功")
    
    def edit_medicine(self):
        # 编辑选中的药品
        selected_rows = self.ui.table_medicines.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要编辑的药品")
            return
        
        row = selected_rows[0].row()
        medicine_id = int(self.ui.table_medicines.item(row, 0).text())
        medicine = self.db.get_medicine_by_id(medicine_id)
        
        dialog = MedicineDialog(self, medicine)
        if dialog.exec_():
            updated_medicine = dialog.get_medicine_data()
            updated_medicine['id'] = medicine_id
            self.db.update_medicine(updated_medicine)
            self.load_data()
            QMessageBox.information(self, "编辑成功", "药品信息已更新")
    
    def select_all_medicines(self):
        # 全选所有药品
        self.ui.table_medicines.selectAll()
    
    def delete_medicine(self):
        # 删除选中的药品
        selected_rows = self.ui.table_medicines.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要删除的药品")
            return
        
        # 获取唯一的行索引
        unique_rows = set()
        for index in selected_rows:
            unique_rows.add(index.row())
        
        # 确认删除
        reply = QMessageBox.question(self, "确认删除", 
                                    f"确定要删除选中的 {len(unique_rows)} 个药品吗？",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # 收集要删除的药品ID
            medicine_ids = []
            for row in unique_rows:
                medicine_id = int(self.ui.table_medicines.item(row, 0).text())
                medicine_ids.append(medicine_id)
            
            # 删除药品
            for medicine_id in medicine_ids:
                self.db.delete_medicine(medicine_id)
            
            self.load_data()
            QMessageBox.information(self, "删除成功", f"已删除 {len(medicine_ids)} 个药品")
    
    def reduce_quantity(self):
        # 核减药品数量
        selected_rows = self.ui.table_medicines.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "警告", "请先选择要核减的药品")
            return
        
        row = selected_rows[0].row()
        medicine_id = int(self.ui.table_medicines.item(row, 0).text())
        medicine = self.db.get_medicine_by_id(medicine_id)
        
        quantity, ok = QInputDialog.getInt(self, "核减数量", 
                                          f"当前库存: {medicine['current_quantity']}\n请输入要核减的数量:",
                                          1, 1, medicine['current_quantity'], 1)
        if ok:
            new_quantity = medicine['current_quantity'] - quantity
            self.db.update_quantity(medicine_id, new_quantity)
            self.load_data()
            QMessageBox.information(self, "核减成功", f"已核减 {quantity} 个药品，当前库存: {new_quantity}")
    
    def search_medicine(self):
        # 搜索药品
        keyword = self.ui.txt_search.text().strip()
        if keyword:
            medicines = self.db.search_medicines(keyword)
            self.update_table(medicines)
            self.statusBar().showMessage(f"找到 {len(medicines)} 条匹配记录")
        else:
            self.load_data()
            self.statusBar().showMessage("显示所有记录")
    
    def auto_backup(self):
        # 自动备份数据
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(self.app_path, 'data', 'backup')
        os.makedirs(backup_dir, exist_ok=True)
        backup_file = os.path.join(backup_dir, f"medicines_backup_{timestamp}.json")
        
        try:
            medicines = self.db.get_all_medicines()
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(medicines, f, ensure_ascii=False, indent=2)
            self.statusBar().showMessage(f"数据已自动备份 - {timestamp}")
        except Exception as e:
            self.statusBar().showMessage(f"自动备份失败: {str(e)}")
    
    def check_warnings(self):
        # 检查过期和库存不足的药品
        current_date = QDate.currentDate()
        warning_days = 30  # 提前30天提醒即将过期
        
        # 首先收集所有药品信息
        all_medicines = []
        for row in range(self.ui.table_medicines.rowCount()):
            medicine_info = {
                'id': int(self.ui.table_medicines.item(row, 0).text()),
                'name': self.ui.table_medicines.item(row, 1).text(),
                'manufacturer': self.ui.table_medicines.item(row, 2).text(),
                'expiry_date_str': self.ui.table_medicines.item(row, 4).text(),
                'min_quantity': int(self.ui.table_medicines.item(row, 5).text()),
                'current_quantity': int(self.ui.table_medicines.item(row, 6).text()),
                'row': row,
                'expiry_warning': False,
                'quantity_warning': False
            }
            
            # 解析过期日期
            expiry_date = QDate.fromString(medicine_info['expiry_date_str'], "yyyy-MM-dd")
            days_to_expiry = current_date.daysTo(expiry_date)
            medicine_info['days_to_expiry'] = days_to_expiry
            
            # 检查是否已过期或即将过期
            if days_to_expiry <= warning_days:
                medicine_info['expiry_warning'] = True
            
            all_medicines.append(medicine_info)
        
        # 计算同名称同厂家且未过期药品的总库存
        medicine_groups = {}
        for medicine in all_medicines:
            # 跳过已过期或即将过期的药品
            if medicine['expiry_warning']:
                continue
                
            key = f"{medicine['name']}_{medicine['manufacturer']}"
            if key not in medicine_groups:
                medicine_groups[key] = {
                    'name': medicine['name'],
                    'manufacturer': medicine['manufacturer'],
                    'total_quantity': 0,
                    'min_quantity': medicine['min_quantity'],
                    'medicines': []
                }
            
            medicine_groups[key]['total_quantity'] += medicine['current_quantity']
            medicine_groups[key]['medicines'].append(medicine)
        
        # 检查每个药品组的总库存是否低于最少保有数量
        for group_key, group in medicine_groups.items():
            if group['total_quantity'] < group['min_quantity']:
                # 标记该组所有药品为库存不足
                for medicine in group['medicines']:
                    medicine['quantity_warning'] = True
        
        # 应用警告标记到表格
        for medicine in all_medicines:
            row = medicine['row']
            for col in range(self.ui.table_medicines.columnCount()):
                item = self.ui.table_medicines.item(row, col)
                if medicine['expiry_warning']:
                    # 过期或即将过期标红
                    item.setBackground(QColor(255, 200, 200))  # 浅红色
                elif medicine['quantity_warning']:
                    # 库存不足标黄
                    item.setBackground(QColor(255, 230, 100))  # 加深的黄色
                else:
                    # 正常状态为白色
                    item.setBackground(QColor(255, 255, 255))  # 白色

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MedicineManagementSystem()
    window.show()
    sys.exit(app.exec_())