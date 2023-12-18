import os

from dotenv import load_dotenv
import mysql.connector

# Lataa ympäristömuuttujat tiedostosta
load_dotenv("dotenv.env")

# Muodosta tietokantayhteys
db_connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    port=int(os.getenv("DB_PORT", 3306)),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    use_pure=False,  # Käytä C-toteutusta eikä Python-toteutusta
    unix_socket=''
)

# Luo tietokantakursori
cursor = db_connection.cursor()

# Suorita SQL-kysely
sql_query = "SELECT * FROM rawdata"
cursor.execute(sql_query)

# Hae kaikki tulokset
results = cursor.fetchall()

# Tulosta tulokset
for result in results:
    print(result)

# Sulje tietokantayhteys
cursor.close()
db_connection.close()
