# Chosun_Capstone_Design
* 주제 :  dump truck accident prevention through object detection

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

# ERROR
