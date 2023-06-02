# Chosun_Capstone_Design
* 주제 :  dump truck accident prevention through object detection
* https://www.notion.so/GOD-Guardians-Of-Dump-6222bb5ed4034dd0adcd08780fed3054

## 구상도 - 2023/04/07
![image](https://github.com/P-C-Space/MyDataAnalysis02/assets/39722575/2d21f363-3b32-4e09-b1dc-a03e97077e0f)
* 차량 외부
  * 운전석 쪽 측면에 카메라 설치 ( 반대쪽 대각선 아래부분으로 촬영 )
  * 추가센서로 감지 ( 미정 )
* 차량 내부
  * 운전석 핸들 뒤 부분에 라즈베리파이와 부저 설치
  * 객체감지나 센서 값이 전달되면 부저로 알림

## 하드웨어 - 2023/04/14
![image](https://github.com/P-C-Space/MyDataAnalysis02/assets/39722575/3954d56c-e863-4077-953c-f3f0aabe1b2c)
* 라즈베리파이4 (8GB) 스타터 키트

## 웹캠 테스트 - 2023/04/21
* 라즈베리파이 웹캠 연결 확인 isusb
<br> ![image](https://github.com/P-C-Space/MyDataAnalysis02/assets/39722575/12cbb41e-add1-450a-9a0f-002ecad13909)
* 웹캠 테스트
<br> ![image](https://github.com/P-C-Space/MyDataAnalysis02/assets/39722575/514b54c1-a7e1-41d7-aae6-d0e619e92697)

## yolo 테스트 - 2023/04/28
* 라즈베리파이에서 웹캠 사진찍기   

```
fswebcam -r 1280*960 --no-banner image6.jpg
```
<br>![image](https://github.com/P-C-Space/MyDataAnalysis02/assets/39722575/674b7ab3-45cb-413b-891c-454549411c03)

* yolo 테스트
```
./darknet detect cfg/yolov2.cfg yolo.weights data/image5.jpg
```
<br>![image](https://github.com/P-C-Space/MyDataAnalysis02/assets/39722575/2fc6cd63-00f6-42eb-8417-89aa1a0ef7d7)
<br>![image](https://github.com/P-C-Space/MyDataAnalysis02/assets/39722575/1c9f03c7-07d7-4063-ba08-112346cedbb7)
* 10초이상 걸림 -> 다른 인공지능 모델 적용 예정
* person 92% 높은 정확도 보유

## 실시간 객체 인식 구현 - 2023/05/03
* 실시간 객체인식(Object Detection) 구현
YOLO 객체 인식 라이브러리를 사용하여 테스트를 한 결과, 객체 인식을 하는데 시간이 많이 걸리는 문제점이 있음
보다 빠른 인식을 위해 Tensorflow-Lite 라이브러리로 변경

**[웹캠 화면 출력 오류]**

OepnCV 3.x와 달리 OepnCV 4.x 버전에서는 

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, hight) 코드를 추가하여 출력되는 화면의 사이즈를 지정해줌

**[Tensorflow Lite와 파이썬 버전 호환 문제]**

![오류1 JPG](https://github.com/P-C-Space/Chosun_Capstone_Design/assets/90131881/a1ae424f-a353-4c5c-9f2b-98b49e9e96d7)

*ERROR: Could not find version that satisfies the requirement tensorflow*
*ERROR: No matching distribution found for tensorflow*

이러한 오류를 해결하기 위해 하위버전 지정설치 및 콘다(conda)와 virtualenv를 이용하여 Tensorflow 설치 등을 시도하였으나, 여전한 오류 발생

## 오류 분석 및 문제 해결 - 2023/05/10
* 포멧 후 YOLO 재설치
Tensorflow-Lite 라이브러리 설치 시 환경 설정 등 잦은 오류로 YOLO를 다시 사용하기로 하였다.

YOLO 일반 모델 적용 시 4GB 메모리를 가진 GPU(그래픽카드)가 필요. 하지만 라즈베리 파이는 CPU 위주로써 거의 불가능에 가까움

이러한 문제를 해결하기 위해 'YOLO-Tiny' 모델 사용(이 모델은 1G 메모리를 가진 그래픽 카드가 필요함)
라즈베리파이에 사용하기에는 속도가 느리긴 하나, 어느정도 객체인식이 가능하게 됨

-YOLO 가중치 파일 다운로드 링크: [yolov3 weight(가중치) 다운 (velog.io)](https://velog.io/@jeongm/yolov3-weight%EA%B0%80%EC%A4%91%EC%B9%98-%EB%8B%A4%EC%9A%B4)

-YOLO Object Detection 알고리즘 참고 링크(1): [https://bong-sik.tistory.com/16](https://bong-sik.tistory.com/16)

-YOLO Object Detection 알고리즘 참고 링크(2): [https://bong-sik.tistory.com/16](https://deep-eye.tistory.com/6)

## 추가센서 구성 - 2023-05-30
* 아두이노로 초음파 센서 및 적외선 센서로 추가 감지
* 아두이노로 감지한 값을 블루투스로 라즈베리파이에 전송
* 라즈베리파이에서 부저 및 led 출력

### 전체 코드
```
import cv2
import numpy as np
import time # 시간 체크
from gpiozero import Buzzer
from time import sleep
from bluetooth import *
import RPi.GPIO as GPIO

# 블루투스 통신 체크
socket = BluetoothSocket(RFCOMM)
socket.connect(('블루투스 맥주소',1))

# 시간 체크
start_time = 0

# LED
led_pin = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin,GPIO.OUT)

# buzzer setting
buzzer = Buzzer(17)

# webcam signal
VideoSignal = cv2.VideoCapture(0)
VideoSignal.set(cv2.CAP_PROP_FRAME_WIDTH, 120)
VideoSignal.set(cv2.CAP_PROP_FRAME_HEIGHT,100)


# yolo weight file
#YOLO_net = cv2.dnn.readNet("yolov2-tiny.weights","yolov2-tiny.cfg")
YOLO_net = cv2.dnn.readNet("/home/god/yolo/darknet/test/yolov2-tiny.weights","/home/god/yolo/darknet/test/yolov2-tiny.cfg")
# print(YOLO_net)

classes = ["person"]
#classes = []
# with open("coco.names","r") as f:
# 	classes = [line.strip() for line in f.readlines()]
# print(classes)
layer_names = YOLO_net.getLayerNames()
# print(layer_names)
output_layers = [layer_names[i - 1] for i in YOLO_net.getUnconnectedOutLayers()]
# print(output_layers)
colors = np.random.uniform(0,255,size = (len(classes),3 ))

# video brightness calculate
def calculate_brightness(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	brightness = np.mean(gray)
	return brightness

def detect__lighting_condition(brithtness, threshold=60): # threshold
	if brightness < threshold:
		return 'dark'
	else:
		return 'bright'
		
def adjust_brightness(image, lighting_condition):
    if lighting_condition == 'dark':
      alpha = 7.0
      beta = 50.0
    else:
      alpha = 1.0
      beta = 0
    
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted


while True:

	data = socket.recv(1024)
	if(data == b'1'):
		print(data)
		buzzer.on()
		GPIO.output(led_pin,1)
		start_time = time.time()

	print('\a')
	# read the actual frame
	for i in range(2):
		VideoSignal.grab()
	# webcam Frame
	ret, frame = VideoSignal.read()
	h,w,c = frame.shape # height width, channel
	
	# adjusting brightness 
	brightness = calculate_brightness(frame)
	# print(brightness)
	lighting_condition = detect__lighting_condition(brightness)
	# print(lighting_condition)
	frame = adjust_brightness(frame, lighting_condition)
	
	
	# yolo input
	blob = cv2.dnn.blobFromImage(frame, 0.00392, (120,100), (0,0,0), True, crop = False)
	YOLO_net.setInput(blob)
	outs = YOLO_net.forward(output_layers)
	class_ids = []
	confidences = []
	boxes = []
	
	for out in outs:
		for detection in out:
			scores = detection[5:]
			class_id = np.argmax(scores)
			confidence = scores[class_id]

			if confidence > 0.1 and classes and class_id < len(classes) and classes[class_id] == "person":
				# buzzer sound
				buzzer.on()
				start_time = time.time()
				GPIO.output(led_pin,1)
				
				
				# Object detected
				center_x = int(detection[0] * w)
				center_y = int(detection[1] * h)
			
				dw = int(detection[2] * w)
				dh = int(detection[3] * h)
			
				# Rectangle coordinate
				x = int(center_x - dw / 2)
				y = int(center_y - dh / 2)
				boxes.append([x,y,dw,dh])
				confidences.append(float(confidence))
				class_ids.append(class_id)
	
	indexes = cv2.dnn.NMSBoxes(boxes,confidences, 0.45, 0.4) # remove noise
	
	for i in range(len(boxes)):
		if i in indexes:
			x, y, w, h = boxes[i]
			label = str(classes[class_ids[i]])
			score = confidences[i]
			color = colors[0] # person 
			
			cv2.rectangle(frame, (x,y), (x+w,y+h), color,2)
			cv2.putText(frame, label, (x,y+30),cv2.FONT_ITALIC,3, color,3)
	
	# cv2.namedWindow("YOLOv2", cv2.WINDOW_NORMAL)
	cv2.imshow("YOLOv2",frame)
	
	if(start_time != 0):
		if((time.time()-start_time)>=3):
			start_time = 0
			GPIO.output(led_pin,0)
			buzzer.off()

	if cv2.waitKey(20) == ord('q'):
		socket.close()
		GPIO.cleanup()
		break
	
	
```
