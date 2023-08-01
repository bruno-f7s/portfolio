# import libraries
####################################################################################
import sys
import pandas as pd
from sqlalchemy import create_engine

# define functions
####################################################################################
def load_data(messages_filename, categories_filename):
    """
    This functions takes in two names of the csv files containing messages and categories data and returns a pandas dataframe of the merged datasets.
    The function expects the files in the same directory as the script.

    Parameters:
        messages_filename (str): file name of the messages csv file. Example: your_file.csv.
        categories_filename (str): file path to the categories csv file. Example: your_file.csv.

    Returns:
        df (dataframe): merged datasets
    """

    # load messages dataset
    messages_df = pd.read_csv(filepath_or_buffer=messages_filename, encoding="utf-8")

    # load categories dataset
    categories_df = pd.read_csv(filepath_or_buffer=categories_filename, encoding="utf-8")

    # merge both datasets
    df = pd.merge(messages_df, categories_df, on='id', how='inner')

    return df


def clean_data(df):
    """
    This function takes in the merged datasets and returns the cleaned dataframe. It applies the following cleaning steps:
        1. Transform the "categories" string column into as many columns as label categories available.
        2. For each label category it extracts the value 0 or 1, depending whether the category was labelled for the current message (row).
        3. Removes duplicate rows.
        4. Removes rows with Null values in the label categories.
        5. Replaces all values of 2 with 1 in  the label categories.  

    Parameters:
        df (pandas dataframe): merged datasets of messages and categories

    Returns:
        df (pandas dataframe): cleaned dataset
    """

    # create a dataframe of the 36 individual category columns
    categories_df = df["categories"].str.split(pat=";", expand=True)

    # select the first row of the categories dataframe to create a list of column names for the label categories
    row = categories_df.loc[0]
    category_colnames = row.apply(lambda x: x[:-2]).tolist()

    # rename the columns of the categories_df
    categories_df.columns = category_colnames

    # convert category values to 0 or 1
    for column in categories_df.columns:
        # set each value to be the last character of the string
        categories_df[column] = categories_df[column].str[-1]
    
        # convert column from string to numeric
        categories_df[column] = categories_df[column].astype(int)

    # replace the "categories" column in df with new category columns
    df = df.drop("categories", axis=1)
    df = pd.concat([df, categories_df], axis=1)
    
    # remove any possible duplicates
    df = df.drop_duplicates()

    # remove all rows where the categories include null values
    for column in categories_df.columns:
       df = df[df[column].notna()]

    # replace 2s with 1s
    for col in df.columns:
        df[col] = df[col].replace(2.,1.)

    return df

def save_data(df, database_filename):
    """
    The function creates a SQL lite database in the current directory for a passed dataframe.

    Parameters:
        df (pandas dataframe): final dataset to be saved.
        database_filename (str): the file name for the SQL lite database. Example: your_db_name.
    """
    engine = create_engine(f"sqlite:///{database_filename}")
    df.to_sql(database_filename.replace(".db",""), engine, index=False)


def main():
    if len(sys.argv) == 4:

        messages_filename, categories_filename, database_filename = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filename, categories_filename))
        df = load_data(messages_filename, categories_filename)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filename))
        save_data(df, database_filename)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')

# run the main code
if __name__ == '__main__':
    main()