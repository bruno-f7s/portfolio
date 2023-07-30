# Disaster Response Classification
Table of Contents:
1. Introduction
2. Requirements
3. How to run the code
4. File Descriptions
5. Data


---
## 1. Project Introduction
This project was developed as part of the [Udacity's Data Scientist Nanodegree program]( https://www.udacity.com/course/data-scientist-nanodegree--nd025) and consists of a machine learning multi-label classification problem. The objective was to train a model that can predict the labels for text messages and deploy it in a simple web app so that other users are able to interact with the model. 

For understanding of the context of the problem, let us assume that a certain natural disaster occurs in a certain region and that people affected in that region start to post messages online in a specific social media platform. These messages could then be classified live using the model, which could more quickly be intercepted by a specific helper organization with the aim of knowing which kind of help would be need or which kind of disaster had happened. Possible classification categories can be _food_, _water_, _earthquake_, etc.

The goal of the project was not to create the best possible model but instead develop and apply the needed skills to create a data preparation pipeline, a machine learning pipeline as well as a web interface.


## 2. Requirements
To run the code you need the following software:
- Python v.3+
- Suggestion: Anaconda v.4+ since it has already many of the needed packages


## 3. How to run the code
To run the code you need the following software:
- Python v.3+
- Suggestion: Anaconda v.4+ since it has already many of the needed packages


## 4. File Descriptions
### 4.1. Web App
| File Name      | Description |
| ----------- | ----------- |
| go.html      | HTML file provided by Udacity for this project responsible to pass URL parameters as message for classification. |
| master.html    | HTML file provided by Udacity for this project with the full HTML structure of the web app. |
| run.py    | Script used to start up the web app and take care of the back-end. |


### 4.2. Data
| File Name      | Description |
| ----------- | ----------- |
| categories.csv      | CSV file with the categories' data provided by [Appen](https://appen.com/). |
| messages.csv      | CSV file with the messages' data provided by [Appen](https://appen.com/). |
| process_data.py    | Script used to load and process the data from the CSV files and create a SQL Lite database. |
| DisasterResponse.db   | SQL Lite database containing the processed and labelled data. |


### 4.3. Model
| File Name      | Description |
| ----------- | ----------- |
| train_classifier.py      | Script with a ML pipeline to create the best fitting model for the data based on a algorithm and multiple parameters. It deploys the model as a pickel file.|
| dr_classifier.pkl      | Pickel file with the fitted model. |


### 4.4. Extra
| File Name      | Description |
| ----------- | ----------- |
| data-preparation.ipynb      | Jupyter notebook with the loading and preparation used as an assistance to try and run the code of process_data.py. NOT NEEDED to run the web app.|
| ml-pipeline-preparation.ipynb     | Jupyter notebook with the ml-pipeline used as an assistance to try out different algorithms and parameters to chose the best algorithm for the ml-pipeline of train_classifier.py. NOT NEEDED to run the web app. |


## 5. Data
The data consists of labelled messages and was provided by [Appen](https://appen.com/). It is divided into two csv files: categories.csv and messages.csv.

### 5.1. File: messages.csv
The messages.csv file has 4 columns:
- __id__: the message's id.
- __message__: the text information of the message in English. Example: "Is the Hurricane over or is it not over".
- __original__:  the text information of the message in its original language. Example: "Cyclone nan fini osinon li pa fini".
- __genre__: a category with the type of genre of the message (direct, news, social)

### 5.2. File: categories.csv
The messages.csv file has 2 columns:
- __id__: the message's id.
- __categories__: a string column with all the labels and its value (1 or 0) for the current message, example: "related-1;request-0;offer-0;aid_related-0;...".

### 5.3. Data Limitations
- The dataset has 26216 rows and 36 labels. Although the number of rows is of a considerable size there are many different labels.
- The labels _ related_ and _ child_alone_ only include one of the categories (1 or 0) and therefore do not hold any prediction power.
- Many labels like _aid_centers_ (2.1%), _tools_ (1.1%), _ shops_ (0.8%), etc. are extremely imbalanced. This will be a challenge for the algorithms considering the amount of data available and the complexity of the classification problem. 
- Without the two labels _ related_ and _ child_alone_, 11431 messages (57% of total) do not have any other label present. This means that these rows will always have 0 prediction on any of the present labels. This data was excluded from the training process to try compensating for the imbalanced labels and try some overfitting on said labels.
