import random
import datetime
import pymysql

# 数据库配置
db_config = {
    'host': 'localhost',  # 根据实际情况修改
    'user': 'root',
    'password': 'passwd',
    'database': 'volunteer_management',
}

# 选择活动状态
activity_status_choices = ['未开始', '招募中', '已招满', '进行中', '已结束', '已取消']

# 选择申请结果
application_result_choices = ['待审核', '未通过', '已通过']

# 选择活动参与结果
activity_result_choices = ['已参与', '未参与', '参与中', '已报名', '已录取', '未录取', '已取消']

def insert_data():
    try:
        # 连接到数据库
        db = pymysql.connect(**db_config)
        cursor = db.cursor()

        # 获取已存在的 ID
        cursor.execute("SELECT DISTINCT student_id FROM api_volunteer")
        volunteer_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT activity_id FROM api_activity")
        activity_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT organizer_id FROM api_organizer")
        organizer_ids = [row[0] for row in cursor.fetchall()]

        # 插入 ActivityStatus
        for activity_id in activity_ids:
            activity_status = random.choice(activity_status_choices)
            accepted_volunteers = random.randint(0, 100)
            registered_volunteers = random.randint(0, 100)
            clicks_in_1h = random.randint(0, 50)
            clicks_in_12h = random.randint(0, 200)
            total_clicks = random.randint(0, 1000)

            cursor.execute("""
                INSERT INTO api_activitystatus (activity_id, activity_status, accepted_volunteers, registered_volunteers, clicks_in_1h, clicks_in_12h, total_clicks)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (activity_id, activity_status, accepted_volunteers, registered_volunteers, clicks_in_1h, clicks_in_12h, total_clicks))

        # 插入 ActivityApplication
        for activity_id in activity_ids:
            for _ in range(random.randint(1, 5)):  # 为每个活动随机插入 1 到 5 个申请
                student_id = random.choice(volunteer_ids)
                application_result = random.choice(application_result_choices)
                application_date = datetime.datetime.now()

                cursor.execute("""
                    INSERT INTO api_activityapplication (student_id, activity_id, application_result, application_date)
                    VALUES (%s, %s, %s, %s)
                """, (student_id, activity_id, application_result, application_date))

        # 插入 VolunteerActivity
        for volunteer_id in volunteer_ids:
            for _ in range(random.randint(1, 3)):  # 为每个志愿者随机插入 1 到 3 个活动
                activity_id = random.choice(activity_ids)
                activity_result = random.choice(activity_result_choices)

                # 检查是否已经存在相同的 student_id 和 activity_id 组合
                cursor.execute("""
                    SELECT COUNT(*) FROM api_volunteeractivity WHERE student_id = %s AND activity_id = %s
                """, (volunteer_id, activity_id))
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        INSERT INTO api_volunteeractivity (student_id, activity_id, activity_result)
                        VALUES (%s, %s, %s)
                    """, (volunteer_id, activity_id, activity_result))

        # 插入 OrganizerActivity
        for organizer_id in organizer_ids:
            for activity_id in activity_ids:
                activity_result = random.choice(activity_result_choices)

                cursor.execute("""
                    INSERT INTO api_organizeractivity (organizer_id, activity_id, activity_result)
                    VALUES (%s, %s, %s)
                """, (organizer_id, activity_id, activity_result))

        db.commit()
        print("Data inserted successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    insert_data()