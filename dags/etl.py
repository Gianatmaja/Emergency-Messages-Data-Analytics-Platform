from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import numpy as np
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
from Helpers import tokenize, get_ln_id, get_date_id, get_cat_id
import joblib
from smart_open import smart_open
import s3fs
from sqlalchemy import create_engine
pd.options.mode.chained_assignment = None

def start_DAG():
    # Dummy DAG to initiate process
    out = 'DAG started'
    return out

def data_quality_check():
    
    # Input AWS Key ID
    aws_key = 
    # Input AWS Secret Key ID
    aws_secret = 
    
    # Input bucket name
    bucket_name = 
    # Input path to object, e.g csv file
    object_key = 
    
    path = 's3://{}:{}@{}/{}'.format(aws_key, aws_secret, bucket_name, object_key)

    # Read data
    df = pd.read_csv(smart_open(path))

    relevant_columns = ['ID', 'date', 'labeled', 'message', 'language', 'related', 'request', 'aid_related', 
                        'medical_help', 'medical_products', 'search_and_rescue', 'security', 'military', 'water', 
                        'food', 'shelter', 'clothing', 'money', 'missing_people', 'refugees', 'death', 'other_aid',
                        'infrastructure_related', 'transport', 'buildings', 'electricity', 'tools', 'hospitals', 
                        'shops', 'aid_centers', 'other_infrastructure', 'weather_related', 'floods', 'storm', 
                        'fire', 'earthquake', 'cold', 'other_weather', 'direct_report']
    
    df = df[relevant_columns]
    
    index_fail = []
    # Check data completeness
    for i in range(len(df)):
        row = df.iloc[i]
        condition1 = pd.notnull(row['date'])
        condition2 = pd.notnull(row['message'])
        condition3 = isinstance(row['message'], str)
        
        if ((condition1 & condition2 & condition3) == True):
            print("Data Quality Test for Row {}: Passed".format(i))
        else:
            index_fail.append(i)
            print("Data Quality Test for Row {}: Failed. Please Check Data".format(i))
    # Keep good data
    if (len(index_fail) > 0):
        df_checked = df.drop(df.iloc[index_fail].index)
        df_checked = df_checked.reset_index()
        df_checked.drop('level_0', axis = 1, inplace = True)
    else:
        df_checked = df
        
    relevant_columns = ['ID', 'date', 'labeled', 'message', 'language', 'related', 'request', 'aid_related', 
                        'medical_help', 'medical_products', 'search_and_rescue', 'security', 'military', 'water', 
                        'food', 'shelter', 'clothing', 'money', 'missing_people', 'refugees', 'death', 'other_aid',
                        'infrastructure_related', 'transport', 'buildings', 'electricity', 'tools', 'hospitals', 
                        'shops', 'aid_centers', 'other_infrastructure', 'weather_related', 'floods', 'storm', 
                        'fire', 'earthquake', 'cold', 'other_weather', 'direct_report']
    
    df_checked = df_checked[relevant_columns]
    print("\nAll tests completed.")
    
    # Input destination bucket and desired filename
    bucket name = 
    file_name = 
    
    # Write to processing layer
    bytes_to_write = df_checked.to_csv(None).encode()
    fs = s3fs.S3FileSystem(key=aws_key, secret=aws_secret)
    with fs.open('s3://{}/{}'.format(bucket_name, file_name), 'wb') as f:
        f.write(bytes_to_write)
        

