import cv2

# Replace with your RTMP URL\
RTMP_URL = "rtmp://localhost/live"
MAX_CONSECUTIVE_FAILURES = 30

cap = cv2.VideoCapture(RTMP_URL, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print("Error: Could not open RTMP stream.")
    exit(1)

print("Press 'q' to quit.")

consecutive_failures = 0

while True:
    ret, frame = cap.read()

    if not ret or frame is None: # type: ignore[reportUnnecessaryComparison]
        consecutive_failures += 1
        print(f"Warning: dropped frame ({consecutive_failures}/{MAX_CONSECUTIVE_FAILURES}).")
        if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
            print("Error: too many consecutive dropped frames, stream lost.")
            break
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        continue

    consecutive_failures = 0
    cv2.imshow("RTMP Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()