# Customer Segmentation Report (Arvato Financial Services)

Table of Contents:
1. Requirements
2. Run the Code
3. File Descriptions
4. Data
5. Project Motivation
6. Code Structure
7. Improvement Ideas
8. Author

---
## 1. Requirements
To run the code you need the following software:
- Python v.3+
- Jupyter Notebook
- Suggestion: Anaconda v.4+ since it has both in one suite.
- Install additional libraries, for example via pip:
    - `pip install xgboost`
    - `pip install imblearn`
    - `pip install skopt`  


__Note__: When you are reading most likely data files will not exist anymore due to the terms & conditions agreed with Arvato Financial Services for this project. If you want to access this data, please contact either Udacity or Arvato Financial Services directly.

## 2. Run the code
1. Fork the repository into your own computer
2. Unpack the 7z files into the same directory: 
    - _../data/Udacity_AZDIAS_052018.7z_ 
    - _../data/Udacity_CUSTOMERS_052018.7z_
    - _../data/Udacity_MAILOUT_052018_TEST.7z_
    - _../data/Udacity_MAILOUT_052018_TRAIN.7z_
3. Open the file _01-data-cleaning.ipynb_ and run all cells
4. (Only after the previous step is completed) Open the file _02-customer-segmentation.ipynb_ and run all cells
5. (Only after the previous step is completed) Open the file _03-customer-prediction.ipynb_ and run all cells

__Notes__: 
- When you are reading this it is likely that these files do not exist anymore due to the terms & conditions agreed with Arvato Financial Services for this project. If you want to access this data, please contact either Udacity or Arvato Financial Services directly.
- The Jupyter notebooks 2 and 3 may take some days to run depending on your CPU capacities. This was developed in the course of several days and due to the complexity of the data some tests needed to be run in order to make the best decisions.

## 3. File Descriptions
### 3.1 Data-related
- _../data/Udacity_AZDIAS_052018.7z_: Real-word data of a subset of the German population containing 366 features.
- _../data/Udacity_CUSTOMERS_052018.7z_: Real-word data of customers' data from Arvato Financial Services containing the same features as the population data + 3 additional columns that can be removed.
- _../data/Udacity_MAILOUT_052018_TRAIN.7z_: Real-word labeled data from Arvato Financial Services containing the same features as the population data + target variable.
- _../data/Udacity_MAILOUT_052018_TEST.7z_: Real-word unlabeled  data from Arvato Financial Services containing the same features as the population data that can be used to create predictions.
- _../data-dictionary/DIAS Attributes - Values 2017.xlsx_: Data dictionary with a description as well as the possible values for each features (some features may be missing here or are written differently).
- _../data-dictionary/DIAS Information Levels - Attributes 2017.xlsx_: Further information about to which information level (category) the features belong.

### 3.2 Code-related
- _01-data-cleaning.ipynb_: Jupyter notebook containing the data cleaning and processing part.
- _02-customer-segmentation.ipynb_: Jupyter notebook containing the customer segmentation part (unsupervised learning).
- _03-customer-prediction.ipynb_: Jupyter notebook containing the customer prediction part (supervised learning).

### 3.3 Models
- All models developed accross the project were deployed into the folder _..models/._ For further details about each model, I suggest to navigate through the Jupyter Notebooks 02 and 03.

## 4. Data
The data was provided by Arvarto Financial Services to be used solely in the context of this project:
- It contains demographic and consumer-behavioral information about a subset of the German population as well as the company's customers database.
- It is high-dimensional and requires a big amount of processing since there is missing data.
- Some features may be of type string and the majority is numeric. However, some of the numeric columns do not have an ordinal meaning, which is something to consider while encoding them when applying it in Machine Learning.
- The labeled data is very imbalanced with around 1% for the positive class.
- A description of each column and types of values can be found in the file _../data-dictionary/DIAS Attributes - Values 2017.xlsx_.

