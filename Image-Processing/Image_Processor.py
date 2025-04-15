import cv2
import numpy as np

def detect_squares(frame, min_area=1500, square_only=True):
    # Convert to grayscale and apply GaussianBlur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding instead of a fixed threshold for better results
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY, 11, 2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < min_area:
            continue

        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the contour has 4 vertices (i.e., it might be a square or rectangle)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h

            # If square_only is True, filter out rectangles
            if square_only and not (0.9 <= aspect_ratio <= 1.1):
                continue

            # Draw the square or rectangle
            cv2.drawContours(frame, [approx], -1, (0, 215, 255), 3)  # Golden color
            shape_type = "Square" if square_only else "Rectangle"
            cv2.putText(frame, shape_type, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (0, 215, 255), 2)

    return frame

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Call the function to detect squares or rectangles
    frame = detect_squares(frame, min_area=1500, square_only=True)

    # Display the result
    cv2.imshow("Square Detection", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
