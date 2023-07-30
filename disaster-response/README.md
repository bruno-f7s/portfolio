# Disaster Response Classification
Table of Contents:
1. Introduction
2. Requirements
3. How to run the code
4. File descriptions
5. Data
6. Web app
7. Disclaimer

---
## 1. Project Introduction
This project was developed as part of the [Udacity's Data Scientist Nanodegree program]( https://www.udacity.com/course/data-scientist-nanodegree--nd025) and consists of a machine learning multi-label classification problem. The objective was to train a model that can predict the labels for text messages and deploy it in a simple web app so that other users are able to interact with the model. 

For understanding of the context of the problem, let us assume that a certain natural disaster occurs in a certain region and that people affected in that region start to post messages online in a specific social media platform. These messages could then be classified live using the model, which could more quickly be intercepted by a specific helper organization with the aim of knowing which kind of help would be need or which kind of disaster had happened. Possible classification categories can be _food_, _water_, _earthquake_, etc.

The goal of the project was not to create the best possible model but instead develop and apply the needed skills to create a data preparation pipeline, a machine learning pipeline as well as a web interface.


## 2. Requirements
To run the code you need the following software:
- Python v.3+
- Packages:
  - pandas
  - numpy
  - sklearn
  - re
  - nltk
  - sqlite3
  - joblib 
- Suggestion: Anaconda v.4+ since it already includes the majority of the needed packages


## 3. How to run the code
To interact with this code follow these steps:
1. Download the complete project or fork this repository
2. (Not necessary if the `data\DisasterResponse.db` is already available). To run the ETL pipeline that cleans, processes and stores the data, run the following command inside the `data` directory:`python process_data.py messages.csv categories.csv DisasterResponse.db`
3. (Not necessary if the `model\dr_classifier.pkl` is already available). To run the ML pipeline that trains and deploys the model, run the following command inside the `models` directory:`python train_classifier.py ..\data\DisasterResponse.db dr_classifier.pkl`.
4. To start the app run the following command inside `app` directory: `python run.py`.
5. Open this link on your browser: [http://127.0.0.1:3001/](http://127.0.0.1:3001/).


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

## 6 Web app
The web app has an area where the use can enter a message for classification:

![Screenshot of the web app](images/dr_app_screenshot_1.png "Web app screenshot 1")

Below that area there are two graphics that give an overview about the data at hand.

![Screenshot of the web app](images/dr_app_screenshot_2.png "Web app screenshot 2")

![Screenshot of the web app](images/dr_app_screenshot_3.png "Web app screenshot 3")

The performance of the model for the training set can be seen below:

__Accuracy__ per label:
```
request                   0.803520
offer                     0.962546
aid_related               0.626484
medical_help              0.634875
medical_products          0.706508
search_and_rescue         0.770774
security                  0.813754
military                  0.774048
water                     0.634056
food                      0.646541
shelter                   0.610929
clothing                  0.858985
money                     0.803111
missing_people            0.881907
refugees                  0.750307
death                     0.696275
other_aid                 0.567131
infrastructure_related    0.670487
transport                 0.715718
buildings                 0.702415
electricity               0.835039
tools                     0.940442
hospitals                 0.891731
shops                     0.946582
aid_centers               0.883135
other_infrastructure      0.732296
weather_related           0.641220
floods                    0.659844
storm                     0.727384
fire                      0.885591
earthquake                0.746828
cold                      0.831764
other_weather             0.692796
direct_report             0.753377
```

__Precision__, __Recall__ and __F1-Score__ per label:
```
                        precision    recall  f1-score   support

               request       0.65      0.78      0.71      1481
                 offer       0.03      0.10      0.04        41
           aid_related       0.78      0.68      0.73      3597
          medical_help       0.16      0.37      0.23       701
      medical_products       0.10      0.29      0.14       420
     search_and_rescue       0.05      0.20      0.08       235
              security       0.04      0.19      0.07       166
              military       0.10      0.43      0.16       254
                 water       0.13      0.43      0.20       514
                  food       0.29      0.56      0.38       963
               shelter       0.19      0.47      0.27       741
              clothing       0.07      0.34      0.12       135
                 money       0.05      0.23      0.09       195
        missing_people       0.02      0.12      0.04        98
              refugees       0.07      0.29      0.11       273
                 death       0.09      0.32      0.14       387
             other_aid       0.26      0.48      0.34      1122
infrastructure_related       0.13      0.35      0.19       527
             transport       0.10      0.33      0.16       389
             buildings       0.10      0.30      0.15       432
           electricity       0.05      0.21      0.09       181
                 tools       0.02      0.08      0.03        52
             hospitals       0.01      0.07      0.02        81
                 shops       0.00      0.03      0.01        37
           aid_centers       0.02      0.09      0.03        99
  other_infrastructure       0.10      0.32      0.15       360
       weather_related       0.65      0.60      0.63      2437
                floods       0.24      0.56      0.33       740
                 storm       0.31      0.51      0.39       834
                  fire       0.02      0.10      0.03        77
            earthquake       0.33      0.48      0.39       820
                  cold       0.07      0.27      0.11       183
         other_weather       0.12      0.38      0.18       446
         direct_report       0.62      0.73      0.67      1695

             micro avg       0.26      0.53      0.35     20713
             macro avg       0.18      0.34      0.22     20713
          weighted avg       0.41      0.53      0.44     20713
           samples avg       0.29      0.55      0.35     20713
```
## 7 Disclaimer
- The data was provided by [Appen](https://appen.com/).
- The HTML code parts were provided by [Udacity](https://www.udacity.com).
