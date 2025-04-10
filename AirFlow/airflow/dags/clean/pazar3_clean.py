def clean_pazar3(**kwargs):
    ti = kwargs['ti']
    kwargs['ti'].xcom_push(key='cleaned_data', value=ti)
