# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import sys
import os
# from PyQt5.QtCore import pyqtSlot
# from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Ui_MainWindow import Ui_MainWindow

from Config import Config
import plugins


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()
        
        self.list_unselect = ['选项1',  '选项2',  '选项3']
        self.list_selected = []
        

        self.list_Unselect.addItems(self.list_unselect)
        self.list_Selected.addItems(self.list_selected)
    
    @pyqtSlot()
    def on_btn_Browser_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_Browser.setText('{}'.format(dir_choose))
        
    @pyqtSlot()
    def on_btn_Export_clicked(self):
        item_num = self.list_Selected.count()
        item_list = [self.list_Selected.item(i).text() for i in range(item_num)]
        
        config = Config()
        config.setting['PATH'] = self.ledt_Browser.text()
        config.setting['ITEM'] = self.cbox_List.currentText()
        config.setting['ITEMLIST'] = ','.join(item_list)
        
        file_name, file_type = QFileDialog.getSaveFileName(self, '文件保存', self.cwd, 'Text Files(*.txt)')
        if file_name=='':
            return
        else:
            with open(file_name, 'w+') as f:
                f.write(config.toString())
                QMessageBox.information(self, '消息', '保存成功', QMessageBox.Yes)

    @pyqtSlot()
    def on_btn_Import_clicked(self):
        content_list = []
        file_name, file_type = QFileDialog.getOpenFileName(self, '配置文件选择', self.cwd, 'Text Files(*.txt)')
        if file_name=='':
            return
        else:
            with open(file_name, 'r') as f:
                content_list = f.readlines()
        config = Config()
        content_list = [content.strip().split(':', 1) for content in content_list]
        for k, v in content_list:
            config.setting[k] = v
        print(config.setting)
        
        
    @pyqtSlot(QModelIndex)
    def on_list_Unselect_doubleClicked(self, index):
        select_items = list(self.list_Unselect.selectedItems())
        if len(select_items)>1:
            QMessageBox.warning(self,  '警告',  '无法对多个条目同时操作！', QMessageBox.Yes)
        else:
            self.list_Selected.addItem(index.data())
            self.list_Unselect.takeItem(self.list_Unselect.row(*select_items))

    @pyqtSlot()
    def on_btn_Add_clicked(self):
        select_items = list(self.list_Unselect.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_Unselect.row(i)
                item = self.list_Unselect.takeItem(item_no)
                self.list_Selected.addItem(item)
    
    @pyqtSlot()
    def on_btn_Del_clicked(self):
        select_items = list(self.list_Selected.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_Selected.row(i)
                item = self.list_Selected.takeItem(item_no)
                self.list_Unselect.addItem(item)

if __name__=='__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    

