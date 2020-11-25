import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pymysql as my

form_class = uic.loadUiType("./UI/previous_alert.ui")[0]
# 검색페이지에서 이전버튼 눌렀을때 더 이상 데이터가 없으면 띄워주는 창
class PreviousAlertClass(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
    def showModal(self):
        return super().exec_()