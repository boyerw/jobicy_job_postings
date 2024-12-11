import json
import sys

# Get json data from API
import requests
import json

# Import the AWS Glue libraries
import pandas as pd
from pandas import DataFrame
import datetime
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

# How to access the parameters passed to the glue job in Terraform
args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "s3_bucket",
#         "source_path",
        "target_path",
#         "compression",
#         "partition_cols"
    ]
)

# Main entry point for Spark functionality, connection to a Spark cluster
sc = SparkContext()
# Glue wrapper to provide additional features on top of Spark
glueContext = GlueContext(sc)
# Spark Session, the entry point to programming Spark with the Dataset and DataFrame API
spark = glueContext.spark_session
# Instanciate a Glue Job with the Glue context
job = Job(glueContext)
# Initialize the Job
job.init(args["JOB_NAME"], args)

# Get data from Jobicy API
API_URL = "https://jobicy.com/api/v2/remote-jobs?&industry=data-science"
response = requests.get(API_URL)
response.raise_for_status()
json_response = json.loads(response.content)

# Convert JSON data to Pandas DataFrame
df = pd.json_normalize(json_response['jobs'])

# Remove null values in numeric columns
df['salaryMissing'] = (df.loc[:, 'annualSalaryMin'].isna() + df.loc[:, 'annualSalaryMax'].isna()) > 0
df.loc[:, ['annualSalaryMin','annualSalaryMax']] = df.loc[:, ['annualSalaryMin','annualSalaryMax']].fillna(value=0, axis=0)
df['annualSalaryMin'] = df['annualSalaryMin'].copy().astype(int)
df['annualSalaryMax'] = df['annualSalaryMax'].copy().astype(int)

# Typing
numeric_cols = ['annualSalaryMin', 'annualSalaryMax', 'salaryMissing']
for col in df.columns:
    if col in numeric_cols: continue
    df[col] = df[col].copy().astype('string')        
    
df['annualSalaryMin'] = df['annualSalaryMin'].copy().astype(int)
df['annualSalaryMax'] = df['annualSalaryMax'].copy().astype(int)
df['salaryMissing'] = df['salaryMissing'].copy().astype(bool)

# Enrich with metadata 
df["loadDate"] = datetime.date.today()

# Generate a Spark DataFrame from Pandas DataFrame
dest_sdf = spark.createDataFrame(df)

# Generate a  Glue DynamicFrame from Spark DataFrame
dest_gdf = DynamicFrame.fromDF(dest_sdf, glueContext, "dest_gdf")

connection_options = (
    {
        "path": f"s3://{args['s3_bucket']}/{args['target_path']}",
    }
)

# Write the previous Glue DynamicFrame to a parquet file in a given S3 path
datasink = glueContext.write_dynamic_frame.from_options(
    frame=dest_gdf,
    connection_type="s3",
    format="csv",
    connection_options=connection_options,
    # format_options={"compression": args["compression"]},
    transformation_ctx="datasink",
)

job.commit()
