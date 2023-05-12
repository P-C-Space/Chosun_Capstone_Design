import cv2
import numpy as np

# webcam signal
VideoSignal = cv2.VideoCapture(0)
# yolo weight file
YOLO_net = cv2.dnn.readNet("yolo.weights","yolov2-tiny.cfg")


classes = []
with open("coco.names","r") as f:
	classes = [line.strip() for line in f.readlines()]
	
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i - 1] for i in YOLO_net.getUnconnectedOutLayers()]
colors = np.random.uniform(0,255,size = (len(classes),3 ))

while True:
	# webcam Frame
	ret, frame = VideoSignal.read()
	h,w,c = frame.shape # height width, channel
	
	# yolo input
	blob = cv2.dnn.blobFromImage(frame, 0.00392, (320,320), (0,0,0), True, crop = False)
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
			
			if confidence > 0.5:
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
	
	indexes = cv2.dnn.NMSBoxes(boxes,confidences, 0.45, 0.4)
	
	for i in range(len(boxes)):
		if i in indexes:
			x, y, w, h = boxes[i]
			label = str(classes[class_ids[i]])
			score = confidences[i]
			
			cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),5)
			cv2.putText(frame, label, (x,y-20),cv2.FONT_ITALIC,0.5, (255,255,255),1)
	
	cv2.imshow("YOLOv2",frame)
	
	if cv2.waitKey(100) > 0:
		break
	