import sys
import numpy as np
from turtle import window_height
import cv2
from PySide6.QtGui import QAction, QImage, QPixmap, QIcon, QPainter, QPen, QColor
from PySide6.QtCore import QSize, Qt, QPoint
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton,
    QFileDialog
    )

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Photoshop")
        self.setWindowIcon(QIcon('title.png'))
        self.setGeometry(300,150,800,750)
        
        
        # 메뉴바 만들기
        filetoolbar = self.addToolBar("File")
        self.menu = self.menuBar()   # 변수 생성
        self.menu_file = self.menu.addMenu("파일")    # 변수 생성
        save = QAction(QIcon("save.png"), "이미지 저장", self, triggered = self.save_image)
        exit = QAction(QIcon("exit.png"),"나가기", self, triggered = qApp.quit)
        filetoolbar.addAction(save)
        filetoolbar.addAction(exit)
        self.menu_file.addAction(save)
        self.menu_file.addAction(exit)
        
        
        # 메인화면 레이아웃
        main_layout = QHBoxLayout()


        # 사이드바 기능 버튼
        sidebar = QVBoxLayout()
        button1 = QPushButton("이미지 열기")
        button2 = QPushButton("좌우반전")
        button3 = QPushButton("이미지 흑백")
        button4 = QPushButton("Barrel 왜곡")
        button5 = QPushButton("얼굴 모자이크")
        button6 = QPushButton("그리기")
        button7 = QPushButton("새로고침")
        
        button1.clicked.connect(self.show_file_dialog)   # 이전버전은 clicked X, triggered 0
        button2.clicked.connect(self.flip_image)
        button3.clicked.connect(self.make_gray)
        button4.clicked.connect(self.lens_distortion)
        button5.clicked.connect(self.face_mosaic)
        button6.clicked.connect(self.show_drawed_image)
        button7.clicked.connect(self.clear_label)
        
        sidebar.addWidget(button1)
        sidebar.addWidget(button2)
        sidebar.addWidget(button3)
        sidebar.addWidget(button4)
        sidebar.addWidget(button5)
        sidebar.addWidget(button6)
        sidebar.addWidget(button7)

        main_layout.addLayout(sidebar)


        # 첫번째 이미지 라벨 편집
        self.label1 = QLabel(self)
        self.label1.setFixedSize(600,600)
        self.label1.setStyleSheet("border-style: dashed;"
                                  "border-width: 3px;"
                                  "border-color: #1E90FF")
        main_layout.addWidget(self.label1)
        
        
        # 두번째 이미지 라벨 편집
        self.label2 = QLabel(self)
        self.label2.setFixedSize(600,600)
        self.label2.setStyleSheet("border-style: dashed;"
                                  "border-width: 3px;"
                                  "border-color: #FA8072")
        main_layout.addWidget(self.label2)
        

        # 위젯 배치
        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)



    # 이미지 열기 기능
    def show_file_dialog(self):
        ## 경로 창 만들기
        self.file_path = QFileDialog.getOpenFileName(self, "이미지 열기", "./")  # 경로: 현재경로
        
        ## 이미지 갖다 붙이기
        self.image = cv2.imread(self.file_path[0])   # 튜플형태, [0]: 이미지명
        self.image_copy = self.image 
        height, weight, _ = self.image_copy.shape   
        bytese_per_line = 3 * weight
        
        image = QImage(
            self.image_copy.data, weight,height, bytese_per_line, QImage.Format_RGB888
        ).rgbSwapped()

        pixmap = QPixmap(image)
        pixmap_scaled = pixmap.scaled(QSize(600,600), aspectMode=Qt.KeepAspectRatio)
        self.label1.setPixmap(pixmap_scaled)



    # 좌우반전 기능
    def flip_image(self):
        self.image_copy = cv2.flip(self.image_copy, 1)    # 1: 좌우반전
        height, weight, _ = self.image_copy.shape   
        bytese_per_line = 3 * weight
        image = QImage(
            self.image_copy.data, weight,height, bytese_per_line, QImage.Format_RGB888
        ).rgbSwapped()

        pixmap = QPixmap(image)
        pixmap_scaled = pixmap.scaled(QSize(600,600), aspectMode=Qt.KeepAspectRatio)
        self.label2.setPixmap(pixmap_scaled)



    # 이미지 흑백 변환 기능
    def make_gray(self):
        self.image_copy = cv2.cvtColor(self.image_copy, cv2.COLOR_BGR2GRAY)
        self.image_copy = np.expand_dims(self.image_copy, axis = -1) * np.ones((1,1,3))
        self.image_copy = self.image_copy.astype(np.uint8)
        height, weight, _ = self.image_copy.shape   
        bytese_per_line = 3 * weight
        image = QImage(
            self.image_copy.data, weight, height, bytese_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        
        pixmap = QPixmap(image)
        pixmap_scaled = pixmap.scaled(QSize(600,600), aspectMode=Qt.KeepAspectRatio)
        self.label2.setPixmap(pixmap_scaled)
        
    
    
    # Barrel Distortion 기능
    def lens_distortion(self):
        image = cv2.cvtColor(self.image_copy, cv2.COLOR_BGR2RGB)
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
        self.image_copy = distorted2
        
        pixmap = QPixmap(image3)
        pixmap_scaled = pixmap.scaled(QSize(600,600), aspectMode=Qt.KeepAspectRatio)
        self.label2.setPixmap(pixmap_scaled)
               
               
               
    # 얼굴 모자이크 기능
    def face_mosaic(self):
        img = cv2.cvtColor(self.image_copy, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        xml = 'opencv/haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(xml)
        faces = face_cascade.detectMultiScale(img_gray, 1.1, 5)
        ratio = 0.05
        for (x,y,w,h) in faces:
            small = cv2.resize(img[y: y + h, x: x + w], None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
            img[y: y + h, x: x + w] = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
            
        height, weight, _ = img.shape   
        bytese_per_line = 3 * weight
        
        image3 = QImage(
            img.data, weight, height, bytese_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        
        self.image_copy = img
        
        pixmap = QPixmap(image3)
        pixmap_scaled = pixmap.scaled(QSize(600,600), aspectMode=Qt.KeepAspectRatio)
        self.label2.setPixmap(pixmap_scaled)
    
    
    # 이미지에 그림 그리기 기능
    def onChange(self, param):
        self.r = int(cv2.getTrackbarPos('R','draw'))
        self.g = int(cv2.getTrackbarPos('G','draw'))
        self.b = int(cv2.getTrackbarPos('B','draw'))
        self.s = int(cv2.getTrackbarPos('Brush Size','draw'))
    
    px = -1
    py = -1    
    def draw_mouse(self,event, x, y, flags, params):
        
        global px, py
        if event == cv2.EVENT_LBUTTONDOWN:    # 마우스 왼쪽이 눌러지면 실행
            px, py = x, y                     # 마우스를 눌렀을 때 좌표 저장, 띄워진 영상에서의 좌측
        elif event == cv2.EVENT_MOUSEMOVE:    # 마우스가 움직일 때 발생
            if flags & cv2.EVENT_FLAG_LBUTTON:     # == 를 쓰면 다른 키도 입력되었을 때 작동안하므로 &(and)사용
                cv2.line(self.image_copy, (px, py), (x,y), (self.r, self.g, self.b), self.s, cv2.LINE_AA)   # circle은 끊기므로 line으로..
                cv2.imshow("draw",self.image_copy)
                px, py = x, y
        
        
    def show_drawed_image(self):
        h, w = self.image_copy.shape[:2]
        if (h>=650) or (w>=650):
            self.image_copy = cv2.resize(self.image_copy, (int(w//1.5), int(h//1.5)))
        elif (650<h<=950) or (650<h<=950):
            self.image_copy = cv2.resize(self.image_copy, (int(w//2), int(h//2)))
        elif (950<h<=1500) or (950<h<=1500):
            self.image_copy = cv2.resize(self.image_copy, (int(w//3), int(h//3)))
        elif (h<300) or (w<300):
            self.image_copy = cv2.resize(self.image_copy, (int(w*1.5), int(h*1.5)))
        
        
        height, weight, _ = self.image_copy.shape
        bytese_per_line = 3 * weight
        
        
        cv2.namedWindow("draw", flags = cv2.WINDOW_NORMAL)
        if (height > weight):
            cv2.resizeWindow("draw", width = int(weight), height = int(height*1.2))
        elif (height < weight):
            cv2.resizeWindow("draw", width = int(weight), height = int(height*1.6))
        
        cv2.moveWindow('draw', 120, 30)  
        cv2.createTrackbar('R', 'draw', 1, 255, self.onChange)
        cv2.createTrackbar('G', 'draw', 1, 255, self.onChange)
        cv2.createTrackbar('B', 'draw', 1, 255, self.onChange)
        cv2.createTrackbar('Brush Size', 'draw', 1, 20, self.onChange)

        cv2.setMouseCallback("draw", self.draw_mouse, self.image_copy)  
        cv2.imshow("draw",self.image_copy)
        cv2.waitKey()
        cv2.destroyAllWindows()
    
        image3 = QImage(
            self.image_copy.data, weight, height, bytese_per_line, QImage.Format_RGB888
        ).rgbSwapped()
        
        pixmap = QPixmap(image3)
        pixmap_scaled = pixmap.scaled(QSize(600,600), aspectMode=Qt.KeepAspectRatio)
        self.label2.setPixmap(pixmap_scaled)

        

    # 새로고침
    def clear_label(self):
        self.label2.clear()
        self.image_copy = cv2.imread(self.file_path[0])   # 튜플형태, [0]: 이미지명
        
        

    # 이미지 저장
    def save_image(self):
        image_saver = self.label2.pixmap()
        image_saver.save("SavedImage.jpg")
    
        
            
if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())   # sys : 내장 메모리
    
       

