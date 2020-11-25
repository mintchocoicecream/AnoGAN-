import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pymysql as my
from next_alert import NextAlertClass
from previous_alert import PreviousAlertClass

form_class = uic.loadUiType("./UI/list.ui")[0]

class ListClass(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.page = 1
        data = self.SelectDataAll()
        keys = list(data[0].keys())
        self.tableWidget.setRowCount(len(data))
        for row in range(len(data)):
            key=0
            for col in range(len(data[0])):
                qTableWidgetItemVar = QTableWidgetItem(str(data[row][keys[key]]))
                self.tableWidget.setItem(row, col, qTableWidgetItemVar)
                key+=1
        
        #self.tableWidget_Test.cellChanged.connect(self.cellChangeFunc)
        self.next_btn.clicked.connect(self.nextButton)
        self.previous_btn.clicked.connect(self.previousButton)
        self.search_btn.clicked.connect(self.searchButton)

    # 검색버튼 눌렀을때 동작하는 함수
    # 시리얼번호로 검색
    def searchButton(self):
        # 입력창에서 입력된 시리얼번호를 불러옴
        text = self.search_line.text()
        # 입력되어있는 아이템값들을 없애준다.
        self.tableWidget.clearContents()
        # db에 연결
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
                    SELECT * 
                    FROM IMG
                    WHERE serial_no=%s
                    ORDER BY check_date DESC
                    '''
                cs.execute(sql, (text)) # sql에 파라미터(시리얼번호) 전달
                row = cs.fetchall()
                print(row)
        except Exception as e:
            # 로그 처리
            print(e)
        finally:
            if conn:
                conn.close()

            data = row
            # SQL문 결과값으로 TABLE에 아이템 채우기
            for row in range(len(data)):
                key1 = 0
                keys = list(data[0].keys())
                for col in range(len(data[0])):
                    qTableWidgetItemVar = QTableWidgetItem(str(data[row][keys[key1]]))
                    self.tableWidget.setItem(row, col, qTableWidgetItemVar)
                    key1+=1
            return row
    
    # 다음버튼 눌렀을때 동작
    def nextButton(self):
        # 1페이지당 20개의 아이템을 보여줌
        self.page+=20
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
                    SELECT serial_no, img_path_1, img_path_2, result, img1_score, img2_score, check_date
                    FROM
                        (SELECT serial_no, 
                            img_path_1, 
                            img_path_2, 
                            result, 
                            img1_score,
                            img2_score,
                            check_date,
                            @rownum := @rownum+1 AS RNUM
                        FROM img, (SELECT @rownum :=0) AS R
                        ORDER BY check_date) AS A
                    WHERE RNUM BETWEEN %s AND %s
                    '''
                cs.execute(sql, (self.page, self.page+19)) # sql에 파라미터(0~20개의 결과를 불러오기위해) 전달
                row = cs.fetchall()
                print(type(row))
                
        except Exception as e:
            # 로그 처리
            print(e)
        finally:
            if conn:
                conn.close()
            
            # 만약 결과값이 없으면 맨 마지막 페이지(더 이상 페이지가 없다) 그러면 마지막페이지라는 경고창을 띄워준다.
            if not row :
                win = NextAlertClass()
                r = win.showModal()
                self.page-=20
                return 1
            data = row
            self.tableWidget.clearContents()
            for row in range(len(data)):
                key1 = 0
                keys = list(data[0].keys())
                for col in range(len(data[0])):
                    qTableWidgetItemVar = QTableWidgetItem(str(data[row][keys[key1]]))
                    self.tableWidget.setItem(row, col, qTableWidgetItemVar)
                    key1+=1
            print(self.page, self.page+9)
            return row

    # 이전버튼 눌렀을때 동작
    def previousButton(self):
        
        self.page-=20
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
                    SELECT serial_no, img_path_1, img_path_2, img1_score, img2_score, score, check_date
                    FROM
                        (SELECT serial_no, 
                            img_path_1, 
                            img_path_2, 
                            result, 
                            img1_score, 
                            img2_score,
                            check_date,
                            @rownum := @rownum+1 AS RNUM
                        FROM img, (SELECT @rownum :=0) AS R
                        ORDER BY check_date) AS A
                    WHERE RNUM BETWEEN %s AND %s
                    '''
                cs.execute(sql, (self.page, self.page+19)) # sql에 파라미터 전달
                row = cs.fetchall()
                print(row)
        except Exception as e:
            # 로그 처리
            print(e)
        finally:
            if conn:
                conn.close()
                
            if not row :
                win = PreviousAlertClass()
                r = win.showModal()
                self.page+=20
                return 1
            data = row
            self.tableWidget.clearContents()
            for row in range(len(data)):
                key1 = 0
                keys = list(data[0].keys())
                for col in range(len(data[0])):
                    qTableWidgetItemVar = QTableWidgetItem(str(data[row][keys[key1]]))
                    self.tableWidget.setItem(row, col, qTableWidgetItemVar)
                    key1+=1
            print(self.page, self.page+9)
            return row

    def cellChangeFunc(self) :
        pass
    
    # 처음 MAIN 페이지에서 검색버튼을 눌러서 창을 띄울때 아이템들을 출력하는 함수
    def SelectDataAll(self):
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
                # 최근일자 기준으로 정렬
                sql = '''
                    SELECT serial_no, img_path_1, img_path_2, result, img1_score, img2_score, check_date
                    FROM
                        (SELECT serial_no, 
                            img_path_1, 
                            img_path_2, 
                            result, 
                            img1_score, 
                            img2_score,
                            check_date,
                            @rownum := @rownum+1 AS RNUM
                        FROM img, (SELECT @rownum :=0) AS R
                        ORDER BY check_date) AS A
                    WHERE RNUM BETWEEN 1 AND 20
                    '''
                cs.execute(sql) # sql에 파라미터 전달
                row = cs.fetchall()
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
        
if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = ListClass()
    myWindow.show()
    app.exec_()