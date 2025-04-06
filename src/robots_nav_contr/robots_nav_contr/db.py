import pyodbc

# Connection details

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = '192.168.1.175'
DATABASE_NAME = 'RobotsDB'
USERNAME = 'sa'
PASSWORD = '@AutomationIcon'

def connect_to_mssql():
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
        print("Successfully connected to the MSSQL database!")
        
        # Example query
        cursor = connection.cursor()
        cursor.execute("SELECT @@VERSION;")
        result = cursor.fetchone()
        print("SQL Server version:", result[0])
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    connect_to_mssql()

