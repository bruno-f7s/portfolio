# Disaster Response Classification
Table of Contents:
1. Requirements
2. File Descriptions


---
## 1. Requirements
To run the code you need the following software:
- Python v.3+
- Suggestion: Anaconda v.4+ since it has already many of the needed packages

## 2. File Descriptions
### 2.1. Web App
| File Name      | Description |
| ----------- | ----------- |
| go.html      | HTML file provided by Udacity for this project responsible to pass URL parameters as message for classification. |
| master.html    | HTML file provided by Udacity for this project with the full HTML structure of the web app. |
| run.py    | Script used to start up the web app and take care of the back-end. |


### 2.2. Data
| File Name      | Description |
| ----------- | ----------- |
| categories.csv      | CSV file with the categories' data provided by [Appen](https://appen.com/). |
| messages.csv      | CSV file with the messages' data provided by [Appen](https://appen.com/). |
| process_data.py    | Script used to load and process the data from the CSV files and create a SQL Lite database. |
| DisasterResponse.db   | SQL Lite database containing the processed and labelled data. |


### 2.3. Model
| File Name      | Description |
| ----------- | ----------- |
| train_classifier.py      | Script with a ML pipeline to create the best fitting model for the data based on a algorithm and multiple parameters. It deploys the model as a pickel file.|
| dr_classifier.pkl      | Pickel file with the fitted model. |


### 2.4. Extra
| File Name      | Description |
| ----------- | ----------- |
| data-preparation.ipynb      | Jupyter notebook with the loading and preparation used as an assistance to try and run the code of process_data.py. NOT NEEDED to run the web app.|
| ml-pipeline-preparation.ipynb     | Jupyter notebook with the ml-pipeline used as an assistance to try out different algorithms and parameters to chose the best algorithm for the ml-pipeline of train_classifier.py. NOT NEEDED to run the web app. |



