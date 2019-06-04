# Align Iranian National Id Card
A program to align rotated **id cards** and extract user data from it.

## Motivation Of Project
For a user authentication project by the National IdCard, a number of data (national card image) were collected that some of these data could not be processed due to their size and scale. Because of this, images are manually aligned by the Camscanner program. They were then cut off. A national card balancing program was written to automate this process.

## Prerequisites
```
Python 3+
Opencv 3.4+
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
There is a sample input card in **input_cards/2.jpg** directory you replace it with you're own real cards.
## License
MIT ©2019
