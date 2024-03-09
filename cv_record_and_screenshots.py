import cv2 as cv
import os
from datetime import datetime

# Initialize camera
camera = cv.VideoCapture(0)  # Change to 0 for default camera, or provide the camera index

# Check if the camera is opened
if not camera.isOpened():
    print("Error: Unable to open camera.")
    exit()

# Get camera properties
fps = camera.get(cv.CAP_PROP_FPS)
frame_width = int(camera.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv.CAP_PROP_FRAME_HEIGHT))

# Define codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
out = cv.VideoWriter(os.path.join(output_dir, 'output.avi'), fourcc, fps, (frame_width, frame_height))

# Initialize mode to Preview
mode = "Preview"
cap_mode = False

while True:
    # Capture frame-by-frame
    ret, frame = camera.read()

    if ret:
        # Check mode and perform actions accordingly
        if mode == "Record":
            cv.circle(frame, (50, 50), 20, (0, 0, 255), -1)
            cv.putText(frame, 'Recording...', (40,100), cv.FONT_HERSHEY_DUPLEX, 0.5, (0,0,255)) #글쓰기
            # Write the frame to the output video file
            out.write(frame)
        
        if cap_mode == True:
            img_dir = output_dir
            now = datetime.now()
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            img_file = os.path.join(img_dir, f'capture_{timestamp}.png')
            cv.imwrite(img_file, frame)
            cap_mode = False

        # Display the current frame
        cv.imshow('Camera', frame)

        # Check for key presses
        key = cv.waitKey(1) & 0xFF

        # Change mode on Space key press
        if key == ord(' '):
            if mode == "Preview":
                mode = "Record"
            else:
                mode = "Preview"
        # Exit program on ESC key press
        elif key == 27:
            break

        elif key == ord('c'):
            cap_mode = not cap_mode

    else:
        break

# Release resources
camera.release()
out.release()
cv.destroyAllWindows()
