import json
import plotly
import pandas as pd
import sqlite3
import re

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request
from plotly.graph_objs import Bar
import joblib


app = Flask(__name__)

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

# load data
database_filepath = "../data/DisasterResponse.db"
conn = sqlite3.connect(database_filepath)
df = pd.read_sql_query('SELECT * FROM DisasterResponse', conn)

# remove rows which do not have any label as they will not provide any prediction
label_cols = df.drop(["id","message","original","genre","related","child_alone"], axis=1).columns
df['sum'] = df[label_cols].sum(axis=1)
df = df[df['sum'] != 0]
df = df.drop(["sum"], axis=1)

df = df.drop(["related","child_alone"], axis=1)

# load model
model = joblib.load("../models/dr_classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    genre_counts = df.groupby('genre').count()['message']
    genre_names = list(genre_counts.index)

    label_counts = df[df.columns[4:]].sum().reset_index().rename(columns={'index': 'Label', 0: 'Number of Messages'}).sort_values('Number of Messages', ascending=False)
    
    # create visuals
    # TODO: Below is an example - modify to create your own visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=genre_names,
                    y=genre_counts
                )
            ],

            'layout': {
                'title': 'Distribution of the Message Genres',
                'yaxis': {
                    'title': "Count"
                },
                'xaxis': {
                    'title': "Genre"
                }
            }
        },
        {
            'data': [
                Bar(
                    x=label_counts['Label'],
                    y=label_counts['Number of Messages'],
                    marker=dict(color='rgb(85, 175, 85)')
                )
            ],

            'layout': {
                'title': 'Distribution of the Labels',
                'yaxis': {
                    'title': "Number of messages with the label"
                },
                'xaxis': {
                    'title': "Label"
                },
                'margin': {
                'b': 150
                }
            }
        }        
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='127.0.0.1', port=3001, debug=True)


if __name__ == '__main__':
    main()