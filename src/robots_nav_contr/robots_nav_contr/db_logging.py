import pyodbc

# Connection details

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
        query = 'SELECT * FROM [RobotsDB].[dbo].[db_test]'
        cursor.execute(query)

        rows = cursor.fetchall()

        # print the data 
        for row in rows:
            print(row)
        
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

