import cv2
import numpy as np

face_classifier = cv2.CascadeClassifier('data_harr/haarcascade_frontalface_alt2.xml')
eye_classifier = cv2.CascadeClassifier('data_harr/haarcascade_eye.xml')


def get_eyes(img):
    eyes_total = []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 6)

    if faces is ():
        print(' face not found ! ')
        return img

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        eyes = eye_classifier.detectMultiScale(roi_gray)
        eyes_row_args = eyes[:,2].argsort()[-2:][::-1]
    
        for eyes_row_arg in eyes_row_args:
            [ex, ey, ew, eh] = eyes[eyes_row_arg,:]
            eyes_total.append([ex + x, ey + y, ew, eh])
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (188, 16, 190), 2) #-- Drawe on eye
        eyes_total = np.array(eyes_total)
        eyes_total = eyes_total[eyes_total[:, 0].argsort()]
        return (eyes_total[0,:], eyes_total[1,:])
    
    cv2.waitKey(0)

