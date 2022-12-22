#!/usr/bin/env python
# coding: utf-8

# In[1]:


    #get_ipython().system('python3 --version')


    #get_ipython().system('jupyter --version')


#pip install pyspark
#pip install findspark
#pip install pandas
#pip install numpy
#pip install matplotlib




import sys  
#import pandas 
#pandas.__version__


# In[1]:


import warnings
warnings.filterwarnings('ignore')
import findspark
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
from pyspark.sql.types import *
from pyspark.sql import Row
#import seaborn as sns
#import pandas as pd pandas dont work
#pd.options.display.mpl_style = 'default'
from pyspark import SparkContext
from pyspark import SQLContext
findspark.init()

import argparse

import os

sparkClassPath="/home/bigdata/postgresql-42.5.1.jar"

postgresJarPackage="org.postgresql:postgresql-42.5.1"


#sparkClassPath = os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.postgresql:postgresql:42.5.1 pyspark-shell'
from pyspark.sql import SparkSession




def main(params):
    user = params.user
    password = params.password
    host = params.host
    port =params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = "/home/bigdata/yellow_tripdata_2022-01.csv"

    #download csv
    os.system(f"wget {url} -0 {csv_name}")    
    
    sc = SparkSession.builder \
              .appName("Churn data Analysis") \
              .master("local[*]") \
              .config("spark.driver.extraClassPath", sparkClassPath) \
              .config("spark.jar.postgresJarPackage", postgresJarPackage) \
              .getOrCreate()

#spark_con = SparkContext(sc=sc)
    spark = SQLContext(sc)
    print("Explore the data and analysis the assignment")


    df = spark.read.csv("csv_name", header=True, inferSchema=True)

# # Create a connection to postgresql creating ETL pipeline
    url = f"jdbc:postgresql://{host}:{port}/{db}"
    table = f"{table_name}"
    driver = "org.postgresql.Driver"
    user = f"{user}"
    password = f"{password}"


# Solving the issues is using your port number that point to the port
    df.write.format('jdbc').option("driver", driver).option("url", url).option("dbtable", table).option("user", user).option("password", password).save()




#add the env variables name using python argparser
#user, password, host, port, databasename, tablename, url of csv

if __name__=="__main__":

        parser = argparse.ArgumentParser(description='Ingest NY taxi data to postgresql')
        parser.add_argument('--user', help='user to postgresql')
        parser.add_argument('--password', help='password to postgresql')
        parser.add_argument('--host', help='host name to postgresql')
        parser.add_argument('--port', help='port name to postgresql')
        parser.add_argument('--db', help='database name to postgresql')
        parser.add_argument('--table_name', help='table name to postgresql')
        parser.add_argument('--url', help='url of the csv file')


        args =parser.parse_args()
             
        main(args)



# # Create a connection to postgresql creating ETL pipeline
# url = "jdbc:postgresql://0.0.0.0:5431/ny_taxi"
# table = "yellow_tripdata"
# driver = "org.postgresql.Driver"
# user = "root"
# password = "root"


# # Solving the issues is using your port number that point to the port
# df.write.format('jdbc').option("driver", driver).option("url", url).option("dbtable", table).option("user", user).option("password", password).save()


