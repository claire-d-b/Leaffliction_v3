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

make re;

echo "processing train pictures' transformations...";
./Transformation.py Train/Train_Grape_Black_rot --script &
./Transformation.py Train/Train_Grape_Esca --script &
./Transformation.py Train/Train_Grape_healthy --script &
./Transformation.py Train/Train_Grape_spot --script &
wait
echo "processing train pictures' augmentations...";
./Augmentation.py Train/Train_Grape_Black_rot --script &
./Augmentation.py Train/Train_Grape_Esca --script &
./Augmentation.py Train/Train_Grape_healthy --script &
./Augmentation.py Train/Train_Grape_spot --script &
wait

./train.py Augmented;
mv features.csv dataset_test_truth.csv;
mv features_test.csv dataset_test.csv;
mv thetas.csv thetas_old.csv;
mv output_class_I.png output_class_I_old.png;

echo "processing test pictures' transformations...";
./Transformation.py Test/Test_Grape_Black_rot --script &
./Transformation.py Test/Test_Grape_Esca --script &
./Transformation.py Test/Test_Grape_healthy --script &
./Transformation.py Test/Test_Grape_spot --script &
wait
echo "processing test pictures' augmentations...";
./Augmentation.py Test/Test_Grape_Black_rot --script &
./Augmentation.py Test/Test_Grape_Esca --script &
./Augmentation.py Test/Test_Grape_healthy --script &
./Augmentation.py Test/Test_Grape_spot --script &
wait

if [[ $(uname -s) == "Darwin" ]]; then
    sed -i '' 's/features_Train_/features_Test_/g' train.py
else
    sed -i 's/features_Train_/features_Test_/g' train.py
fi;
./train.py Augmented;

./predict.py;
./compare.py;

if [[ $(uname -s) == "Darwin" ]]; then
    sed -i '' 's/features_Test_/features_Train_/g' train.py
else
    sed -i 's/features_Test_/features_Train_/g' train.py
fi;