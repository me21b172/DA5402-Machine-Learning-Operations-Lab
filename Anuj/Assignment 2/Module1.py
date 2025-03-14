from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import datetime
import sys
sys.path.insert(0, 'C:/Users/aksha/OneDrive/Desktop/codes/CP/DA5402-Machine-Learning-Operations-Lab/Anuj/Assignment 1')
from Module1AndModule2Web_scrapping import extract_top_stories

# Define the Python function to be used in the PythonOperator
def my_function(x):
    return x + " is a must-have tool for Data Engineers."

# Default arguments for the DAG
default_args = {
    'owner': 'Anuj',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}
print(extract_top_stories())
# Define the DAG using a context manager for better readability
with DAG(
    dag_id="python_operator",
    default_args=default_args,
    start_date=datetime.datetime(2025, 2, 8),  # Updated to current or recent date
    schedule_interval="@daily",  # Use `schedule_interval` instead of `schedule`
    catchup=False,  # Prevent backfilling of missed runs
) as dag:

    # Define the PythonOperator task
    t1 = PythonOperator(
        task_id='print',
        python_callable=my_function,
        op_kwargs={"x": "Apache Airflow"},
    )
