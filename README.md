# Photoshop
school project (Computer Vision1)

## main tech list
* 이미지 열기 기능
* 좌우반전 기능
* 이미지 흑백 전환 기능
* 렌즈왜곡 (Bareel Distortion) 기능
* 얼굴 모자이크 기능
* 이미지에 그림 그리기 기능
* 새로고침

## tech_discription
* **이미지 열기 기능**
: 포토샵할 이미지를 불러온다
→` QFileDialog.getOpenFileName` 모듈로 이미지를 불러온다    
→ `cv2.imread`로 이미지를 읽은 후 첫번째 이미지 라벨에 불러온 원본 이미지를 출력한다. 이때, 나중에 있을 새로고침을 위해 `self.image`를 `self.image_copy` 변수에 복사한다.    
→ 원본 이미지를 첫번째 이미지 라벨에 출력하는 과정에서, 출력하는 이미지의 크기를 원본 크기와 다르게 해주기 위해 QPixmap클래스의 scaled 메소드를 활용한다. 이미지 비율을 해치지 않기 위해 이미지의 종횡비(aspect ratio)을 유지해주는 `Qt.KeepAspectRatio`로 설정한다 (사이즈: 600,600)    

* **좌우반전 기능**
: 이미지를 좌우반전시킨다   
→ `cv2.flip`을 활용하여 좌우반전 기능을 구현한다. `cv2.filp(self.image, 1)`에서 "1"은 좌우반전을 의미한다
→ 이 기능 역시, QPixmap클래스의 scaled 메소드를 활용하여 이미지 비율을 해치지 않도록 한다   

* **이미지 흑백 전환 기능**
: 컬러 이미지를 흑백 이미지로 전환시킨다   
→ `cv2.cvtColor`에서 두번째 인자에 `cv2.COLOR_BGR2GRAY`를 활용하여 RGB 원본 이미지를 흑백으로 전환시킨다.   
→ 이 기능 역시, QPixmap클래스의 scaled 메소드를 활용하여 이미지 비율을 해치지 않도록 한다  

* **렌즈왜곡(Barrel Distortion)**
: 이미지를 왜곡 보정한다    
→ Pincushion Distortion과 Barrel Distortion 중, Barrel Distortion을 적용한다.  
→ 이 기능 역시, QPixmap클래스의 scaled 메소드를 활용하여 이미지 비율을 해치지 않도록 한다  

* **얼굴 모자이크 기능**
: 얼굴만 탐지하여 모자이크를 처리한다   
→ `cv2.CascadeClassifier()` 메소드를 활용하고, detectMultiScale 모듈로 모자이크 스케일을 조정한다.    

* **이미지에 그림 그리기 기능**
: "그리기" 버튼을 클릭하면 draw 이름의 새 창이 하나 뜨고, 브러쉬(brush)의 굵기, 색깔을 조정하여 painting을 할 수 있다.    
→ cv2에서 제공하는 Trackbar로 브러쉬 굵기, 브러쉬 색깔 RGB을 조절할 수 있다.   
→ 작동 순서: `show_drawed_image()` → `draw_mouse()`   
→ RGB설정 초기값(default)은 R, G, B 모두 1로 설정한다.    
→ brush size는 숫자가 클수록 굵기가 굵어진다.    

* **새로고침**
: 새로고침을 하면 처음 이미지를 불러왔을 때로 되돌아간다.   
→ 두번째 이미지를 clear 시킨다.

## 그 외 기능
1. 나가기 : "나가기"를 누르면 창이 닫힌다.
2. 이미지 저장 : "이미지 저장"을 누르면 "SavedImage.jpg" 이름으로 같은 경로에 저장된다.

