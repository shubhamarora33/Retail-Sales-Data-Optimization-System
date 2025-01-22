# Retail-Sales-Data-Optimization-System Using Python, MySQL, AWS S3 and Apache Spark

This project builds an end-to-end ETL data pipeline to process transactional data from various sources. It creates structured data marts to enable insightful analysis of customer purchasing behavior and sales team performance. The pipeline ensures data security, logging, error handling, and efficient resource management. Processed data is sourced from AWS S3 and utilized to generate actionable reports supporting various business use cases.

# What Are We Doing?
1. Reading Data
Extracting data from an AWS S3 bucket containing transactional datasets.
2. Transforming Data
Transforming data to meet specific business requirements.
3. Writing Transformed Data
Storing the processed data in a data mart for analytics and reporting.

# Why Are We Doing This?
Incentivize Sales Performance:
Reward top-performing sales personnel with a 1% incentive on total monthly sales.
Track Customer Spending:
Provide relevant coupons and discounts based on customer activity.
Generate Actionable Reports:
Deliver daily and monthly business reports for informed decision-making.

# How Are We Doing This?
**1. Tools and Libraries**<br>
Apache Spark: Handles data transformation efficiently for up to 15GB/day.<br>
Boto3: Facilitates seamless interactions with AWS S3.<br>
**2. Storage and Processing**<br>
Data marts enable efficient querying and reporting.<br>
Partitioning speeds up data read/write operations.<br>
**3. Processed Data Handling**<br>
Processed data is saved in S3 and removed from the local system to optimize resources.<br>

# Data Schema Design
## **1. Fact Table**<br>
**sales_data (from S3):**
* **Fields:** customer_id, store_id, product_name, sales_date, sales_person_id, price, quantity, total_cost, additional_column.<br>

## **2. Dimension Tables**<br>
* **Customer Table:** customer_id, first_name, last_name, address, phone_number, etc.<br><br>
* **Store Table:** store_id, address, store_manager_name, store_opening_date, etc.<br><br>
* **Product Table:** product_id, name, current_price, old_price, and other details.<br><br>
* **Sales Team Table:** sales_person_id, first_name, is_manager, etc.<br>

## **3. Staging Table**<br>
* Tracks the process status (active/inactive) for auditing updates.<br>

## **4. Data Marts**<br>
* **Customer Data Mart:** Insights into customer purchases.<br><br>
* **Sales Data Mart:** Detailed sales performance metrics.<br><br>

# Key Features and Workflow
## **1. Data Ingestion**
* Files downloaded from S3 are validated and logged in a MySQL staging table.<br>
* Non-compliant files are moved to an error folder for debugging.
## **2. Schema Validation**
* Ensures mandatory columns are present; invalid files are flagged for review.
## **3. Data Transformation**
* DataFrames consolidate extra columns into additional_column.<br>
* Enriched with joins to dimension tables (Customer, Store, etc.).
## **4. Data Marts Creation**
* Customer Data Mart: Tracks customer purchase patterns.<br>
* Sales Data Mart: Tracks sales performance and incentives with partitioning by month/store.
## **5. Data Storage**
* Enriched data is saved locally as Parquet files and uploaded to S3.
## **6. Reporting Integration**
* Final data is written back to MySQL tables for analytics and reporting.
## **7. Cleanup and Archival**
* Processed files archived in S3; local copies are deleted.

# Technology Stack
* **Programming Language:** Python
* **Data Processing Framework:** Apache Spark
* **Storage:** AWS S3, MySQL<br>
* **Utilities:**
  * **Cryptodome:** Secure key management.
  * **Custom Modules:** Logging, file handling, S3 operations, database interactions.

# Key Outputs
## **1. Customer Data Mart**
* Monthly purchase totals by customer.<br>
* Store-level customer activity tracking.<br>
## **2. Sales Team Data Mart**
* Monthly performance tracking for salespersons.<br>
* Incentive calculation based on total sales.<br>
## **3. Error Handling**
* Schema validation and error logging for mismatched files.

# Impact
* This pipeline automates data preparation, ensuring data quality, efficiency, and scalability. It integrates sales and customer data into structured marts, empowering marketing, sales, and operational decision-making.



```plaintext
Project structure:-
my_project/
├── docs/
│   └── readme.md
├── resources/
│   ├── __init__.py
│   ├── dev/
│   │    ├── config.py
│   │    └── requirement.txt
│   └── qa/
│   │    ├── config.py
│   │    └── requirement.txt
│   └── prod/
│   │    ├── config.py
│   │    └── requirement.txt
│   ├── sql_scripts/
│   │    └── table_scripts.sql
├── src/
│   ├── main/
│   │    ├── __init__.py
│   │    └── delete/
│   │    │      ├── aws_delete.py
│   │    │      ├── database_delete.py
│   │    │      └── local_file_delete.py
│   │    └── download/
│   │    │      └── aws_file_download.py
│   │    └── move/
│   │    │      └── move_files.py
│   │    └── read/
│   │    │      ├── aws_read.py
│   │    │      └── database_read.py
│   │    └── transformations/
│   │    │      └── jobs/
│   │    │      │     ├── customer_mart_sql_transform_write.py
│   │    │      │     ├── dimension_tables_join.py
│   │    │      │     ├── main.py
│   │    │      │     └──sales_mart_sql_transform_write.py
│   │    └── upload/
│   │    │      └── upload_to_s3.py
│   │    └── utility/
│   │    │      ├── encrypt_decrypt.py
│   │    │      ├── logging_config.py
│   │    │      ├── s3_client_object.py
│   │    │      ├── spark_session.py
│   │    │      └── my_sql_session.py
│   │    └── write/
│   │    │      ├── database_write.py
│   │    │      └── parquet_write.py
│   ├── test/
│   │    ├── scratch_pad.py.py
│   │    └── generate_csv_data.py
|   |    |__ extra_column_csv_generated_data.py
|   |    |__ less_column_csv_generated_data.py
|   |    |__ generate_customer_table_data.py
|   |    |__ generate_customer_table_data.py
|   |    |__ sales_data_upload_s3.py
```


Project Architecture:-
![Architecture](Retail Sales Data Optimization System\docs](https://github.com/shubhamarora33/Retail-Sales-Data-Optimization-System/tree/main/docs\architecture.png)

Database ER Diagram:-
![Architecture](Retail Sales Data Optimization System](https://github.com/shubhamarora33/Retail-Sales-Data-Optimization-System/tree/main/docs\database_schema.drawio.png)

