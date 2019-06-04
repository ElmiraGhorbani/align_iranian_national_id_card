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
import math
import operator
import random
import os
from os import listdir
from os.path import isfile, join


cards_cropped_by_eyes_path = 'outputs/cards_cropped_by_eyes/'
cards_cropped_rotated_path = 'outputs/cards_cropped_rotated'
cards_rotated_path = 'outputs/rotated_cards_by_HoughLines'

files = [f for f in listdir(cards_cropped_by_eyes_path) if isfile(join(cards_cropped_by_eyes_path, f))]

def rotate(image, theta):
        
        (h, w) = image.shape[:2]
        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, theta, 1)
        rotated = cv2.warpAffine(image, M, (int(w), int(h)), cv2.INTER_LINEAR,borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))
        return rotated



def dot(vA, vB):
        return vA[0]*vB[0]+vA[1]*vB[1]



def ang(lineA, lineB):
        # Get nicer vector form
        vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
        vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
        # Get dot prod
        dot_prod = dot(vA, vB)
        # Get magnitudes
        magA = dot(vA, vA)**0.5
        magB = dot(vB, vB)**0.5
        # Get cosine value
        cos_ = dot_prod/magA/magB
        # Get angle in radians and then convert to degrees
        angle = math.acos(dot_prod/magB/magA)
        # Basically doing angle <- angle mod 360
        ang_deg = math.degrees(angle)%360

        #mydegrees = math.degrees(myradians)
        #myradians = math.radians(mydegrees)

        if ang_deg-180>=0:
                # As in if statement
                return 360 - ang_deg
        else: 

                return  math.radians(ang_deg)

def crop(x1,x2,x3,x4,y1,y2,y3,y4,img):
        
        x1 = x1
        x2 = x2

        x3 = x3
        x4 = x4

        y1 = y1
        y2 = y2

        y3 = y3
        y4 = y4

        top_left_x = min([x1,x2,x3,x4])
        top_left_y = min([y1,y2,y3,y4])
        bot_right_x = max([x1,x2,x3,x4])
        bot_right_y = max([y1,y2,y3,y4])

        rotated = img

        cropped=rotated[top_left_y:bot_right_y, top_left_x:bot_right_x]
        crop_h , crop_w = cropped.shape[:2]
        rotated_h , rotated_w = rotated.shape[:2]

        if crop_h < 300 or crop_w <900:

                return rotated
        else:
                return cropped


def HoughLines():

        for file in files:
                img = cv2.imread(cards_cropped_by_eyes_path + file)
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                kernel = np.ones((5,5),np.float32)/25
                gray = cv2.filter2D(gray,-1,kernel)
                edges = cv2.Canny(gray,400,600,apertureSize = 5)
                cv2.imwrite(file,edges)

                """
                cv2.imshow('image',cv2.resize(edges,(1000,630)))
                cv2.waitKey(0)

                """
                lines = cv2.HoughLines(edges,1,np.pi/180,15)

                pointsListX1 =[]
                pointsListX2 =[]
                pointsListY1 =[]
                pointsListY2 =[]
                anglesList =  []
                for i in range(8):
                        for rho,theta in lines[i]:
                                a = np.cos(theta)
                                b = np.sin(theta)
                                x0 = a*rho
                                y0 = b*rho
                                x1 = int(x0 + 1000*(-b))
                                y1 =int(y0 + 1000*(a))
                                x2 = int(x0 - 1000*(-b))
                                y2 = int(y0 - 1000*(a))
                                angle = np.arctan2(y2 - y1, x2 - x1) * 180. / np.pi
                                
                                #draw whole detected line
                                #cv2.line(img,(x1 ,y1),( x2,y2),(62,0,255),2)
                                if x1<0:
                                        pointsListX1.append(x1)
                                        pointsListY1.append(y1)
                                        pointsListX2.append(x2)
                                        pointsListY2.append(y2)
                                        anglesList.append(angle)

                                #print(x1 ,y1 ,'   ', x2 ,y2 ,'  ',angle )

                #bottom line
                index, value = max(enumerate(pointsListY1), key=operator.itemgetter(1))

                # draw bottom line
                #cv2.line(img,(pointsListX1[index] ,pointsListY1[index] ),( pointsListX2[index] ,pointsListY2[index]),(255,0,255),2)
                sub_y_frist_line = pointsListY2[index] - pointsListY1[index]

                #print(pointsListY1 , pointsListY2,anglesList)
                #print(sub_y_frist_line)

                #top line
                temp = []

                for indy in range(len(pointsListY2)):
                        sub = pointsListY2[indy] - pointsListY1[indy] 
                        sub_y_2 = pointsListY2[index] - pointsListY2[indy]
                        sub_y_1 = pointsListY1[index] - pointsListY1[indy]
                        
                        # print(sub,sub_y_1 ,sub_y_2)

                        if sub_y_frist_line == 1:
                                if sub > 1 and anglesList[indy] > 0 and anglesList[indy] > anglesList[index] and sub_y_2 >500 and sub_y_1 >500 :
                                        second_index=indy
                                        #print(indy)
                                        break
                                else:
                                        if sub == 1 and anglesList[indy] > 0  and sub_y_2 >400 and sub_y_1 >400 :
                                                second_index=indy
                                                #print(indy)
                                                break
                                        
                        elif sub_y_frist_line<0: 
                                tempL=[]
                                for i in range(len(pointsListY1)):
                                        if pointsListY1[i] > 0 and pointsListY1[i] < pointsListY1[index] and anglesList[i] >= anglesList[index]:
                                                tempL.append(pointsListY1[i])
                                                indx, value = min(enumerate(tempL), key=operator.itemgetter(1))
                                                second_index=pointsListY1.index(value)
             

                        else:
                                if sub == 1 and anglesList[indy] > 0  and sub_y_2 > 0 and sub_y_1 > 0 :
                                        temp.append(pointsListY1[indy])
                                        ind, val = max(enumerate(temp), key=operator.itemgetter(1))
                                        second_index = pointsListY1.index(val)
                                        #print(second_index)
                                
                #draw top line                                                   
                #cv2.line(img,(pointsListX1[second_index] ,pointsListY1[second_index] ),( pointsListX2[second_index] ,pointsListY2[second_index]),(255,0,255),2)
               # print( 'angles: (top , bottom) :', anglesList[second_index], anglesList[index])

                lineA =[[pointsListX1[index],pointsListY1[index] ],[pointsListX2[index],pointsListY2[index]]]
                lineB =[[pointsListX1[second_index],pointsListX1[second_index]],[pointsListX2[second_index],pointsListY2[second_index]]]
                angle =ang(lineA , lineB) 
                #print(angle)

                if anglesList[index]== anglesList[second_index]:
                        rotated=rotate(img , -(anglesList[index]-angle))

                else:
                        rotated=rotate(img , (anglesList[second_index]-angle))

                save_cards_rotated_path = os.path.join(cards_rotated_path, file)
                cv2.imwrite(save_cards_rotated_path,rotated)

                #cv2.imshow('rotated',cv2.resize(rotated,(1000,630)))
                #cv2.waitKey(0)
              
                crop_img = crop(pointsListX1[index] ,pointsListX1[second_index] ,pointsListX2[index] ,pointsListX2[second_index] ,pointsListY1[index] ,pointsListY1[second_index] ,pointsListY2[index] ,pointsListY2[second_index],rotated)   
                # cv2.imshow('crop',cv2.resize(crp,(1000,630)))
                save_crop_rotated_card = os.path.join(cards_cropped_rotated_path, file)
                cv2.imwrite(save_crop_rotated_card,crop_img)
                cv2.waitKey(0)     
