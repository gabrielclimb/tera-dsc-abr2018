import os
import boto3
from boto3 import s3
import pandas as pd

import gc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

s3_bucket = boto3.client('s3')
S3_BUCKET = 'rayssak-tera'
S3_DIRETORIO = '/data/avazu/'

def get_invalid(df):
    df_invalid = ( (df.isnull().sum()+get_invalid_quotes(df).sum() ) / len(df)) * 100
    df_invalid = df_invalid.drop(df_invalid[df_invalid == 0].index).sort_values(ascending=False)
    return (df_invalid)

def get_invalid_quotes(df):
    
    tmp = pd.DataFrame(None, columns=df.columns)
    ncols = len(df.columns)
    aux = 0
    
    while aux < ncols:
        
        current_col = df.columns[aux]
        if not df[current_col].isnull().all().any():
            col_content = df[current_col].tolist()
            invalid = len([row for row in col_content if row == '\"\"'])
            tmp.loc[len(tmp)-1, current_col] = invalid
        aux += 1
        
    return (tmp.fillna(0))

def print_invalid(df):
    if len(df) > 0:
        f, ax = plt.subplots(figsize=(15, 9))
        plt.xticks(rotation='90')
        sns.barplot(x=df.index, y=df)
        ax.set(title='Atributos invalidos', ylabel='% invalido')
    else:
        print ('Dataframe sem valores invalidos.')
    
def save_data(data, name):
    print (S3_BUCKET + S3_DIRETORIO + name)
    s3_bucket.put_object(Body=data.to_csv(None, encoding='utf-8'), Bucket=S3_BUCKET, Key=S3_DIRETORIO + name)