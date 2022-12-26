import cv2
import numpy as np
import pyautogui

# Load the pre-trained SSD model
# https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md#coco-trained-models
model = cv2.dnn.readNetFromTensorflow("ssd_model.pb", "ssd_model.pbtxt")

# Capture a screenshot of the screen
screenshot = pyautogui.screenshot()

# Convert the screenshot to a NumPy array
image = np.array(screenshot)

# Create a blob from the image
blob = cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True, crop=False)

# Set the input to the model
model.setInput(blob)

# Run the model and get the detections
detections = model.forward()

# Iterate over the detections and draw a rectangle around each one
for i in range(detections.shape[2]):
    confidence = detections[0, 0, i, 2]
    if confidence > 0.5:
        x1 = int(detections[0, 0, i, 3] * image.shape[1])
        y1 = int(detections[0, 0, i, 4] * image.shape[0])
        x2 = int(detections[0, 0, i, 5] * image.shape[1])
        y2 = int(detections[0, 0, i, 6] * image.shape[0])
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

# Show the image with the detected soldiers
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
