# -*- coding: utf-8 -*-

"""
Module implementing IndexWindow.
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Ui_IndexWindow import Ui_IndexWindow

import plugins
import os
from MSConfig import *
from MSConfigFile import *
from MSConfigUi import *
import configparser
import tempfile

from Register import Register

class IndexWindow(QMainWindow, Ui_IndexWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(IndexWindow, self).__init__(parent)
        self.setupUi(self)
        
        self.cwd = os.getcwd()
        
        try:
            self.cpu_number = plugins.get_cpu_number()
        except Exception as e:
            print("Error ocurrs {}".format(e))
            QMessageBox.warning(self,  'Error',  'Sorry, Not Support Current System！', QMessageBox.Yes)
            exit(-1)
            
        self.core_buttons = [self.btn_import,  self.btn_export]
        self.check_registered(self.cpu_number)
        
        # 配置文件列表
        self.config_list = [
            ['config_common.txt',  CConfigCommon,  CConfigFileCommon,  CConfigUiCommon], 
            ['config_1.txt', CConfigOne, CConfigFileOne, CConfigUiOne], 
            # ['config_2.txt', ConfigTwo, ConfigFileTwo, ConfigUITwo]
        ]
    
    def check_registered(self, cpu_number):
        result = plugins.check_registered(cpu_number)
        print(result)
        if result['code']==1:
            QMessageBox.warning(self,  '警告',  '您的软件尚未授权，请尽快注册！', QMessageBox.Yes)
            self.setWindowTitle('AutoConfiguration(未授权)')
            for btn in self.core_buttons:
                btn.setEnabled(False)
        elif result['code']==-1:
            QMessageBox.warning(self,  '警告',  '您的软件配置文件错误，请删除cfg.ini后重新运行！', QMessageBox.Yes)
            exit(1)
        else:
            QMessageBox.information(self,  '欢迎',  '您的软件已授权，请尽情使用！', QMessageBox.Yes)
            self.btn_get_license.hide()

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
    def on_btn_export_clicked(self):
        
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
            for config in self.config_list:
                cconfig = config[1]()
                cconfig_file = config[2]()
                cconfig_ui = config[3]()
                
                config_file_name = os.path.join(path_configs, config[0])
                
                cconfig_ui.ui2config(self, cconfig)
                cconfig_file.config2file(config_file_name, cconfig)
                
            QMessageBox.information(self, '消息', '保存成功', QMessageBox.Yes)

    @pyqtSlot()
    def on_btn_import_clicked(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, '配置文件选择', self.cwd, 'Text Files(*.txt)')
        if not os.path.exists(file_name) or file_name=='':
            return
            
        path_configs = os.path.join(os.path.dirname(file_name), 'params')
        if not os.path.exists(path_configs):
            QMessageBox.warning(self, '警告', '无可供导入的配置文件，请先尝试重新导入', QMessageBox.Yes)
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
        # Config配置文件读取
        with open(file_name, 'r') as f:
            config_string = f.read().replace('# ',  '')
        with  tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(config_string.encode())
        config = configparser.ConfigParser()
        config.read(tmp_file.name, encoding='utf-8')
        config.sections()
        
        

    @pyqtSlot()
    def on_btn_data_2_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_data_2.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_data_3_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_data_3.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_data_4_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_data_4.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_data_5_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_data_5.setText('{}'.format(dir_choose))

    @pyqtSlot(bool)
    def on_btn_hide_clicked(self, checked):
        if checked:
            self.widget_2.setVisible(True)
        else:
            self.widget.setVisible(False)
    
    
    '''
    @pyqtSlot(bool)
    def on_btn_cfg_data_toggled(self, checked):
        if checked:
            self.frame_data.hide()
        else:
            self.frame_data.show()
    
    @pyqtSlot(bool)
    def on_btn_cfg_data_clicked(self):
        if self.frame_data.isHidden():
            self.frame_data.show()
            
        else:
            self.frame_data.hide()
    
    @pyqtSlot()
    def on_btn_cfg_biology_clicked(self):
        if self.frame_biology.isHidden():
            self.frame_biology.show()
        else:
            self.frame_biology.hide()
    
    @pyqtSlot()
    def on_btn_cfg_mass_clicked(self):
        if self.frame_mass.isHidden():
            self.frame_mass.show()
        else:
            self.frame_mass.hide()
    '''
    
    @pyqtSlot()
    def on_btn_mass_del_clicked(self):
        select_items = list(self.list_mass_selected.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_mass_selected.row(i)
                item = self.list_mass_selected.takeItem(item_no)
                self.list_mass_unselect.addItem(item)
    
    @pyqtSlot()
    def on_btn_mass_add_clicked(self):
        select_items = list(self.list_mass_unselect.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_mass_unselect.row(i)
                item = self.list_mass_unselect.takeItem(item_no)
                self.list_mass_selected.addItem(item)
    
    @pyqtSlot(QModelIndex)
    def on_list_mass_selected_doubleClicked(self, index):
        select_items = list(self.list_mass_selected.selectedItems())
        if len(select_items)>1:
            QMessageBox.warning(self,  '警告',  '无法对多个条目同时操作！', QMessageBox.Yes)
        else:
            self.list_mass_unselect.addItem(index.data())
            self.list_mass_selected.takeItem(self.list_mass_selected.row(*select_items))
    
    @pyqtSlot(QModelIndex)
    def on_list_mass_unselect_doubleClicked(self, index):
        select_items = list(self.list_mass_unselect.selectedItems())
        if len(select_items)>1:
            QMessageBox.warning(self,  '警告',  '无法对多个条目同时操作！', QMessageBox.Yes)
        else:
            self.list_mass_selected.addItem(index.data())
            self.list_mass_unselect.takeItem(self.list_mass_unselect.row(*select_items))
    
    @pyqtSlot()
    def on_btn_data_PM_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_data_PM.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_data_PF_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_data_PF.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_data_PFE_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_data_PFE.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_data_PRE_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, '选择文件夹', self.cwd)
        if dir_choose == '':
            print('\n取消选择')
            return
        else:
            self.ledt_data_PRE.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_mass_v2u_clicked(self):
        select_items = list(self.list_mass_variable.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_mass_variable.row(i)
                item = self.list_mass_variable.takeItem(item_no)
                self.list_mass_unselect.addItem(item)
    
    @pyqtSlot()
    def on_btn_mass_u2v_clicked(self):
        select_items = list(self.list_mass_unselect.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_mass_unselect.row(i)
                item = self.list_mass_unselect.takeItem(item_no)
                self.list_mass_variable.addItem(item)
    
    @pyqtSlot()
    def on_btn_mass_f2u_clicked(self):
        select_items = list(self.list_mass_fixed.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_mass_fixed.row(i)
                item = self.list_mass_fixed.takeItem(item_no)
                self.list_mass_unselect.addItem(item)
    
    @pyqtSlot()
    def on_btn_mass_u2f_clicked(self):
        select_items = list(self.list_mass_unselect.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_mass_unselect.row(i)
                item = self.list_mass_unselect.takeItem(item_no)
                self.list_mass_fixed.addItem(item)
    
    @pyqtSlot()
    def on_btn_common_PM_clear_clicked(self):
        self.list_common_PM.clear()
    
    @pyqtSlot()
    def on_btn_common_PM_add_clicked(self):
        file_names, file_type = QFileDialog.getOpenFileNames(self, 'Files select', self.cwd, 'All Type Files(*)')
        if len(file_names)==0:
            return
        for file_name in file_names:
            self.list_common_PM.addItem(file_name)
        
    
    @pyqtSlot()
    def on_btn_common_PM_del_clicked(self):
        select_items = list(self.list_common_PM.selectedItems())
        if len(select_items)==0:
            return
        else:
            for i in select_items:
                item_no = self.list_common_PM.row(i)
                self.list_common_PM.takeItem(item_no)
    
    @pyqtSlot()
    def on_btn_common_PRE_clicked(self):
        dir_choose = QFileDialog.getExistingDirectory(self, 'Directory Select', self.cwd)
        if dir_choose == '':
            return
        else:
            self.ledt_common_PRE.setText('{}'.format(dir_choose))
    
    @pyqtSlot()
    def on_btn_common_PF_clicked(self):
        file_name, file_type = QFileDialog.getOpenFileName(self, 'PATH_FASTA File Select', self.cwd, 'All Type Files(*)')
        if not os.path.exists(file_name) or file_name=='':
            return
        self.ledt_common_PF.setText('{}'.format(file_name))
    
    @pyqtSlot(str)
    def on_cbox_common_TM_currentIndexChanged(self, p0):
        print(type(p0))
        print(type(str(p0)))
