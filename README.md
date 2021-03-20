## Table of Contents
- [General Info](#general-info)
- [Technologies](#technologies)

## General Info
In this mini-project, I used Apache Airflow to create a log analyzer in Python to monitor the DAG Airflow I set up in my airflow-stock-market project. The following steps were executed:

- Created the Airflow DAG
- Created a PythonOperator to retrieve number of errors and error messages for each log file
- Created a PythonOperator to read from XCom and produce the total error count and error messages
- Set job dependencies
- Scheduled the job in Airflow

## Technologies
Mini-project is created with: 
* Python
* Apache Airflow