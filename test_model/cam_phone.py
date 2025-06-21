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

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Inference (model expects RGB)
    results = model(frame[..., ::-1])

    # Render results (in RGB)
    annotated_frame = results.render()[0]

    # Convert to BGR for OpenCV display
    annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

    # Get frame dimensions
    height, width, _ = annotated_frame.shape

    # Draw a plus sign (+) in the center of the frame
    center_x, center_y = width // 2, height // 2
    line_length = 20
    color = (0, 255, 0)  # Green color
    thickness = 2

    # Vertical line of plus
    cv2.line(annotated_frame,
             (center_x, center_y - line_length),
             (center_x, center_y + line_length),
             color, thickness)

    # Horizontal line of plus
    cv2.line(annotated_frame,
             (center_x - line_length, center_y),
             (center_x + line_length, center_y),
             color, thickness)

    # Show frame
    cv2.imshow("YOLOv5 Fire Detection - DroidCam", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
