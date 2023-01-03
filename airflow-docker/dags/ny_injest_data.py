import os


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





sparkClassPath="/home/bigdata/postgresql-42.5.1.jar"

postgresJarPackage="org.postgresql:postgresql-42.5.1"


#sparkClassPath = os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.postgresql:postgresql:42.5.1 pyspark-shell'
from pyspark.sql import SparkSession




def main(user, password, host, port, db, table_name, csv_file):

    csv_file = "/home/bigdata/yellow_tripdata_2022-01.csv"

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






# # Create a connection to postgresql creating ETL pipeline
# url = "jdbc:postgresql://0.0.0.0:5431/ny_taxi"
# table = "yellow_tripdata"
# driver = "org.postgresql.Driver"
# user = "root"
# password = "root"


# # Solving the issues is using your port number that point to the port
# df.write.format('jdbc').option("driver", driver).option("url", url).option("dbtable", table).option("user", user).option("password", password).save()


