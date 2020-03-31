# -*- coding: utf-8 -*-

"""
Module implementing IndexWindow.
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor

from Ui_IndexWindow import Ui_IndexWindow

import plugins
import os
import re
from MSConfig import *
from MSConfigFile import *
from MSConfigUi import *

from Register import Register

class IndexWindow(QMainWindow, Ui_IndexWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        super(IndexWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.cwd = os.getcwd()
        self.anchor_file_name = ''
        self.color_warning = QColor(255, 0, 0)
        self.color_normal = QColor(255, 255, 255)
        
        try:
            self.cpu_number = plugins.get_cpu_number()
        except Exception as e:
            print("Error ocurrs {}".format(e))
            QMessageBox.warning(self,  'Error',  'Sorry, Not Support By Current System！', QMessageBox.Yes)
            exit(-1)
            
        self.core_buttons = [self.btn_import,  self.btn_save, self.btn_save_as, self.btn_run]
        self.check_registered(self.cpu_number)
        
        # 配置文件列表
        self.config_list = [
            ['config_1.txt', CConfigOne, CConfigFileOne, CConfigUiOne], 
            ['config_2.txt', CConfigTwo, CConfigFileTwo, CConfigUiTwo]
        ]
    
    def check_registered(self, cpu_number):
        result = plugins.check_registered(cpu_number)
        print(result)
        if result['code']==1 or result['code']==2:
            QMessageBox.warning(self,  'Warning',  '您的软件尚未授权，请尽快注册！', QMessageBox.Yes)
            self.setWindowTitle('AutoConfiguration(未授权)')
            for btn in self.core_buttons:
                btn.setEnabled(False)
        elif result['code']==-1:
            QMessageBox.warning(self,  'Warning',  '您的软件配置文件错误，请删除cfg.ini后重新运行！', QMessageBox.Yes)
            exit(1)
        else:
            QMessageBox.information(self,  'Welcome',  '您的软件已授权，请尽情使用！', QMessageBox.Yes)
            self.btn_get_license.hide()
            self.btn_save.setEnabled(False)
            self.btn_run.setEnabled(False)

    @pyqtSlot()
    def on_btn_get_license_clicked(self):
        # self.tab_box.hide()
        self.lbl_status.setText('联网申请中..')
        self.pbar_status.setRange(0,  0)
        
        # 加载并初始化注册界面
        register = Register(self)
        register.ledt_number.setText(self.cpu_number)
        code = register.exec_()
        
        if register.result['code']==0:
            self.setWindowTitle('AutoConfiguration(已授权)')
            self.btn_get_license.hide()
            for btn in self.core_buttons:
                btn.setEnabled(True)
            self.lbl_status.setText('运行状态')
            self.pbar_status.setRange(0,  100)
        print("Code: {}".format(code))
    
    @pyqtSlot()
    def on_btn_save_clicked(self):
        file_name = self.anchor_file_name
        path_configs = os.path.join(os.path.dirname(file_name), 'params')
        if not os.path.exists(path_configs):
            os.makedirs(path_configs)
        with open(file_name, 'w') as f:
            f.write('')
        for i in range(len(self.config_list)):
            cconfig = self.config_list[i][1]() if i==0 else self.config_list[i][1](self.config_list[i-1][-1])
            cconfig_file = self.config_list[i][2]()
            cconfig_ui = self.config_list[i][3]()
            
            config_file_name = os.path.join(path_configs, self.config_list[i][0])
            
            cconfig_ui.ui2config(self, cconfig)
            cconfig_file.config2file(config_file_name, cconfig)
            
            self.config_list[i].append(cconfig)
            
        QMessageBox.information(self, '消息', '保存成功', QMessageBox.Yes)

    @pyqtSlot()
    def on_btn_save_as_clicked(self):
        if len(self.config_list)==0:
            QMessageBox.warning(self, '消息', '无可供导出的配置文件，请先尝试导入', QMessageBox.Yes)
            return
        file_name, file_type = QFileDialog.getSaveFileName(self, '文件保存', self.cwd, 'Text Files(*.txt)')
        if file_name=='':
            return
        else:
            path_configs = os.path.join(os.path.dirname(file_name), 'params')
            if not os.path.exists(path_configs):
                os.makedirs(path_configs)
            with open(file_name, 'w') as f:
                f.write('')
            for i in range(len(self.config_list)):
                cconfig = self.config_list[i][1]() if i==0 else self.config_list[i][1](self.config_list[i-1][-1])
                cconfig_file = self.config_list[i][2]()
                cconfig_ui = self.config_list[i][3]()
                
                config_file_name = os.path.join(path_configs, self.config_list[i][0])
                
                cconfig_ui.ui2config(self, cconfig)
                cconfig_file.config2file(config_file_name, cconfig)
                
                self.config_list[i].append(cconfig)
                
            QMessageBox.information(self, '消息', '保存成功', QMessageBox.Yes)

    @pyqtSlot()
    def on_btn_import_clicked(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, 'Choose the file', self.cwd, 'Text Files(*.txt)')
        if not os.path.exists(file_name) or file_name=='':
            return
        
        # 有配置文件时，方可使用保存按钮
        self.anchor_file_name = file_name
        self.btn_save.setEnabled(True)
        
        # 由锚点文件检索并读取具体的配置文件
        path_configs = os.path.join(os.path.dirname(file_name), 'params')
        if not os.path.exists(path_configs):
            QMessageBox.warning(self, 'Warning', '无可供导入的配置文件，请先尝试重新导入', QMessageBox.Yes)
            return
        name_configs = os.listdir(path_configs)
        self.config_list = list(filter(lambda c: c[0] in name_configs, self.config_list))

        for config in self.config_list:
            cconfig = config[1]()
            cconfig_file = config[2]()
            cconfig_ui = config[3]()
            
            config_file_name = os.path.join(path_configs, config[0])
            
            cconfig_file.file2config(config_file_name, cconfig)
            cconfig_ui.config2ui(self, cconfig)
            
        QMessageBox.information(self, 'Success', 'Config File Load Success!', QMessageBox.Yes)
        return

    @pyqtSlot()
    def on_btn_run_clicked(self):
        os.system('notepad.exe {}'.format(self.anchor_file_name))
        pass
    
    def check_row(self, table, row, value, value_rule=None):
        table.setItem(row, 1, QTableWidgetItem(value))
        flag = re.match(re.compile(value_rule), value) if value_rule else True
        color = self.color_normal if flag else self.color_warning
        for i in range(2):
            table.item(row, i).setBackground(color)
        return 0 if flag else 1
    
    def chek_pannels(self):
        num_error = 0
        # Pannel One
        item_cfg1_TM = self.cbox_cfg1_TM.currentText()
        num_error += self.check_row(self.tbl_cfg1, 0, item_cfg1_TM, r'(raw)|(ms1)|(mgf)')
        item_num = self.list_cfg1_PM.count()
        item_cfg1_PM =  '|'.join([self.list_cfg1_PM.item(i).text() for i in range(item_num)])
        num_error += self.check_row(self.tbl_cfg1, 1, item_cfg1_PM, r'.+')
        item_cfg1_PF = self.ledt_cfg1_PF.text()
        num_error += self.check_row(self.tbl_cfg1, 2, item_cfg1_PF, r'.+')
        item_cfg1_PRE = self.ledt_cfg1_PRE.text()
        num_error += self.check_row(self.tbl_cfg1, 3, item_cfg1_PRE, r'.+')
        return num_error
    
    # Summary 选项卡点击时，自动检查所有字段拼写
    @pyqtSlot(int)
    def on_tab_box_currentChanged(self, index):
        if index==2:
            num_error = self.chek_pannels()
            if num_error==0:
                self.btn_run.setEnabled(True)
            # self.tbl_cfg1.item(0, 0).setBackground(self.color_warning)
            pass
            # self.tbl_cfg1.setItem(0, 1, QTableWidgetItem('Polly'))
        
    @pyqtSlot()
    def on_btn_cfg2_2_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_cfg2_2.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_cfg2_3_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_cfg2_3.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_cfg2_4_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_cfg2_4.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_cfg2_5_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_cfg2_5.setText('{}'.format(dir_choose))

    @pyqtSlot(bool)
    def on_btn_hide_clicked(self, checked):
        if checked:
            self.widget_2.setVisible(True)
        else:
            self.widget.setVisible(False)
    
    
    
    @pyqtSlot()
    def on_btn_cfg2_del_clicked(self):
        select_items = list(self.list_cfg2_selected.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_cfg2_selected.row(i)
                item = self.list_cfg2_selected.takeItem(item_no)
                self.list_cfg2_unselect.addItem(item)
    
    @pyqtSlot()
    def on_btn_cfg2_add_clicked(self):
        select_items = list(self.list_cfg2_unselect.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_cfg2_unselect.row(i)
                item = self.list_cfg2_unselect.takeItem(item_no)
                self.list_cfg2_selected.addItem(item)
    
    @pyqtSlot(QModelIndex)
    def on_list_cfg2_selected_doubleClicked(self, index):
        select_items = list(self.list_cfg2_selected.selectedItems())
        if len(select_items)>1:
            QMessageBox.warning(self,  '警告',  '无法对多个条目同时操作！', QMessageBox.Yes)
        else:
            self.list_cfg2_unselect.addItem(index.data())
            self.list_cfg2_selected.takeItem(self.list_cfg2_selected.row(*select_items))
    
    @pyqtSlot(QModelIndex)
    def on_list_cfg2_unselect_doubleClicked(self, index):
        select_items = list(self.list_cfg2_unselect.selectedItems())
        if len(select_items)>1:
            QMessageBox.warning(self,  '警告',  '无法对多个条目同时操作！', QMessageBox.Yes)
        else:
            self.list_cfg2_selected.addItem(index.data())
            self.list_cfg2_unselect.takeItem(self.list_cfg2_unselect.row(*select_items))
    
    @pyqtSlot()
    def on_btn_cfg2_PM_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_cfg2_PM.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_cfg2_PF_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_cfg2_PF.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_cfg2_PFE_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_cfg2_PFE.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_cfg2_PRE_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_cfg2_PRE.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_cfg2_v2u_clicked(self):
        select_items = list(self.list_cfg2_variable.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_cfg2_variable.row(i)
                item = self.list_cfg2_variable.takeItem(item_no)
                self.list_cfg2_unselect.addItem(item)
    
    @pyqtSlot()
    def on_btn_cfg2_u2v_clicked(self):
        select_items = list(self.list_cfg2_unselect.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_cfg2_unselect.row(i)
                item = self.list_cfg2_unselect.takeItem(item_no)
                self.list_cfg2_variable.addItem(item)
    
    @pyqtSlot()
    def on_btn_cfg2_f2u_clicked(self):
        select_items = list(self.list_cfg2_fixed.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_cfg2_fixed.row(i)
                item = self.list_cfg2_fixed.takeItem(item_no)
                self.list_cfg2_unselect.addItem(item)
    
    @pyqtSlot()
    def on_btn_cfg2_u2f_clicked(self):
        select_items = list(self.list_cfg2_unselect.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_cfg2_unselect.row(i)
                item = self.list_cfg2_unselect.takeItem(item_no)
                self.list_cfg2_fixed.addItem(item)
    
    @pyqtSlot()
    def on_btn_cfg1_PM_clear_clicked(self):
        self.list_cfg1_PM.clear()
    
    @pyqtSlot()
    def on_btn_cfg1_PM_add_clicked(self):
        file_names, file_type = QFileDialog.getOpenFileNames(self, 'Files select', self.cwd, 'All Type Files(*)')
        if len(file_names)==0:
            return
        for file_name in file_names:
            self.list_cfg1_PM.addItem(file_name)
        
    
    @pyqtSlot()
    def on_btn_cfg1_PM_del_clicked(self):
        select_items = list(self.list_cfg1_PM.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_cfg1_PM.row(i)
                self.list_cfg1_PM.takeItem(item_no)
    
    @pyqtSlot()
    def on_btn_cfg1_PRE_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, 'Directory Select', self.cwd)
        if dir_choose == '':
            return
        else:
            self.ledt_cfg1_PRE.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_cfg1_PF_clicked(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, 'PATH_FASTA File Select', self.cwd, 'All Type Files(*)')
        if not os.path.exists(file_name) or file_name=='':
            return
        self.ledt_cfg1_PF.setText('{}'.format(file_name))
    
    @pyqtSlot(str)
    def on_cbox_cfg1_TM_currentIndexChanged(self, p0):
        print(type(p0))
        print(type(str(p0)))
    

