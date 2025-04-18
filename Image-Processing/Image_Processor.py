import cv2
import numpy as np

# limited to cube colors
COLOR_NAMES = {
    "Red": (0, 0, 255),
    "Green": (0, 255, 0),
    "Blue": (255, 0, 0),
    "Yellow": (0, 255, 255),
    "Orange": (0, 165, 255)
}

# get our color name based on the bgr value
def closest_color_name(bgr_color):
    min_dist = float('inf')
    closest_name = "Unknown"

    for name, bgr in COLOR_NAMES.items():
        dist = np.linalg.norm(np.array(bgr_color) - np.array(bgr))

        if dist < min_dist:
            min_dist = dist
            closest_name = name

    return closest_name


def detect_squares(frame, min_area=1500, square_only=True):
    color_frame = frame.copy()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < min_area:
            continue

        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4 and cv2.isContourConvex(approx):
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h

            if square_only and not (0.9 <= aspect_ratio <= 1.1):
                continue

            # Draw the contour
            cv2.drawContours(frame, [approx], -1, (0, 215, 255), 3)
            shape_type = "Square" if square_only else "Rectangle"

            # Mask the square
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.drawContours(mask, [approx], -1, 255, -1)

            mean_color = cv2.mean(color_frame, mask=mask)[:3]
            mean_color = tuple(map(int, mean_color))

            # Get closest color name (restricted to 5)
            color_name = closest_color_name(mean_color)

            label = f"{shape_type} - {color_name}"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 215, 255), 2)

    return frame


# open our camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Err: Failed to access webcam.")
    exit()

# our main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # display out view
    frame = detect_squares(frame)
    cv2.imshow("Square Detection", frame)

    # exit case
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
