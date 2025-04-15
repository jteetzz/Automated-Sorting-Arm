import cv2
import numpy as np

# Open the camera (change index if necessary)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Show the captured frame
    cv2.imshow("Frame", frame)

    # Exit when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

def detect_color_objects(frame, lower_color, upper_color):
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask based on the color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find contours (objects) in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours, mask


# Color ranges for detection (e.g., red)
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detect red color objects
    contours, mask = detect_color_objects(frame, lower_red, upper_red)

    # Draw contours on the frame
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Minimum area to consider (filter noise)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Show the frame with the detected objects
    cv2.imshow("Frame", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
