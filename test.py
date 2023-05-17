import cv2
import numpy as np

# webcam signal
VideoSignal = cv2.VideoCapture(0)
# VideoSignal.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# VideoSignal.set(cv2.CAP_PROP_FRAME_HEIGHT,240)

# yolo weight file
YOLO_net = cv2.dnn.readNet("yolov2-tiny.weights","yolov2-tiny.cfg")
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

while True:
	# read the actual frame
	for i in range(2):
		VideoSignal.grab()
	# webcam Frame
	ret, frame = VideoSignal.read()
	h,w,c = frame.shape # height width, channel
	
	# yolo input
	blob = cv2.dnn.blobFromImage(frame, 0.00392, (320,240), (0,0,0), True, crop = False)
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
	
	cv2.imshow("YOLOv2",frame)
	
	if cv2.waitKey(100) > 0:
		break
	
	