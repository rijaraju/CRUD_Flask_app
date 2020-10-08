import mysql.connector
import pandas as pd

data = pd.read_csv(r"path\to\data.csv")
df = pd.DataFrame(data, columns=["Name", "Address", "password", "Phone", "Score"])
df["password"] = "password"

# print(df)

connection = mysql.connector.connect(
    user="root", password="password", host="localhost", database="api"
)
# print(connection)
cursor = connection.cursor()

cursor.execute("drop table if exists data")

create_table = "CREATE TABLE IF NOT exists data (id int not null auto_increment primary key,Name nvarchar(50), Address nvarchar(500), password nvarchar(50), Phone nvarchar(50), Score int)"
cursor.execute(create_table)

for row in df.itertuples():
    val = (row.Name, row.Address, row.password, row.Phone, row.Score)
    # print(val)
    query = "INSERT INTO api.data (Name, Address, Password, Phone, Score) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(query, val)

# query = "select * from data "
# # print(name)
# cursor.execute(query)
# row = cursor.fetchone()
# print(row)
connection.commit()
connection.close()
