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
import numpy as np
from face_tracker import FaceTracker
from eye_detector import get_eyes
import os
from os import listdir
from os.path import isfile, join
import shutil
import math
from rotate_crop_with_HoughLines import HoughLines
from information_exteract import card_data
EYE_DIST = 60

input_cards_path = 'input_cards/'
rotated_cards_path = 'outputs/rotated_cards'
cards_cropped_by_eyes_path = 'outputs/cards_cropped_by_eyes'


if __name__ == '__main__':

	import sys, getopt
	
	cascade_fn = "data_harr/haarcascade_frontalface_alt2.xml"
	
	
	scale=1
	scaleFactor=1.3
	
	tracker = FaceTracker(cascade_fn,scale,scaleFactor)

	files = [f for f in listdir(input_cards_path) if isfile(join(input_cards_path, f))]


	#====================#
	#read ou image files#
	#====================#

	for file in files:
		img = cv2.imread(input_cards_path + file)
		print(file)
		#save path
		save_rotated_card = os.path.join(rotated_cards_path, file)
		save_cropped_by_eyes = os.path.join(cards_cropped_by_eyes_path, file)
	
		npoints,rects,angle= tracker.detect(img)

		img=tracker.draw_rectangle(img,npoints)
		cv2.imwrite(file,img)

		face_angle=tracker.face_angle(img,npoints)
		

		#=================================#
		# #set right angle to rotate a card#
		#=================================#
		if angle == 90 or angle == 180:
			angle_card = -angle

		elif angle == 270 and face_angle == 90:
			angle_card = -angle

		elif angle == 270 and face_angle < 0:
			angle_card = -angle

		elif angle == 330 and face_angle>0:
			angle_card = 0

		elif angle == 330 and face_angle<0:
			angle_card = -180

		elif angle == 150 and face_angle < 0:
			angle_card = -270

		elif angle == 270 and face_angle != 90:
			face_angle = 90 -face_angle
			angle_card = -(angle+face_angle)

		elif angle==120:
			angle_card = 220

		elif angle==300 and face_angle != 90:
			angle_card = 90		

		else:
			angle_card = face_angle	

		#======================================#
		# rotated cards according to card angle#
		#======================================#

		height, width = img.shape[:2] # image shape has 3 dimensions
		image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
		rotation_mat = cv2.getRotationMatrix2D(image_center, angle_card, 1.)

		# rotation calculates the cos and sin, taking absolutes of those.
		abs_cos = abs(rotation_mat[0,0]) 
		abs_sin = abs(rotation_mat[0,1])
			
		# find the new width and height bounds
		bound_w = int(height * abs_sin + width * abs_cos)
		bound_h = int(height * abs_cos + width * abs_sin)
		
		# subtract old image center (bringing image back to origo) and adding the new image center coordinates
		rotation_mat[0, 2] += bound_w/2 - image_center[0]
		rotation_mat[1, 2] += bound_h/2 - image_center[1]

		# rotate image with the new bounds and translated rotation matrix
		rotated_mat = cv2.warpAffine(img, rotation_mat, (bound_w, bound_h))

		#===================#
		#save rotated image#
		#===================#
		cv2.imwrite(save_rotated_card,rotated_mat)
		rotated=rotated_mat
			
		#===================#
		#show rotated image#
		#===================#
		#cv2.imshow('Image rotated by - ? degrees',cv2.resize(rotated_mat,(1000,630)))
		#cv2.waitKey(0)

			

		#=================================================#
		#find eyes and resize id cards like it's real size#
		#=================================================#
		image=rotated
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
	
		cv2.rectangle(image, ((x1)  , (y1) ) ,((x2) , (y2)  ) , (86,170,240) ,3)
		

		idCard = image[int(y1  - 350):int(y1  + 380), int(x1 - 200):int(x2 + 660 +70 +80)]
		idCard_h , idCard_w = idCard.shape[:2]
		orig_img_h , orig_img_w  = image.shape[:2]
		#print(image.shape)
		

		if idCard_w < 600 or idCard_h < 600 :

			cx1=orig_img_w*4.05
			cx2=orig_img_w/4.05
			
			temp_h=orig_img_h/2
			cy1=temp_h*1.22
			cy2=temp_h/1.22
			
			idCard = image[int(y1  - cy2):int(y1  + cy1), int(x2 - cx2):int(x2 + cx1)]
		
		if orig_img_h < 600 or orig_img_w < 900:

			#cv2.imshow('cropped',image)
			cv2.imwrite(save_cropped_by_eyes,image)

		else:
			#cv2.imshow('cropped',idCard)
			cv2.imwrite(save_cropped_by_eyes,idCard)
	HoughLines()
	card_data()
	#os.system('python ./ctpn/demo_pb.py')

		

