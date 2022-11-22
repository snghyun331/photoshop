import sys
import numpy as np
from turtle import window_height
import cv2
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton,
    QFileDialog
    )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Photoshop")

        # 메뉴바 만들기
        self.menu = self.menuBar()   # 변수 생성
        self.menu_file = self.menu.addMenu("파일")    # 변수 생성
        exit = QAction("나가기", self, triggered = qApp.quit)
        self.menu_file.addAction(exit)

        # 메인화면 레이아웃
        main_layout = QHBoxLayout()

        # 사이드바 메뉴버튼
        sidebar = QVBoxLayout()
        button1 = QPushButton("이미지 열기")
        button2 = QPushButton("좌우반전")
        button3 = QPushButton("이미지 흑백")
        button4 = QPushButton("렌즈왜곡")
        button5 = QPushButton("얼굴 모자이크")
        button6 = QPushButton("새로고침")
        
        button1.clicked.connect(self.show_file_dialog)   # 이전버전은 clicked X, triggered 0
        button2.clicked.connect(self.flip_image)
        button3.clicked.connect(self.make_gray)
        button4.clicked.connect(self.lens_distortion)
        button5.clicked.connect(self.face_mosaic)
        button6.clicked.connect(self.clear_label)
        
        sidebar.addWidget(button1)
        sidebar.addWidget(button2)
        sidebar.addWidget(button3)
        sidebar.addWidget(button4)
        sidebar.addWidget(button5)
        sidebar.addWidget(button6)

        main_layout.addLayout(sidebar)

        ## 사이드바 메뉴버튼 사이즈 조정
        self.label1 = QLabel(self)
        self.label1.setFixedSize(640,480)
        main_layout.addWidget(self.label1)
        ### 이미지 배치 칸 늘이기? 
        self.label2 = QLabel(self)
        self.label2.setFixedSize(640,480)
        main_layout.addWidget(self.label2)
        

        # 창 넓히기
        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    # 이미지 열기
    def show_file_dialog(self):
        ## 경로 창 만들기
        file_path = QFileDialog.getOpenFileName(self, "이미지 열기", "./")  # 경로: 현재경로
        print(file_path)
        ## 이미지 갖다 붙이기
        self.image = cv2.imread(file_path[0])   # 튜플형태, [0]: 이미지명
        
        h, w = self.image.shape[:2]
        if (h>=800) or (w>=800):
            self.image = cv2.resize(self.image, (w//2, h//2))
            
        height, weight, _ = self.image.shape   
        bytese_per_line = 3 * weight
        
        
        image = QImage(
            self.image.data, weight,height, bytese_per_line, QImage.Format_RGB888
        ).rgbSwapped()

        pixmap = QPixmap(image)
        self.label1.setPixmap(pixmap)

    # 좌우반전
    def flip_image(self):
        image = cv2.flip(self.image, 1)    # 1: 좌우반전
        height, weight, _ = image.shape   
        bytese_per_line = 3 * weight
        image = QImage(
            image.data, weight,height, bytese_per_line, QImage.Format_RGB888
        ).rgbSwapped()

        pixmap = QPixmap(image)
        self.label2.setPixmap(pixmap)

    # 이미지 흑백
    def make_gray(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        image1 = np.expand_dims(gray, axis = -1) * np.ones((1,1,3))
        image2 = image1.astype(np.uint8)
        height, weight, _ = image2.shape   
        bytese_per_line = 3 * weight
        image3 = QImage(
            image2.data, weight, height, bytese_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        
        pixmap = QPixmap(image3)
        self.label2.setPixmap(pixmap)
        
    
    # 렌즈 왜곡
    def lens_distortion(self):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        h, w = image.shape[:2]

        exp = 2  # 볼록지수 1.1 ~, 오목지수 0.1 ~ 1.0
        scale = 1
        mapy, mapx = np.indices((h, w), dtype = np.float32)

        mapx = 2 * mapx / (w - 1) - 1
        mapy = 2 * mapy / (h - 1) - 1
        
        r, theta = cv2.cartToPolar(mapx, mapy)
        r[r < scale] = r[r < scale] ** exp
        
        mapx, mapy = cv2.polarToCart(r, theta)
        mapx = ((mapx + 1) * w - 1) / 2
        mapy = ((mapy + 1) * h - 1) / 2
        
        distorted = cv2.remap(image, mapx, mapy, cv2.INTER_LINEAR)
        distorted2 = cv2.cvtColor(distorted, cv2.COLOR_BGR2RGB)
        
        height, weight, _ = distorted2.shape   
        bytese_per_line = 3 * weight
        image3 = QImage(
            distorted2.data, weight, height, bytese_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        
        pixmap = QPixmap(image3)
        self.label2.setPixmap(pixmap)
               
    # 얼굴 모자이크    
    def face_mosaic(self):
        img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        
        xml = 'opencv/haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(xml)
        faces = face_cascade.detectMultiScale(img_gray, 1.2, 5)
        ratio = 0.1
        for (x,y,w,h) in faces:
            small = cv2.resize(img[y: y + h, x: x + w], None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
            img[y: y + h, x: x + w] = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
            
        height, weight, _ = img.shape   
        bytese_per_line = 3 * weight
        
        image3 = QImage(
            img.data, weight, height, bytese_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        
        pixmap = QPixmap(image3)
        self.label2.setPixmap(pixmap)
        
        
        
    # 새로고침
    def clear_label(self):
        self.label2.clear()

if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())   # sys : 내장 메모리

        
        
        
        
    # https://velog.io/@bangsy/Python-OpenCV1
    # https://bskyvision.com/entry/pyside-keepaspectratio
       


