
import os
from datetime import datetime
from airflow import DAG

from airflow.utils.dates  import days_ago
from airflow.operators.bash import BashOperator
from airflow.operatoor.python import PythonOperator
from ny_injest_data import main


#using the environ path in airflow

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

PG_HOST=os.getenv('PG_HOST')
PG_USER=os.getenv('PG_USER')
PG_PASSWORD=os.getenv('PG_PASSWORD')
PG_PORT=os.getenv('PG_PORT')
PG_DATABASE=os.getenv('PG_DATABASE')

#Create a DAG and give it a name and time scheduler and date

local_workflow = DAG(

    "LocalIngestion",
     shedule_interval="0 6 2 * *",
     start_date= datetime(2022, 1, 1)
     )

#Downloading url into Airflow using curl or wget
URL_PREFIX = "https://yellow+tripdata"

URL_TEMPLATE = URL_PREFIX + '/{{execution_date.striftime(\'%Y-%m\')}}.parquet'
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_{{execution_date.striftime(\'%Y-%m\')}}.parquet'
TABLE_NAME = 'yellow_tripdata_{{execution_date.striftime(\'%Y_%m\')}}'

#creating a workflow

with local_workflow:
#need to specify theeeeeeeeeeeeeeee BashOperator
    wget_task = BashOperator(
        task_id = 'wget',
        #bash_command = f'curl -sSL {url} -0 {AIRFLOW_HOME}/output.csv'    #save the url to Airflow home output
        bash_command = f'curl -sSL {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE }'  #SHOWING THE SPECIFIC DATE TASK ARE RUN
    )
    
   # we can pass the function parameters 

    ingest_task = PythonOperator(
        task_id = 'ny_data',
        python_data = main,
        op_kwargs=dict(user=PG_USER,password=PG_PASSWORD,host=PG_HOST,port=PG_PORT,db=PG_DATABASE,table_name=TABLE_NAME,csv_file=OUTPUT_FILE_TEMPLATE), 

    )


    wget_task >> ingest_task