def predict_categories():

    # Input AWS Key ID
    aws_key = 
    # Input AWS Secret Key ID
    aws_secret = 
    
    # Input bucket name
    bucket_name = 
    # Input path to object, e.g csv file
    object_key = 
    
    path = 's3://{}:{}@{}/{}'.format(aws_key, aws_secret, bucket_name, object_key)

    # Read data
    df = pd.read_csv(smart_open(path))
    # Load predictor
    Pipeline = joblib.load('Prediction_Pipeline.joblib')
    
    X = df[['ID', 'date', 'labeled', 'message', 'language']]
    y = df[['related', 'request', 'aid_related', 'medical_help', 'medical_products', 'search_and_rescue', 
            'security', 'military', 'water', 'food', 'shelter', 'clothing', 'money', 'missing_people', 'refugees', 
            'death', 'other_aid', 'infrastructure_related', 'transport', 'buildings', 'electricity', 'tools', 
            'hospitals', 'shops', 'aid_centers', 'other_infrastructure', 'weather_related', 'floods', 'storm', 
            'fire', 'earthquake', 'cold', 'other_weather', 'direct_report']]
    
    Pred_df = pd.DataFrame(columns = ['related', 'request', 'aid_related', 'medical_help', 'medical_products',
                                      'search_and_rescue', 'security', 'military', 'water', 'food', 'shelter',
                                      'clothing', 'money', 'missing_people', 'refugees', 'death', 'other_aid',
                                      'infrastructure_related', 'transport', 'buildings', 'electricity',
                                      'tools', 'hospitals', 'shops', 'aid_centers', 'other_infrastructure',
                                      'weather_related', 'floods', 'storm', 'fire', 'earthquake', 'cold',
                                      'other_weather', 'direct_report'])
    # Predict class
    for i in range(len(X)):
        if (X['labeled'][i] == 1):
            Pred_df = Pred_df.append(y.iloc[i], ignore_index = True)
        else:
            pred = Pipeline.predict(X['message'].iloc[i:(i+1)])
            y_pred = pd.Series(pred[0], index = ['related', 'request', 'aid_related', 'medical_help', 
                                                 'medical_products','search_and_rescue', 'security', 'military', 
                                                 'water', 'food', 'shelter','clothing', 'money', 'missing_people', 
                                                 'refugees', 'death', 'other_aid', 'infrastructure_related', 
                                                 'transport', 'buildings', 'electricity', 'tools', 'hospitals', 
                                                 'shops', 'aid_centers', 'other_infrastructure', 'weather_related', 
                                                 'floods', 'storm', 'fire', 'earthquake', 'cold', 'other_weather', 
                                                 'direct_report'])
            Pred_df = Pred_df.append(y_pred, ignore_index = True)
    # Determine level of emergency
    Sums = Pred_df.sum(axis = 1)
    Category = []
    for j in range(len(Sums)):
        s = Sums[j]
        if (s == 0):
            Category.append('N/A')
        elif (s == 1):
            Category.append('Low')
        elif (s <= 3):
            Category.append('Med')
        else:
            Category.append('High')
    
    Pred_df['category'] = Category
    
    Concat_df = pd.concat([X, Pred_df], axis = 1)
    
    # Input destination bucket and desired filename
    bucket name = 
    file_name = 
    
    # Write to processing layer
    bytes_to_write = Concat_df.to_csv(None).encode()
    fs = s3fs.S3FileSystem(key=aws_key, secret=aws_secret)
    with fs.open('s3://{}/{}'.format(bucket_name, file_name), 'wb') as f:
        f.write(bytes_to_write)


def get_fact_table():
    
    # Input AWS Key ID
    aws_key = 
    # Input AWS Secret Key ID
    aws_secret = 
    
    # Input bucket name
    bucket_name = 
    # Input path to object, e.g csv file
    object_key = 
    
    path = 's3://{}:{}@{}/{}'.format(aws_key, aws_secret, bucket_name, object_key)

    # Read data
    df = pd.read_csv(smart_open(path))
    # Transformations for dim and fact tables
    lan_id = [get_ln_id(l) for l in df['language'].values]
    date_id = [get_date_id(d) for d in df['date'].values]
    cat_id = [get_cat_id(c) for c in df['category'].values]
    
    df['language_ID'] = lan_id
    df['date_ID'] = date_id
    df['category_ID'] = cat_id
    
    df_fact = df.drop(['language', 'date', 'category'], axis = 1)
    df.drop(['language_ID', 'date_ID', 'category_ID'], axis = 1, inplace = True)
    
    relevant_columns = ['ID', 'date_ID', 'labeled', 'message', 'language_ID', 'related', 'request', 'aid_related', 
                        'medical_help', 'medical_products', 'search_and_rescue', 'security', 'military', 'water', 
                        'food', 'shelter', 'clothing', 'money', 'missing_people', 'refugees', 'death', 'other_aid',
                        'infrastructure_related', 'transport', 'buildings', 'electricity', 'tools', 'hospitals', 
                        'shops', 'aid_centers', 'other_infrastructure', 'weather_related', 'floods', 'storm', 
                        'fire', 'earthquake', 'cold', 'other_weather', 'direct_report', 'category_ID']
    # Finalise fact table
    df_fact = df_fact[relevant_columns]
    # Insert into Redshift
    path_cred = 'postgresql://username:password@yoururl.com:5439/yourdatabase'
    table_name = 
    
    conn = create_engine(path_cred)

    df_fact.to_sql(table_name, conn, index = False, if_exists = 'append')

    
def end_DAG():
    # Dummy DAG to end process
    out = 'DAG completed'
    return out
    
with DAG(dag_id="Msg_Classifier",
         start_date=datetime(2021,1,1),
         schedule="@hourly",
         catchup=False) as dag:
    
    task1 = PythonOperator(
        task_id="Start_DAG",
        python_callable=start_DAG)
    
    task2 = PythonOperator(
        task_id="Data_quality_check",
        python_callable=data_quality_check)

    task3 = PythonOperator(
        task_id="ML_predictions",
        python_callable = predict_categories)
    
    task4 = PythonOperator(
        task_id="Load_into_DWH",
        python_callable=get_fact_table)

    task5 = PythonOperator(
        task_id="End_DAG",
        python_callable = end_DAG)
    
task1 >> task2 >> task3 >> task4 >> task5    
