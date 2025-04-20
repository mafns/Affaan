import mysql.connector as sqltor
connobj=sqltor.connector.connect(host='localhost',user='root',passwd='Affaan')
if connobj.is_connected():
    print("Connection established")
else:
    print("Connection not established")
cursor=connobj.cursor()
cursor.execute("use Olympics;") 
def gold1():
 cursor.execute("Select country from country_table where gold_medals=1 ")
 data=cursor.fetchall()
 count=cursor.rowcount
 print("Countries with 1 gold medal:")
 for row in data:
  print("Country name:",row[0])
def silver1():
 cursor.execute("Select country from country_table where silver_medals=1")
 data=cursor.fetchall()
 count=cursor.rowcount
 print("Countries with 1 silver medal:")
 for row in data:
  print("Country name:",row[0])
def bronze1():
 cursor.execute("Select country from country_table where bronze_medals=1")
 data=cursor.fetchall()
 count=cursor.rowcount
 print("Countries with 1 bronze medal:")
 for row in data:
  print("Country name:",row[0])
def mostgold():
 cursor.execute("SELECT country,gold_medals FROM country_table WHERE gold_medals")