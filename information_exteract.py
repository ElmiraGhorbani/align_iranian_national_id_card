#!/usr/bin/env python
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
from eye_detector import get_eyes
import os
from os import listdir
from os.path import isfile, join
import shutil
import math
from pylab import arange, array, uint8
from skimage import exposure, measure
from skimage.filters import threshold_local

EYE_DIST = 60

cards_cropped_rotated_path = 'outputs/cards_cropped_rotated/'
cards_information_path = 'data/demo'


files = [f for f in listdir(cards_cropped_rotated_path) if isfile(join(cards_cropped_rotated_path, f))]


def card_data():
	
	for file in files:
		image = cv2.imread(cards_cropped_rotated_path + file)
		left_eye, right_eye = get_eyes(image)
		x1 = left_eye[0] + left_eye[2]/2
		x2 = right_eye[0] + right_eye[2] / 2
		y1 = left_eye[1] + left_eye[3]/2
		y2 = right_eye[1] + right_eye[3] / 2
		
		length = math.sqrt(math.pow(x2 - x1,2) + math.pow(y2 - y1,2))
		scale = EYE_DIST / length
		image = cv2.resize(image, None, fx=scale, fy=scale)
			
		x1 = int(x1 * scale)
		x2 = int(x2 * scale)
		y1 = int(y1 * scale)
		y2 = int(y2 * scale) 

		image = image[int(y1  - 130):int(y1  + 310), int(x1 + 200):int(x2  + 660 )]
		#RGB to Black and White
		im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		ret, mask = cv2.threshold(im_gray, 190, 255, cv2.THRESH_BINARY)
		image2 = im_gray
		im_gray = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 12)
		im_gray = cv2.bitwise_or(im_gray, mask)
		im_gray = cv2.bitwise_or(im_gray, image2)
		im_gray = (255.0/1)*(im_gray/(255.0/1))**2
		im_gray = array(im_gray,dtype=uint8)
		im_gray = cv2.equalizeHist(im_gray)

		save_cards_inf_path = os.path.join(cards_information_path, file)
		cv2.imwrite(save_cards_inf_path, im_gray)	

