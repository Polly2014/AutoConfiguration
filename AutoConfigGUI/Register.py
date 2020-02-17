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
        result = plugins.register(pay_load)
        if result['code']==0:
            QMessageBox.information(self, 'Success', 'Regist scucess, enjoy it!', QMessageBox.Yes)
            self.close()
        elif result['code']==-1:
            QMessageBox.information(self, 'Failed', 'Regist failed, please check your network!', QMessageBox.Yes)
            self.close()
            return
        else:
            pass
