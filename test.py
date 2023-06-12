import cv2
import numpy as np
import time
from gpiozero import Buzzer
from time import sleep
from bluetooth import *
import RPi.GPIO as GPIO


sleep(10);

socket = BluetoothSocket(RFCOMM)
socket.connect(('98:DA:60:05:33:34',1))
start_time = 0

led_pin = 18
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)


# buzzer setting
buzzer = Buzzer(17)

# webcam signal
VideoSignal = cv2.VideoCapture(0)
VideoSignal.set(cv2.CAP_PROP_FRAME_WIDTH, 360)
VideoSignal.set(cv2.CAP_PROP_FRAME_HEIGHT,240)


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

def detect__lighting_condition(brithtness, threshold=10): # threshold
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
	# frame = cv2.flip(frame,0)
	
	h,w,c = frame.shape # height width, channel
	
	# adjusting brightness 
	brightness = calculate_brightness(frame)
	# print(brightness)
	lighting_condition = detect__lighting_condition(brightness)
	# print(lighting_condition)
	frame = adjust_brightness(frame, lighting_condition)
	
	
	# yolo input
	blob = cv2.dnn.blobFromImage(frame, 0.00392, (360,240), (0,0,0), True, crop = False)
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
		if((time.time() - start_time) >= 3):
			start_time = 0
			GPIO.output(led_pin,0)
			buzzer.off()
	
	if cv2.waitKey(20) == ord('q'):
		socket.close()
		GPIO.cleanup()
		break
	