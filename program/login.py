import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PIL import Image
import pymysql as my
from main import WindowClass


form_class = uic.loadUiType('./UI/login2.ui')[0]

class LoginClass(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 로그인 페이지 백그라운드 이미지 불러오기
        self.qPixmapVar1 = QPixmap()
        self.qPixmapVar1.load('./UI/artificial-intelligence-3382507_1920.jpg')
        self.label.setPixmap(self.qPixmapVar1)
        
        # 버튼을 누르지않고 Enter키를 누르면 동작하는 함수
        self.lineEdit.returnPressed.connect(self.button1Function)
        self.lineEdit_2.returnPressed.connect(self.button1Function)
        self.btn.clicked.connect(self.button1Function)

    
    def button1Function(self):
        uid = self.lineEdit.text()
        upw = self.lineEdit_2.text()
        result = self.selectLogin(uid, upw)
        if result == None:
            print('로그인 실패')
            self.reset_button()

            self.login_label.setStyleSheet("Color : red")
            self.login_label.setText('아이디 비밀번호를 확인해주세요')
            # 로그인 실패하면 result값 0
            self.LOGIN_RESULT = 0
        elif uid == result['id']:
            # 성공하면 result값 1
            self.USER_NAME = result['user_name']
            self.LOGIN_RESULT = 1
            m = WindowClass()
            l = m.showModal()
            
        else:
            print('로그인 실패')
            self.reset_button()
            # 로그인 실패하면 result값 0
            self.LOGIN_RESULT = 0
        
            
    def reset_button(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        
    
    def selectLogin(self, uid, upw):
        conn = None
        row  = None
        try:
            conn = my.connect(host='localhost',
                port=3306, 
                user='root',
                password='12341234',
                db='vision_checker',
                charset='utf8',
                cursorclass=my.cursors.DictCursor # 결과집합은 튜플이 아니라 딕셔너리이다.
            )
            with conn.cursor() as cs:
                sql = '''
                    SELECT 
                        id, passwd, user_name, depart
                    FROM
                        user
                    WHERE
                        id=%s
                    AND
                        passwd=%s
                    '''
                cs.execute(sql, (uid, upw)) # sql에 파라미터 전달
                row = cs.fetchone()
                #print(row)
        except Exception as e:
            # 로그 처리
            print(e)
        finally:
            if conn:
                conn.close()
            return row

    def showModal(self):
        return super().exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginClass()
    myWindow.show()
    app.exec_()