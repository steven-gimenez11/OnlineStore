# test_connection.py
import pyodbc

conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost\\STEVEN;"
    "Database=OnlineStore;"
    "Trusted_Connection=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("¡Conexión exitosa!")
    conn.close()
except Exception as e:
    print(f"Error de conexión: {str(e)}")