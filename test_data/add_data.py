import random
import datetime
import pymysql
import json

# 数据库配置
with open('db_config.json', 'r') as f:
    db_config = json.load(f)

# 选择活动状态
activity_status_choices = ['未开始', '招募中', '已招满', '进行中', '已结束', '已取消']

# 选择申请结果
application_result_choices = ['待审核', '未通过', '已通过']

# 选择活动参与结果
volunteer_activity_result = ['已参与', '未参与', '参与中', '已报名', '已录取', '未录取', '已取消']

organizer_activity_result = ['未开始', '招募中', '已招满', '进行中', '已结束', '已取消']

def get_activity_status(activity_id):
    db = pymysql.connect(**db_config)
    cursor = db.cursor()

    cursor.execute("SELECT application_start_time, application_end_time, activity_start_time, activity_end_time FROM api_activity WHERE activity_id = %s", (activity_id,))
    activity_time = cursor.fetchone()
    # print(activity_time)
    if datetime.datetime.now() < activity_time[0]:
        return '未开始'
    elif datetime.datetime.now() < activity_time[1]:
        return '招募中'
    elif datetime.datetime.now() < activity_time[2]:
        return '已招满'
    elif datetime.datetime.now() < activity_time[3]:
        return '进行中'
    else:
        return '已结束'


