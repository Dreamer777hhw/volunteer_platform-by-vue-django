# 清除数据库表的所有内容
# 清除表：api_activity api_organizer api_volunteer
# api_volunteeractivity api_activityapplication api_activitystatus api_organizeractivity

import random
import datetime
import pymysql
from pymysql import MySQLError
import json

with open('db_config.json', 'r') as f:
    db_config = json.load(f)

def clear_data():
    # 连接到数据库
    db = pymysql.connect(**db_config)
    print("Connection successful.")
    try:
        cursor = db.cursor()

        # 按顺序清除表的内容
        tables = [
            'api_volunteeractivity',
            'api_activityapplication',
            'api_activitystatus',
            'api_organizeractivity',
            'api_activity',
            'api_volunteer',
            'api_organizer'
        ]

        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Cleared table: {table}")

        db.commit()
        print("Data cleared successfully.")

    except MySQLError as e:
        print(f"Error: {e}")

    finally:
        if db:
            cursor.close()
            db.close()

if __name__ == "__main__":
    clear_data()
