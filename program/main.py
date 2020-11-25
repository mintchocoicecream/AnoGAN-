import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PIL import Image
import glob
from ctypes import *
import pymysql as my




from PyQt5.QtCore import Qt
#from login import LoginClass
from list import ListClass
#from train import *
import time
import numpy as np
import tensorflow as tf
import train
import shutil
import misc
import config
import tfutil
import dataset



form_class = uic.loadUiType('./UI/main.ui')[0]

class WindowClass(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.result = 0
        
        # 라인에디터 함수 동작 연결
        self.serial_line.textChanged.connect(self.register_button)
        # 버튼과 함수 연결
        self.reset_btn.clicked.connect(self.reset_button)
        self.btn_1.clicked.connect(self.check_button_Function)
        
        self.search_btn.clicked.connect(self.search_button)
        #self.register_btn.clicked.connect(self.register_button)
        # ComboBox에 기능 연결
        self.comboBox.addItem('제네시스G80 핸들')
        self.comboBox.addItem('제네시스G70 핸들')
        self.comboBox.currentIndexChanged.connect(self.comboBoxFunction)

        


    def comboBoxFunction(self):
            print(self.comboBox.currentIndex())
            # 콤보박스 0번쨰 인덱스를 선택하면 제네시스G80 핸들 검사 진행
            if self.comboBox.currentIndex()==0:
                # 첫번째 정상 이미지 띄우기
                self.qPixmapVar1 = QPixmap()
                self.qPixmapVar1.load('OK_1.png')
                self.label_1.setPixmap(self.qPixmapVar1)

                # 두번째 정상 이미지 띄우기
                self.qPixmapVar4 = QPixmap()
                self.qPixmapVar4.load('OK_2.png')
                self.label_4.setPixmap(self.qPixmapVar4)

                self.reset_button()

            # 콤보박스 0번쨰 인덱스를 선택하면 제네시스G70 핸들 검사 진행
            elif self.comboBox.currentIndex()==1:
                # 첫번째 정상 이미지 띄우기
                self.qPixmapVar1 = QPixmap()
                self.qPixmapVar1.load('test_1.png')
                self.label_1.setPixmap(self.qPixmapVar1)

                # 두번째 정상 이미지 띄우기
                self.qPixmapVar4 = QPixmap()
                self.qPixmapVar4.load('OK_2.png')
                self.label_4.setPixmap(self.qPixmapVar4)

                self.reset_button()

                


    def check_button_Function(self):
        path = 'C:/Users/sxxhn/Desktop/VisionCamera/VisionCamera/Vision/Vision/bin/x64/Release/ImageSave/'
        
        # 카메라 실행파일 실행하여 사진 찍기
        os.system(f'C:/Users/sxxhn/Desktop/VisionCamera/VisionCamera/Vision/Vision/bin/x64/Release/Vision.exe')
        
        # 카메라로 찍은 사진 저장된 폴더에서 제일 최근 사진 불러오기
        tmp_path = glob.glob(f'{path}*.bmp')
        files = list()
        for p in tmp_path:
            files.append(int(p[-18:-4]))
        files.sort(reverse=True)
        
        # 원본사진 불러와서 grayscale로 변환
        img = Image.open(f'{path}CAM1_{str(files[0])}.bmp').convert("L")
        
        # 크롭한 후 img1 저장될 경로
        cg_path1 = f'C:/Users/sxxhn/Desktop/finalproject/main/datasets/mnist_2_0.0/validation/anomaly/'
        # 크롭한 후 img2 저장될 경로
        cg_path2 = f'C:/Users/sxxhn/Desktop/finalproject/main/datasets/mnist_2_0.0/validation/anomaly2/'
        
        # 원본사진에서 img1과 img2 크롭
        crop_img1 = img.crop([454, 1095, 582, 1223])
        crop_img2 = img.crop([738, 1094, 866, 1222])
        
        # 크롭한 이미지 저장
        crop_img1.save(f'{cg_path1}{str(files[0])}.png')
        crop_img2.save(f'{cg_path2}{str(files[0])}.png')
        
        # 촬영한 첫번째 이미지 띄우기 
        label_1_path = f'{cg_path1}{str(files[0])}.png'
        self.qPixmapVar1 = QPixmap()
        self.qPixmapVar1.load(label_1_path)
        self.label_1.setPixmap(self.qPixmapVar1)
        
        # 촬영한 두번째 이미지 띄우기 
        label_4_path = f'{cg_path2}{str(files[0])}.png'
        self.qPixmapVar4 = QPixmap()
        self.qPixmapVar4.load(label_4_path)
        self.label_4.setPixmap(self.qPixmapVar4)

        # 첫 번째 이미지 anoGan 모델에서 예측
        self.predictModel("img1")
        
        # 저장된 테스트 결과 저장 폴더 경로
        result_path = 'C:/Users/sxxhn/Desktop/finalproject/main/datasets/mnist_2_0.0/validation/anomaly/test_result'
        result_output = glob.glob(f'{result_path}/*')
        
        # anomaly detection img 이동
        move_path = 'C:/Users/sxxhn/Desktop/finalproject/main/result_img/img1'
        file_name1 = result_output[1][93:]
        shutil.move(f'{result_path}/{file_name1}', f'{move_path}/{file_name1}')
        
        # 필요없는 npy파일 삭제
        os.remove(result_output[2])

        # 첫 번째 이미지 파일 이름에서 anomaly score 가져오기
        img1_score = result_output[1][102:111]
        print(img1_score)
        # 카메라로 찍은 이미지 이동
        move1_path = 'C:/Users/sxxhn/Desktop/finalproject/main/shot_img/img1'
        shot_img1_path = f'{move1_path}/{str(files[0])}.png'
        shutil.move(label_1_path, shot_img1_path)
        
        # generator가 생성한 이미지 이동
        gen_path1 = 'C:/Users/sxxhn/Desktop/finalproject/main/generator_img/img1'
        mov_path=f'{gen_path1}/{result_output[0][93:]}'
        shutil.move(result_output[0], mov_path)
        
        # img1 생성한 이미지 띄우기
        self.qPixmapVar2 = QPixmap()
        self.qPixmapVar2.load(mov_path)
        self.label_2.setPixmap(self.qPixmapVar2)

        # 두 번째 이미지 예측
        self.predictModel("img2")
        # img2 결과 이미지 경로 파일 불러오기
        result_path = 'C:/Users/sxxhn/Desktop/finalproject/main/datasets/mnist_2_0.0/validation/anomaly2/test_result'
        result_output = glob.glob(f'{result_path}/*')
        # 이동시킬 경로
        move_path = 'C:/Users/sxxhn/Desktop/finalproject/main/result_img/img2'
        file_name2 = result_output[1][93:]
        shutil.move(f'{result_path}/{file_name2}', f'{move_path}/{file_name2}')
        # npy파일 삭제
        os.remove(result_output[2])

        # 두 번째 이미지 파일 이름에서 anomaly score 가져오기
        img2_score = result_output[1][103:112]
        print(img2_score)

        # 카메라로 찍은 img2 이동
        move1_path = 'C:/Users/sxxhn/Desktop/finalproject/main/shot_img/img2'
        shot_img2_path = f'{move1_path}/{str(files[0])}.png'
        shutil.move(label_4_path, shot_img2_path)

        # generator가 생성한 img2 이동
        gen_path2 = 'C:/Users/sxxhn/Desktop/finalproject/main/generator_img/img2'
        mov_path1=f'{gen_path2}/{result_output[0][94:]}'
        shutil.move(result_output[0], mov_path1 )

        # 두번째 정상 이미지 띄우기
        self.qPixmapVar5 = QPixmap()
        self.qPixmapVar5.load(mov_path1)
        self.label_5.setPixmap(self.qPixmapVar5)

        # 만약 img1_score의 값이 1400이하이고 img2_score의 1700이하이면 PASS, 아니면 FAIL
        # 만약 PASS이면 label_11의 배경색상을 초록색으로 변경
        # FAIL이면 배경색상을 빨간색으로 변경
        if float(img1_score) <=1400. and float(img2_score) <= 1700:
            final_result = 'PASS'
            self.label_11.setStyleSheet("QLabel { background-color : green; color:white;}")

        else:
            final_result='FAIL'
            self.label_11.setStyleSheet("QLabel { background-color : red; color:white;}")
        
        # 결과(label_11)의 텍스트를 결과값으로 변경
        self.label_11.setText(final_result)
        
        # 모든진행사항이 다 진행되고나서 결과값들 DB에 저장
        self.InsertImageData(self.serial_line.text(), shot_img1_path, shot_img2_path, final_result, img1_score, img2_score)

        # 첫 번째 이미지 anomaly detection 띄우기
        label_3_path = f'C:/Users/sxxhn/Desktop/finalproject/main/result_img/img1/{file_name1}'
        self.qPixmapVar3 = QPixmap()
        self.qPixmapVar3.load(label_3_path)
        self.label_3.setPixmap(self.qPixmapVar3)
        
        # 두 번째 이미지 anomaly detection 띄우기
        label_6_path = f'C:/Users/sxxhn/Desktop/finalproject/main/result_img/img2/{file_name2}'
        self.qPixmapVar6 = QPixmap()
        self.qPixmapVar6.load(label_6_path)
        self.label_6.setPixmap(self.qPixmapVar6)
    
    # anoGAN실행 함수 파라미터값으로 img의 종류를 넣어주면 img에 맞게 돌아감
    def predictModel(self, img):
        if img == 'img1':
            misc.init_output_logging()
            np.random.seed(config.random_seed)
            print('Initializing TensorFlow...')
            os.environ.update(config.env)
            tfutil.init_tf(config.tf_config)
            print('Running %s()...' % config.train['func'])
            tfutil.call_func_by_name(**config.train)
            print('Exiting...')
            print("img1 end@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        else:
            misc.init_output_logging()
            np.random.seed(config.random_seed)
            print('Initializing TensorFlow...')
            os.environ.update(config.env)
            tfutil.init_tf(config.tf_config)
            print('Running %s()...' % config.train['func'])
            tfutil.call_func_by_name(**config.train1)
            print('Exiting...')

    # 결과값들을 DB에 저장하는 함수
    def InsertImageData(self, serial_no, img_path_1, img_path_2, result, img1_score, img2_score):
        try:
            conn = my.connect(host='localhost',
                port=3306, 
                user='root',
                password='12341234',
                db='vision_checker',
                charset='utf8',
                
            )
            with conn.cursor() as cs:
                sql = '''
                    INSERT INTO 
                        img
                    VALUES
                        (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    '''
                cs.execute(sql, (serial_no, img_path_1, img_path_2, result, img1_score, img2_score)) # sql에 파라미터 전달
                conn.commit()
                row = cs.fetchone()
                print(row)
        except Exception as e:
            # 로그 처리
            print(e)
        finally:
            if conn:
                conn.close()
            return row
        pass
    
    # reset 버튼을 누르면 clear해주는 함수
    def reset_button(self):
        self.label_2.clear()
        self.label_5.clear()
        self.label_3.clear()
        self.label_6.clear()
        self.label_11.setText('결과')
        self.serial_line.clear()
        self.serial_label.clear()
        
    '''
    def LoginButtonClicked(self):
        if self.result == 1:
            self.loginButton.setText('로그인')
            self.user_label.clear()
            self.result = 0
        else:
            win = LoginClass()
            r = win.showModal()
            if r:
                self.result = win.LOGIN_RESULT
                self.user_name = win.USER_NAME
            if self.result==1:
                self.loginButton.setText('로그아웃')
                self.user_label.setText(self.user_name+"님")
                self.user_label.setAlignment(Qt.AlignCenter)
    '''
    # 검색버튼을 누르면 검색창 띄워줌
    def search_button(self):
        list = ListClass()
        l = list.showModal()
        
    # 시리얼 번호 입력하면 시리얼번호가 찍힘
    def register_button(self):
        self.serial_no = self.serial_line.text()
        self.serial_label.setText('시리얼번호: ' + self.serial_no)
        self.serial_label.setAlignment(Qt.AlignCenter)
            
    def showModal(self):
        return super().exec_()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
    