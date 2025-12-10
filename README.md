# Supreme Court Case Outcome Predictor 
This repository contains all the data and notebooks used in our final CSC 396 project. We constructed a feedforward neural network to classify Supreme Court cases based on which party (first or second) won the case. The notebooks in this repository should be executed in order of their numbering. See the project report included in this repository for more details on the exact mechanics of the code, and analysis of our model and errors.

## Instructions
First, execute 01_preprocessing.ipynb to convert the cases.json into the clean and raw datasets described in the report. This will also produce some graphs on statistics about the dataset.

Next, execute any of the notebooks numbered 02-04. Each of these is largely the same, just using the different datasets. 02 runs the model training and error plotting for the clean and unbalanced dataset. 03 runs the same for the raw dataset, and 04 runs the same for the clean and balanced dataset. 

Some useful plots from each of these notebooks will be stored in results.
