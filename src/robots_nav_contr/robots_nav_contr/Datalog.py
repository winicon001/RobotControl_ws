# File name   : Datalog.py
# Description : MSSQL Database Connection and Data Insertion
# Product     : redEye  
# E-mail      : winicon@live.com
# Author      : Semiu ADEBAYO
# Date        : 2025/04/04
# credit      : Copyright (c) 2024 Semiu ADEBAYO; Copilot 
# Description : 

        # This script is used to connect to a Microsoft SQL Server database and insert sensor data into a table.
        # It creates a table with the current date in the name if it doesn't already exist, and inserts sensor data into it.
        #
        # The script uses the pyodbc library to connect to the database and execute SQL commands.
        # It also uses the datetime library to get the current date for naming the table.
        #
        # The script includes error handling to catch any exceptions that occur during the database connection or data insertion process.
        # It also includes logging to provide information about the connection status, table creation, and data insertion.
        # It creates a table with the current date in the name if it doesn't already exist, and inserts sensor data into it.
        # It also includes error handling to catch any exceptions that occur during the database connection or data insertion process.



import sqlite3
import pyodbc
import datetime
from datetime import date
import rclpy.logging


#########################################################
######################## Logs ###########################
SQL_Logs = rclpy.logging.get_logger('SQL MESSAGE')

#########################################################

# Connection details
DATABASE_NAME = 'RobotsDB'
def connect_to_mssql(sensor_data):
    
    try:
        # Update with your own database credentials
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=192.168.1.175;'
            'DATABASE=RobotsDB;'
            'UID=sa;'
            'PWD=@AutomationIcon;'
            'TrustServerCertificate=yes;'

        )
        SQL_Logs.info(f"Successfully connected to the MSSQL database! - {DATABASE_NAME}")
        SQL_Logs.info(f"Database Name :  {DATABASE_NAME}")
        
        # Connect to the database
        cursor = connection.cursor()

        # Create the table if it doesn't exist
        table_name = f"{'datalogs3'}_{date.today().strftime('%Y_%m_%d')}"
        # Log the table name
        SQL_Logs.info(f"Table name: {table_name}")
        # Create a table with the current date in the name
        if table_name:
            SQL_Logs.info(f"Creating table {table_name}...")

            cursor.execute(f'''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U')
                BEGIN
                    CREATE TABLE [{table_name}] (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        robotName VARCHAR(50),
                        robotID VARCHAR(50),
                        robotType VARCHAR(50),
                        robotVersion VARCHAR(50),
                        robotSerial VARCHAR(50),
                        robotManufacturer VARCHAR(50),
                        ENC_TOTAL_COUNT_L FLOAT,
                        ENC_TOTAL_COUNT_R FLOAT,
                        COUNTER_L FLOAT,
                        COUNTER_R FLOAT,
                        rotation1 FLOAT,
                        rotation2 FLOAT,
                        speed_L FLOAT,
                        speed_R FLOAT,
                        dist_L FLOAT,
                        dist_R FLOAT,
                        totalDist_L FLOAT,
                        totalDist_R FLOAT,
                        ULTRASENSOR_DIST FLOAT,
                        YAW FLOAT,
                        PITCH FLOAT,
                        ROLL FLOAT,
                        timestamp DATETIME DEFAULT GETDATE()
                    )
                END
                ''')
            
            
            # Confirmation message
            SQL_Logs.info(f"Table {table_name} created successfully.")

        # Insert sensor data into the table
        cursor.execute(
            f"INSERT INTO {table_name} (robotName, robotID, robotType, robotVersion, robotSerial, robotManufacturer, ENC_TOTAL_COUNT_L, ENC_TOTAL_COUNT_R, COUNTER_L, COUNTER_R, rotation1, rotation2, speed_L, speed_R, dist_L, dist_R, totalDist_L, totalDist_R, ULTRASENSOR_DIST, YAW, PITCH, ROLL, timestamp) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)"
            , sensor_data)
        
        # Commit changes and close the connection
        connection.commit()
        
        # Confirmation message
        SQL_Logs.info(f"Data inserted into table {table_name} successfully.")

        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

        SQL_Logs.info("Database connection closed.")


if __name__ == "__main__":

    # Sample sensor 648
    sensor_data = ['Me', 'Take', 'Oscar', 'If', 'Press', 'One',  151, 154, 454, 57963, 25, 455, 50.92, 13.0, 12455.8, 8320, 3295, 2312, 234, 2.0, 25676.8, 27]
    # Call the function to connect to the database
    connect_to_mssql(sensor_data)