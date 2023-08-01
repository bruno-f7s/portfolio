# import libraries
###################################################################################################################
import sys
import re
import sqlite3
import pandas as pd

import nltk
nltk.download(['wordnet'])
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.multioutput import MultiOutputClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import classification_report, make_scorer, accuracy_score, recall_score, f1_score

import joblib

# define processing functions
###################################################################################################################
def load_data(database_filepath):
    """
    The function takes in a file path to SQL lite database and returns the features X and labels Y as well as the labelling columns for that data.
    Additionally it removes any labelling columns which only have one category (1/0), since it will not have any prediction power.

    Parameters:
        database_filepath (str): The file path to the SQL lite database name. Example: "your_database.db". It is expected that the database is located in the "data" folder.

    Returns:
        X (dataframe): The independent variables or features. It is expected to be a single feature with text information.
        y (dataframe): The target variables or labels.
        category_names (list): The list of the target variables or labels.
    """
    
    # set up connection and query
    database_nm = database_filepath.replace(".db", "")
    conn = sqlite3.connect(database_filepath)
    query = "SELECT * FROM '{}'".format(database_nm)

    # load the data into a pandas df
    df = pd.read_sql_query(query, conn)

    # get the list of labelling columns 
    category_names = list(df.drop(["id","message","original","genre"], axis=1).columns)
  
    # remove any labels from the list that only have one category (1/0) 
    for col in category_names:
        if len(df[col].value_counts()) == 1:
            category_names.remove(col)

    # create X and y variables
    X = df["message"]
    y = df[category_names]

    return X, y, category_names


def tokenize(text):
    """
    - This function takes in a string, tokenizes it, removes English stop words and applies lemmatization. 
    - The result is a list of all resulting tokens. 
    - The function can be passed into a tokenizer of a sklearn transformer so that the input will the string of each row on the dataframe.

    Parameters:
        text (str): A single string or if passed into a tokenizer of a sklearn transformer it will treat the string of each row of the dataframe.

    Return:
        clean_tokens (list): A list of the resulting tokens for the passed string after the tokenization processing.
    """
    #tokenize text
    tokens = word_tokenize(text)
    
    #stop word removal
    tokens = [tok.lower().strip() for tok in tokens if tok not in stopwords.words("english")]

    #lemmatization of words
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(tok, pos='v') for tok in tokens]

    #remove tokens that only contain special characters
    clean_tokens = [tok for tok in lemmatized_tokens if not re.match("^[\W_]+", tok)]
    
    #remove tokens that contain digits as they will not be relevant for this supervised learning problem
    clean_tokens = [tok for tok in clean_tokens if not re.search("\d", tok)]
    
    return clean_tokens


# create a class for a custom transformer to count words in a string
class WordCounter:
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return [[len(text.split())] for text in X]


# create a for custom transformer to measure the length of a string
class CharacterCounter:
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        return [[len(text)] for text in X]    


def build_model():
    """
    - This function builds a pipeline for a Gradient Boosting Classifier using a grid search for multiple parameter combinations and a 5-fold crossvalidation.
    - The function is particularly built for a multi-labelling problem using as features a single column containing text information. 

    returns:
        model (class): the pipeline to be used for fitting and predicting multiple labels.

    """

    # build pipeline
    pipeline = Pipeline([
        ('features', FeatureUnion([
            ('tfidf', TfidfVectorizer(tokenizer=tokenize)),
            ('token_count', CountVectorizer(tokenizer=tokenize)),
            ('word_count', Pipeline([
                ('count', WordCounter()),
                ('scale', StandardScaler())
            ])),
            ('character_count', Pipeline([
                ('count', CharacterCounter()),
                ('scale', StandardScaler())
            ]))
        ])),
        ('lr', MultiOutputClassifier(OneVsRestClassifier(LogisticRegression())))
    ])
    
    # define parameter grid
    param_grid = {
        "lr__estimator__estimator__C": [1, 5, 10],
        "lr__estimator__estimator__max_iter": [5000],
        "lr__estimator__estimator__solver": ['saga', 'lbfgs'],
        "lr__estimator__estimator__multi_class": ['ovr'],
        "lr__estimator__estimator__class_weight": ['balanced'],
        "lr__estimator__estimator__n_jobs": [-1]
    }

    # Define the scoring metrics
    scoring = {
        'accuracy': make_scorer(accuracy_score),
        'recall': make_scorer(recall_score, average='weighted', zero_division=1),
        'f1': make_scorer(f1_score, average='weighted', zero_division=1)
    }

    model = GridSearchCV(pipeline, param_grid=param_grid, cv=5, scoring=scoring, return_train_score=True, refit="f1", verbose=1)

    return model