## 5. Project Motivation
This project was done as a capstone project for the [Udacity's Data Scientist Nanodegree](https://www.udacity.com/course/data-scientist-nanodegree--nd025). I decided to choose this project because I personally wanted to further investigate the topic of clustering and segmentation. Since it was dealing with real-world data, I thought it would be a great challenge.

The __main goals__ of this project were to:
1. Use unsupervised learning techniques to perform customer segmentation and to identify the parts of the population that best describe the core customer base of the company.
2. Use supervised learning techniques - possibly including the information gained in the customer segmentation part - and to create a model that is able to predict who may become a new customer.

__Summarized analysis__
- I wrote this [Medium post](https://medium.com/@brunoipfernandes/how-to-perform-data-driven-customer-segmentation-9becb18dc528) about how to employ the techniques I used for customer segmentation, so other professionals can try out this interesting data-driven approach.
- For the handling of the missing values, I employed a simplistic approach by treating the majority of the missing values as "unknown" values. This approach may or may not be the most suitable one, but I personally had the feeling that the data was not very pronounced in terms of its predicting or clustering capabilities. It would be ideal to have a domain expert at hand that could give more insight into this missing information and possibly also help engineering new features.
- The customer segmentation was the most enjoyable part for me because I think that the approach I employed worked well enough. The clusters were not that clearly separable, but still it was possible to derive some relatable information from the clusters' analysis.
- The customer prediction part did not produce the desired results, as I was expecting to include the clusters and the dimensionality reduction models from the previous section into the classification model. However, it turned out that including this information would only highly contribute negatively to the performance of the models. I then used all the data and employed different approaches to try and deal with the imbalanced data, but none produced good results for the positive class. Although the ROC-AUC or accuracy values were relatively good, the F1 score was very bad. 

__Personal note__: I am not sure if this data was sufficient or had a high quality for this task. Feel free to disagree and let me know where you would improve.

## 6. Code Structure
### PART 1: Clean and Prepare the Data (file: _01-data-cleaning.ipynb_)
1. Data cleaning assessment
    1. Deal with columns with high percentage of missing data
    2. Deal with rows with high percentage of missing data
    3. Deal with columns that do not hold any relevant information or are redundant.
    4. Deal with missing data
        1. Deal with missing data for columns with information available in the data dictionary - Part 1
        2. Deal with missing data for columns with information available in the data dictionary - Part 2   
    5. Encode categorical variables
    6. Feature engineering
    7. Data harmonization  
2. Build data cleaning function
3. Clean datasets

### PART 2: Customer Segmentation (Unsupervised Learning) (file: _02-customer-segmentation.ipynb_)
1. Dimensionality reduction
2. Clustering
    1. Find best number of clusters
    2. Cluster analysis
3. Customer segmentation report
4. Model deployment

### PART 3: Customer Prediction (Supervised Learning) (file: _03-customer-prediction.ipynb_)
1. Target variable analysis
2. Build the ML pipeline
3. Model selection
4. Hyperparameter tuning
5. Model training & evaluation
6. Prediction on the new data
7. Final analysis
8. Model deployment

## 7. Improvement Ideas
- Make a more precise feature selection with the help of a domain expert, as some of the features may not have any importance or are redundant.
- Put more focus on feature engineering with the help of a domain expert to create more powerful features that add new relevant information to the dataset.
- Try different clustering algorithms like density-based ones (i.e., DBSCAN) and see if they work better for the clustering part with this dataset.
- Try out further approaches in the prediction part like using alternative resampling techniques or including the threshold for the prediction in the deployment configuration. The latter could be achieved based on the predicted probability following this approach:
    1. Get the predicted probabilities for the positive class.
    2. Decide on a new threshold.
    3. Classify samples based on this new threshold. 

## 8. Author
Bruno Fernandes - Data Enthusiast - [LinkedIn](https://www.linkedin.com/in/b-fernandes/) - [Xing](xing.to/brunofernandes)