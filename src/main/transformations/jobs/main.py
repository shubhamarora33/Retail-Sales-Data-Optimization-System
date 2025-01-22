import os
from http.client import responses

from mysql.connector import connect

from resources.dev import config
from resources.dev.config import aws_access_key, aws_secret_key, bucket_name, local_directory
from src.main.download.aws_file_download import S3FileDownloader
from src.main.read.aws_read import S3Reader
from src.main.utility.encrypt_decrypt import *
from src.main.utility.logging_config import logger
from src.main.utility.s3_client_object import *
from src.main.utility.my_sql_session import *
from src.main.read import *
from src.main.utility.spark_session import spark_session
from src.test.scratch_pad import s3_client, s3_client_provider, folder_path, s3_absolute_file_path

################# Get S3 Client ###############
aws_access_key = config.aws_access_key
aws_secret_key = config.aws_secret_key

s3_client_provider = s3_client_provider(decrypt(aws_access_key), decrypt(aws_secret_key))
s3_client = s3_client_provider.get_client()

# Now you can use s3_client for your s3 operations
response = s3_client.list_buckets()
logger.info("List of Buckets: %s", response['Buckets'])

#check if local directory has already a file
# if file is there then check if the same file is present in the staging area
# with status as A. It so then don't delete and try to re-run
# Else give an error and not process the next file
csv_files = [file for file in os.listdir(config.local_directory) if file.endswith(".csv")]
connection = get_mysql_connection()
cursor = connection.cursor()

total_csv_files = []
if csv_files:
    for file in csv_files:
        total_csv_files.append(file)
    statement = f"""
    select distinct file_name from
    youtube_project.product_staging_table
    where file_name in ({str(total_csv_files)[1:-1]}) and status='I'
    """
    # statement = f"select distinct file_name from " \
    #             f"youtube_project.product_staging_table " \
    #             f"where file_name in ({str(total_csv_files)[1:-1]}) and status='I' "
    logger.info(f"dynamically statment craeted: {statement}")
    cursor.execute(statement)
    data = cursor.fetchall()
    if data:
        logger.info("Your last run was failed please check")
    else:
        logger.info("No record match")

else:
    logger.info("Last run was successful!!!")

try:
    s3_reader = S3Reader()
    # Bucket name should come from table
    folder_path = config.s3_error_directory
    s3_absolute_file_path = s3_reader.list_files(s3_client,
                                                 config.bucket_name,
                                                 folder_path= folder_path)
    logger.info("Absolute path on s3 bucket for csv file %s",s3_absolute_file_path)
    if not s3_absolute_file_path:
        logger.info(f"No files available at {folder_path}")
        raise Exception("No Data available to process")

except Exception as e:
    logger.error("Exited with error:- %s". e)
    raise e

bucket_name = config.bucket_name
local_directory = config.local_directory

prefix = f"s3:/{bucket_name}/"
file_paths = [url[len(prefix):] for url in s3_absolute_file_path]
logger.info(msg: "File path available on s3 under %s bucket and folder name is %s",)
logging.info(f"file path available on s3 under {bucket_name} bucket and folder name is {file_paths}")
try:
    downloader = S3FileDownloader(s3_client, bucket_name, local_directory)
    downloader.download_files(file_paths)
except Exception as e:
    logger.error("File download error: %s, e")
    sys.exit()

# Get a list of all files in the local directory
all_files = os.listdir(local_directory)
logger.info(f"List of files present at my local directory after download {all_files}")

# Filter files with ".csv" in their names and create absolute paths
if all_files:
    csv = []
    error_files = []
    for files in all_files:
        if files.endswith(".csv")
            csv_files.append(os.path.abspath(os.path.join(local_directory, files)))

        if not csv_files:
            logger.error("No csv data available to process the request")
            raise Exception("No csv data available to process the request")

else:
    logger.error("There is no data to process")
    raise Exception("There is no data to process")

##################make csv lines convert into a list of comma separated##################
# csv_files = str(csv_files)[1:-1]
logger.info("*****************Listing the File*********************")
logger.info("List of csv files that needs to be processed %s", csv_files)

logger.info("*****************Creating spark session*********************")

spark = spark_session()

logger.info("*****************Spark session created*********************")