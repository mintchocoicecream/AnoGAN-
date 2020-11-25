import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pymysql as my

form_class = uic.loadUiType("./UI/next_alert.ui")[0]
# 검색페이지에서 다음버튼 눌렀을때 더 이상 데이터가 없으면 띄워주는 창
class NextAlertClass(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
    def showModal(self):
        return super().exec_()