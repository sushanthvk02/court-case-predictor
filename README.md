# Supreme Court Case Outcome Predictor 
This repository contains all the data and notebooks used in our final CSC 396 project. We constructed a feedforward neural network to classify Supreme Court cases based on which party (first or second) won the case. The notebooks in this repository should be executed in order of their numbering. See the project report included in this repository for more details on the exact mechanics of the code, and analysis of our model and errors.

## Instructions
First, execute 01_preprocessing.ipynb to convert the cases.json into the clean and raw datasets described in the report. This will also produce some graphs on statistics about the dataset.

Next, execute any of the notebooks numbered 02-04. Each of these is largely the same, just using the different datasets. 02 runs the model training and error plotting for the clean and unbalanced dataset. 03 runs the same for the raw dataset, and 04 runs the same for the clean and balanced dataset. 

Some useful plots from each of these notebooks will be stored in results.

If you want to build the cases.json from the raw data files, follow the instructions in the following section.

## Build cases.json from Scratch
1. Download the release from walkerdb dataset [here](https://github.com/walkerdb/supreme_court_transcripts/releases) and the justice.csv from the Kaggle dataset [here](https://www.kaggle.com/datasets/deepcontractor/supreme-court-judgment-prediction).
2. Unzip the walkerdb archive and navigate to supreme_court_transcripts/oyez/.
3. Copy the cases folder to the data directory.
    1. You want to remove all cases with years older than 1970, since we limited our analysis to that range. Clear Oyez reporting of years only activates around 1955, so that is the lowest you should go for the matching code to work.
5. Place the justice.csv in the data directory.
6. Run collect_data.py to create a new cases.json file.

## File Descriptions (somewhat redundant with report)

01_preprocessing.ipynb - This file loads in the case information json, and creates two versions of the data, one without possible leakage words, and one with possible leakage words. It then processes the facts and the transcripts into a single block of text, and the decision/winner into a binary label. It then saves the two versions of the dataset.

02_feedfoward_embeddings (clean data).ipynb - This file loads in the cleaned dataset without any leakage words. The text is tokenized, lowercased, and then filtered for stopwords. From there a vocabulary of words is formed and each token is mapped to an ID. Each court case is converted to a sequence of token ID’s and padded to a length of 45,000 and then split into training and test sets. A Pytorch SCOTUS dataset and DataLoader pipeline feeds batches of these cases into a feed forward neural network. The model is then evaluated and visualizations of its performance are created. Finally, error analysis is performed at the end.

03_feedfoward_embeddings (raw data).ipynb - This file loads in the raw dataset containing leakage words. The text is tokenized, lowercased, and then filtered for stopwords. From there a vocabulary of words is formed and each token is mapped to an ID. Each court case is converted to a sequence of token ID’s and padded to a length of 45,000 and then split into training and test sets. A Pytorch SCOTUS dataset and DataLoader pipeline feeds batches of these cases into a feed forward neural network. The model is then evaluated and visualizations of its performance are created. Finally, error analysis is performed at the end.

04_feedfoward_embeddings (clean and balanced data).ipynb - This file loads in the cleaned dataset without any leakage words. The text is tokenized, lowercased, and then filtered for stopwords. From there a vocabulary of words is formed and each token is mapped to an ID. Each court case is converted to a sequence of token ID’s and padded to a length of 45,000 and then split into training and test sets. Before training, the dataset is balanced by undersampling the larger class so that the number of first party winning and second party winning cases in the training set are equal. A Pytorch SCOTUS dataset and DataLoader pipeline feeds batches of these cases into a feed forward neural network. The model is then evaluated and visualizations of its performance are created. Finally, error analysis is performed at the end.
