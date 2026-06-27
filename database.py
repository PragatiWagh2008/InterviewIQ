# database operations
import mysql.connector
InterviewIQ_DB = mysql.connector.connect(
    host="mysql-aryan-dek-interviewiq1.l.aivencloud.com",
    user="avnadmin",
    password="AVNS_wHLgqCUvjt9pJ-QybIV",
    port="24871",
    database="defaultdb"
)
sql_insert = "INSERT INTO testing (user_name,user_fullName,user_email_id) VALUES(%s, %s, %s)"
values = ("aryan-dek","Aryan Dekondwar","aryandek15.5@gmail.com")

IQ_cursor = InterviewIQ_DB.cursor(buffered=True)
IQ_cursor.execute("use defaultdb")
IQ_cursor.execute("show tables")
IQ_cursor.execute(sql_insert, values)
InterviewIQ_DB.commit()
IQ_cursor.execute("select * from testing")

for x in IQ_cursor:
    print(x)
