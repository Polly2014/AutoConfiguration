# -*- coding: utf-8 -*-

"""
Module implementing Register.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *

from Ui_Register import Ui_Register
import plugins


class Register(QDialog, Ui_Register):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Register, self).__init__(parent)
        self.setupUi(self)
        
        self.result = {'code':-1, 'message': 'Not Regist Yet'}
    
    @pyqtSlot()
    def on_btn_submit_clicked(self):
        sn = self.ledt_number.text()
        username = self.ledt_username.text()
        email = self.ledt_email.text()
        if len(username)==0:
            QMessageBox.information(self, 'Warning', 'Username is empty, please fill it!', QMessageBox.Yes)
            return
        if len(email)==0:
            QMessageBox.information(self, 'Warning', 'Email is empty, please fill it!', QMessageBox.Yes)
            return
        if not ('@' in email and '.' in email):
            QMessageBox.information(self, 'Warning', 'Wrong email format, please input right one!', QMessageBox.Yes)
            self.ledt_email.setFocus()
            return
        pay_load = {'sn':sn, 'username':username, 'email':email}
        self.result = plugins.register(pay_load)
        if self.result['code']==0:
            key = self.result['message']['license']
            self.result = plugins.update_license(key)
            if self.result['code']==0:
                QMessageBox.information(self, 'Success', 'Regist success, enjoy it!', QMessageBox.Yes)
                self.close()
            else:
                QMessageBox.information(self, 'Failed', 'Regist success, but update license faild!', QMessageBox.Yes)
                return
        elif self.result['code']==-1:
            QMessageBox.information(self, 'Failed', 'Regist failed, please check your network!', QMessageBox.Yes)
            return
        else:
            pass
