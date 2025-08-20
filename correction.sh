#!/bin/bash

rm features_Train_*;
rm features_Test_*;
rm dataset_test_truth.csv;
rm dataset_test.csv;
rm output_class_I_old.png;
rm output_class_I.png;
rm output_class_II.png;
rm output_scurve.png;
rm thetas_old.csv;
rm thetas.csv;

make re

echo "processing Unit_test1 pictures' transformations...";
./Transformation.py Unit_test1/
echo "processing Unit_test1 pictures' augmentations...";
./Augmentation.py Unit_test1/

./predict.py
./compare.py