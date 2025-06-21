import cv2
import torch

# Load your custom YOLOv5 model (adjust path)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s_best.pt', force_reload=False)
model.eval()

# Use DroidCam IP stream URL instead of webcam device 0
stream_url = "http://192.168.0.108:4747/video"
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("Cannot open video stream")
    exit()

# Initial servo angle (simulate)
servo_angle = 90
servo_min = 0
servo_max = 180
servo_step = 5

# Threshold for alignment (pixels)
alignment_threshold = 20

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Inference (model expects RGB)
    results = model(frame[..., ::-1])
    # results.xyxy[0] is tensor of detected boxes: [x1, y1, x2, y2, confidence, class]
    detections = results.xyxy[0]

    # Convert to BGR for display
    annotated_frame = results.render()[0]
    annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

    height, width, _ = annotated_frame.shape
    center_x, center_y = width // 2, height // 2

    # Draw center cross
    line_length = 20
    color = (0, 255, 0)
    thickness = 2
    cv2.line(annotated_frame, (center_x, center_y - line_length), (center_x, center_y + line_length), color, thickness)
    cv2.line(annotated_frame, (center_x - line_length, center_y), (center_x + line_length, center_y), color, thickness)

    fire_center_x = None

    # Find the biggest detected fire (assuming class for fire detection)
    if len(detections) > 0:
        # Pick detection with highest confidence
        detection = detections[0]  # Already sorted by confidence (usually)
        x1, y1, x2, y2, conf, cls = detection.tolist()

        # Calculate center x of detected fire bbox
        fire_center_x = int((x1 + x2) / 2)

        # Draw a circle on the fire center
        cv2.circle(annotated_frame, (fire_center_x, center_y), 10, (0, 0, 255), -1)

        # Calculate difference from center
        diff_x = fire_center_x - center_x

        if abs(diff_x) <= alignment_threshold:
            print("Aligned! Shoot")
            # No servo movement here - stop
        else:
            if diff_x > 0:
                print("Move Right")
                servo_angle = min(servo_angle + servo_step, servo_max)
            else:
                print("Move Left")
                servo_angle = max(servo_angle - servo_step, servo_min)
            print(f"Servo angle: {servo_angle}")

    else:
        print("No fire detected")

    # Show frame
    cv2.imshow("YOLOv5 Fire Detection - DroidCam", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
