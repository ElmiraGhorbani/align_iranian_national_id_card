# Align Iranian National ID Card
A program to align rotated **id cards** and extract user data from it.

![](demo.gif)

## Motivation of the Project
While working on a user authentication project for the National ID Card Organization, some of collected sample images could not be processed due to irregularity in size and scale. To overcome the problem, images were manually corrected using CamScanner. They were then cut off to be in the proper form. Repeating this process over and over is clearly a tedious task, so a simple program was written to automate it.

## Prerequisites
```
Python 3+
Opencv 3.4.+
Numpy
Scikit-Image
Tensorflow
```
## Running
```
git clone https://github.com/ElmiiiRaa/align_iranian_national_id_card.git
cd align_iran_national_id_card
python main.py
```
A sample card already exists in the **input_cards** directory. Simply replace it with your own input files. It's recommended to use no more than 2 or 3 files in each run.

## Projects we borrowed from
* Text detection in images : https://github.com/jojo23333/ctpn

## Author

* **Elmira Ghorbani** 

See the [blog post](http://blog.class.vision/1398/04/2541/#more-2541) for more information.

## License
MIT ©2019
