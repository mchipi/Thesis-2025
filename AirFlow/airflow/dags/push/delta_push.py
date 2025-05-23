import pandas as pd
import requests
import numpy as np

def push_delta(**kwargs):
    ti = kwargs['ti']
    cleaned_data = ti.xcom_pull(task_ids='clean_delta', key='cleaned_data')

    df = pd.DataFrame.from_dict(cleaned_data)
    df = df.replace({np.nan: None})

    api_url = 'http://flask-api:5000/api/property'

    data_to_send = df.to_dict(orient='records')
   
    print("Delta - fake push")



