import cv2
import torch

# Load your custom YOLOv5 model (adjust path)
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s_best.pt', force_reload=False)
model.eval()

# Open webcam (0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam")
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

    # Show frame
    cv2.imshow("YOLOv5 Fire Detection", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