def evaluate_model(model, X_test, y_test, category_names):
    """
    This function takes in the best model and evaluates the predictions. It prints out:
    - the overall accuracy.
    - the best score of the model.
    - the best parameters of the model.
    - the precision, recall and f1 scores for each label.

    Parameters:
        model (class): the fitted model.
        X_test (dataframe): the testing dataframe containing the features from the train-split.
        y_test (dataframe): the testing dataframe containing the labelling columns from the train-split.
        category_names (list): the list of labelling columns.

    returns:
        best_params (dict): the best parameters for the best model       
    """

    # Predict on the test set and evaluate the performance
    y_pred = model.predict(X_test)

    # Get the best evaluation metric score and parameters
    best_score = model.best_score_
    best_params = model.best_params_

    # Evaluate the overall accuracy
    accuracy = (y_test == y_pred).mean()

    # Print the results
    print(f"Best Parameters: {best_params}")
    print(f"Best Score: {best_score}")
    print(f"Overall accuracy: {accuracy}" )
    print(classification_report(y_test, y_pred, target_names=category_names, zero_division=1))

    return best_params

def build_final_model(best_params, X, y):
    """
    Builds and fits the final model using the whole dataset and the best paramaters found using GridSearchCV.

    Parameters:
        best_params (dict): the best parameters for the best model       
        X_test (dataframe): the whole dataframe containing the features.
        y_test (dataframe): the whole dataframe containing the labelling columns.

    returns:
        final_model (class): the fitted final model using the whole dataset.      
    """

    # extract parameters
    def extract_best_params(best_params):
        for key, values in best_params.items():
            if "estimator__C" in key:
                C = values
            elif "max_iter" in key:
                max_iter = values                    
            elif "solver" in key:
                solver = values 
            elif "multi_class" in key:
                multi_class = values  
            elif "class_weight" in key:
                class_weight = values                                                   
        return C, max_iter, solver, multi_class, class_weight
    
    C, max_iter, solver, multi_class, class_weight = extract_best_params(best_params)

    # build the model with extracted parameters
    final_model = Pipeline([
        ('features', FeatureUnion([
            ('tfidf', TfidfVectorizer(tokenizer=tokenize)),
            ('token_count', CountVectorizer(tokenizer=tokenize)),
            ('word_count', Pipeline([
                ('count', WordCounter()),
                ('scale', StandardScaler())
            ])),
            ('character_count', Pipeline([
                ('count', CharacterCounter()),
                ('scale', StandardScaler())
            ]))
        ])),
        ('lr', MultiOutputClassifier(OneVsRestClassifier(LogisticRegression(C=C, max_iter=max_iter, solver=solver, multi_class=multi_class, class_weight=class_weight, n_jobs=-1))))
    ])

    # fit the model using the whole dataset
    final_model.fit(X, y)

    return final_model


def save_model(model, model_filepath):
    """
    Exports the model as a pickle file in the passed file path.

    Parameters:
        model (class): the fitted final model.
        model_filepath (str): a string containing the directory and name of the pickle file.

    """
    joblib.dump(model, model_filepath)


# define main function
###################################################################################################################
def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, y, category_names = load_data(database_filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, y_train)
        
        print('Evaluating model...')
        best_params = evaluate_model(model, X_test, y_test, category_names)

        print('Building final model with best parameters...')
        final_model = build_final_model(best_params, X, y)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(final_model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py DisasterResponse.db classifier.pkl')


# run the code
###################################################################################################################
if __name__ == '__main__':
    main()
