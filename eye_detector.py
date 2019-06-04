# MIT License
#
# Copyright (c) 2019 https://github.com/ElmiiiRaa/align_iranian_national_id_card
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#author : Elmira Ghorbani
#email:elmira.ghorbani96@gmail.com

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


