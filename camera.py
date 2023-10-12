import cv2
import numpy as np
import time
from collections import deque
import imutils



def get_movement(frames, shape):
    movement_frame = np.zeros(shape, dtype='float32')
    i = 0
    for f in frames:
        i += 1
        movement_frame += f * i
    movement_frame = movement_frame / ((1 + i) / 2 * i)
    movement_frame[movement_frame > 254] = 255
    return movement_frame

def get_background(frames, shape):
    bg = np.zeros(shape, dtype='float32')
    for frame in frames:
        bg += frame
    bg /= len(frames)
    bg[bg > 254] = 255
    return bg

def detect(frame, bg_frames, fg_frames, threshold=25, min_box=50):
    fg_frames.append(frame)
    bg_frames.append(frame)
    fg_frame = get_movement(list(fg_frames), frame.shape)
    bg_frame = get_background(list(bg_frames), frame.shape)

    movement = cv2.absdiff(fg_frame, bg_frame)
    movement[movement < threshold] = 0
    movement[movement > 0] = 254
    movement = movement.astype('uint8')
    movement = cv2.cvtColor(movement, cv2.COLOR_BGR2GRAY)
    movement[movement > 0] = 254
    cv2.imshow('Movement', movement)
    contours = cv2.findContours(movement, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    boxes = []
    for contour in contours:
        if cv2.contourArea(contour) < min_box:
            continue
        box = cv2.boundingRect(contour)
        boxes.append(box)
    return boxes


def main(width=640, height=480, scale_factor=3):
    bg_frames = deque(maxlen=30)
    fg_frames = deque(maxlen=10)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    last_time = time.time()
    while True:
        _, frame = cap.read()
        frame = cv2.resize(frame, (width, height))
        work_frame = cv2.resize(frame, (width // scale_factor, height // scale_factor))
        work_frame = cv2.GaussianBlur(work_frame, (5, 5), 0)
        work_frame_f32 = work_frame.astype('float32')
        boxes = detect(work_frame_f32, bg_frames, fg_frames)
        if boxes != []:

            text = "FPS:" + str(int(1 / (time.time() - last_time)))
            last_time = time.time()
            cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()

