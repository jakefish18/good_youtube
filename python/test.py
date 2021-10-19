import psycopg2

connection = psycopg2.connect(
    host="127.0.0.1",
    user="postgres",
    password="Insaff2006",
    database="postgres" 
    )
with connection.cursor() as cursor:
        # Проверка на наличие в бд
        cursor.execute("select * from users where login='insafich18'")
        r = cursor.fetchall()
        print(r)
        for log in r:
            print(log)
