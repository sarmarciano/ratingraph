import pymysql
import pymysql.cursors


def main():
    connection = pymysql.connect(host='localhost', user='root', password='root', database='', cursorclass=pymysql.cursors.DictCursor)
    if cursor.execute(f"SHOW DATABASES LIKE '%{event["db_name"]}%;'")


    if __name__ == '__main__':
    main()