def clean_reklama5(**kwargs):
    ti = kwargs['ti']
    kwargs['ti'].xcom_push(key='cleaned_data', value=ti)