def insert_data():
    try:
        # 连接到数据库
        db = pymysql.connect(**db_config)
        cursor = db.cursor()

        # 获取已存在的 ID
        cursor.execute("SELECT DISTINCT student_id FROM api_volunteer")
        volunteer_ids = [row[0] for row in cursor.fetchall()]

        # 获取活动信息
        cursor.execute("SELECT DISTINCT activity_id, accepted_volunteers, organizer_id FROM api_activity")
        # 按行获取数据
        activity_infos = cursor.fetchall()

        cursor.execute("SELECT DISTINCT organizer_id FROM api_organizer")
        organizer_ids = [row[0] for row in cursor.fetchall()]

        for activity_info in activity_infos:
            # 插入 ActivityStatus
            activity_id = activity_info[0]
            activity_status = get_activity_status(activity_id)
            accepted_volunteers = activity_info[1]
            if activity_status == '未开始':
                registered_volunteers = 0
            elif activity_status == '招募中':
                registered_volunteers = accepted_volunteers - random.randint(1, 20)
            else:
                registered_volunteers = accepted_volunteers
            clicks_in_1h = random.randint(0, 50)
            clicks_in_12h = clicks_in_1h + random.randint(0, 200)
            total_clicks = clicks_in_12h + random.randint(0, 1000)

            cursor.execute("""
                INSERT INTO api_activitystatus (activity_id, activity_status, accepted_volunteers, registered_volunteers, clicks_in_1h, clicks_in_12h, total_clicks)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (activity_id, activity_status, accepted_volunteers, registered_volunteers, clicks_in_1h, clicks_in_12h, total_clicks))

            # 插入 OrganizerActivity
            organizer_id = activity_info[2]

            cursor.execute("""
                        INSERT INTO api_organizeractivity (organizer_id, activity_id, activity_result)
                        VALUES (%s, %s, %s)
                    """, (organizer_id, activity_id, activity_status))
            
            # 插入 VolunteerActivity 和 ActivityApplication
            student_ids = []
            # 已通过学生
            for _ in range(registered_volunteers):
                student_id = random.choice(volunteer_ids)
                while student_id in student_ids:
                    student_id = random.choice(volunteer_ids)
                student_ids.append(student_id)
                application_result = '已通过'
                application_date = datetime.datetime.now()
                cursor.execute("""
                INSERT INTO api_activityapplication (student_id, activity_id, application_result, application_date)
                VALUES (%s, %s, %s, %s)
            """, (student_id, activity_id, application_result, application_date))
        
                if activity_status == '进行中':
                    activity_result = '参与中'
                elif activity_status == '已结束':
                    activity_result = '已参与'
                else:
                    activity_result = '已录取'
                cursor.execute("""
                    INSERT INTO api_volunteeractivity (student_id, activity_id, activity_result)
                    VALUES (%s, %s, %s)
                """, (student_id, activity_id, activity_result))
            
            # 未通过学生
            if activity_status != '未开始':
                for _ in range(random.randint(1,5)):
                    student_id = random.choice(volunteer_ids)
                    while student_id in student_ids:
                        student_id = random.choice(volunteer_ids)
                    student_ids.append(student_id)
                    application_result = '未通过'
                    application_date = datetime.datetime.now()
                    cursor.execute("""
                    INSERT INTO api_activityapplication (student_id, activity_id, application_result, application_date)
                    VALUES (%s, %s, %s, %s)
                """, (student_id, activity_id, application_result, application_date))
                
                    activity_result = '未录取'
                    cursor.execute("""
                        INSERT INTO api_volunteeractivity (student_id, activity_id, activity_result)
                        VALUES (%s, %s, %s)
                    """, (student_id, activity_id, activity_result))
            
            # 待审核学生
            if activity_status == '招募中':
                for _ in range(random.randint(1, 5)):
                    student_id = random.choice(volunteer_ids)
                    while student_id in student_ids:
                        student_id = random.choice(volunteer_ids)
                    student_ids.append(student_id)
                    application_result = '待审核'
                    application_date = datetime.datetime.now()
                    cursor.execute("""
                    INSERT INTO api_activityapplication (student_id, activity_id, application_result, application_date)
                    VALUES (%s, %s, %s, %s)
                """, (student_id, activity_id, application_result, application_date))
                
                    activity_result = '已报名'
                    cursor.execute("""
                        INSERT INTO api_volunteeractivity (student_id, activity_id, activity_result)
                        VALUES (%s, %s, %s)
                    """, (student_id, activity_id, activity_result))


        # # 插入 ActivityApplication
        # for activity_info in activity_infos:
        #     for _ in range(random.randint(1, 5)):  # 为每个活动随机插入 1 到 5 个申请
        #         student_id = random.choice(volunteer_ids)
        #         application_result = random.choice(application_result_choices)
        #         application_date = datetime.datetime.now()

        #         cursor.execute("""
        #             INSERT INTO api_activityapplication (student_id, activity_id, application_result, application_date)
        #             VALUES (%s, %s, %s, %s)
        #         """, (student_id, activity_id, application_result, application_date))

        # # 插入 VolunteerActivity
        # for volunteer_id in volunteer_ids:
        #     for _ in range(random.randint(1, 3)):  # 为每个志愿者随机插入 1 到 3 个活动
        #         activity_id = random.choice(activity_ids)
        #         activity_result = random.choice(volunteer_activity_result)

        #         # 检查是否已经存在相同的 student_id 和 activity_id 组合
        #         cursor.execute("""
        #             SELECT COUNT(*) FROM api_volunteeractivity WHERE student_id = %s AND activity_id = %s
        #         """, (volunteer_id, activity_id))
        #         if cursor.fetchone()[0] == 0:
        #             cursor.execute("""
        #                 INSERT INTO api_volunteeractivity (student_id, activity_id, activity_result)
        #                 VALUES (%s, %s, %s)
        #             """, (volunteer_id, activity_id, activity_result))

        # # 插入 OrganizerActivity
        # for organizer_id in organizer_ids:
        #     for activity_id in activity_ids:
        #         # 检查 api_activity 表中是否存在对应的 activity_id 和 organizer_id
        #         cursor.execute("""
        #             SELECT COUNT(*) FROM api_activity
        #             WHERE activity_id = %s AND organizer_id = %s
        #         """, (activity_id, organizer_id))
        #         count = cursor.fetchone()[0]

        #         if count > 0:  # 只有当活动和组织者的对应关系存在时才插入
        #             activity_result = random.choice(organizer_activity_result)

        #             cursor.execute("""
        #                 INSERT INTO api_organizeractivity (organizer_id, activity_id, activity_result)
        #                 VALUES (%s, %s, %s)
        #             """, (organizer_id, activity_id, activity_result))

        db.commit()
        print("Data inserted successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    insert_data()