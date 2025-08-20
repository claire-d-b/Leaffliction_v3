- To launch the project

make re

- To create Augmented or Transformed images

./Augmentation <folder/subfolder> example Train/Train_Black_rot

./Transformation <folder/subfolder> example Train/Train_Black_rot

- To train the model on either augmented images or tranformed images

./train "Augmented" or ./train "Transformed"

- To predict

./predict

- To compare predicitions vs real classes

./compare

- To predict Apple data based on 50 (x6 transformations x6 augmentations = 1800) training examples per class and 25 validation examples per class

make Apple
