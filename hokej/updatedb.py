import psycopg2

conn = psycopg2.connect(database = "euro", user = "postgres", password = "123456", host = "127.0.0.1", port = "5432")
cur = conn.cursor()

Q = """select * from hokej.zapasy """
cur.execute(Q)
conn.commit()

result = cur.fetchall()
for i in result:
    if (i[5])>(i[6]):
        
'''
Q = """update hokej.zapasy set skupina = 'B' where zapasy_id = 32"""
try:
    cur.execute(Q)
    conn.commit()
except:
    pass
'''    
conn.commit()
conn.close()