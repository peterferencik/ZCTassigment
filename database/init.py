import psycopg2

conn = psycopg2.connect("user=postgres password=mysecretpassword")
conn.autocommit = True
cur = conn.cursor()
cur.execute("CREATE TABLE cars(ID int,plate TEXT,password TEXT,is_free BOOLEAN);")
for i in range(1,64):
    cur.execute("INSERT INTO cars(ID,plate,password,is_free ) VALUES ({},'', '',TRUE);".format(i))

cur.close()
print("Written into database!")