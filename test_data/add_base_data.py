import random
import datetime
import pymysql
from pymysql import MySQLError

# MySQL 连接信息
db_config = {
    'user': 'root',
    'password': 'passwd',
    'host': 'localhost',  # 修改为你的 MySQL 服务器地址
    'port': 3306,
    'database': 'volunteer_management',
}

SCHOOL_CHOICES = [
    ('工科', '工科'),
    ('船舶海洋与建筑工程学院', '船舶海洋与建筑工程学院'),
    ('机械与动力工程学院', '机械与动力工程学院'),
    ('电子信息与电气工程学院', '电子信息与电气工程学院'),
    ('集成电路学院', '集成电路学院'),
    ('材料科学与工程学院', '材料科学与工程学院'),
    ('环境科学与工程学院', '环境科学与工程学院'),
    ('生物医学工程学院', '生物医学工程学院'),
    ('航空航天学院', '航空航天学院'),
    ('理科', '理科'),
    ('数学科学学院', '数学科学学院'),
    ('物理与天文学院', '物理与天文学院'),
    ('化学化工学院', '化学化工学院'),
    ('海洋学院', '海洋学院'),
    ('生命科学', '生命科学'),
    ('生命科学技术学院', '生命科学技术学院'),
    ('农业与生物学院', '农业与生物学院'),
    ('医学院', '医学院'),
    ('药学院', '药学院'),
    ('人文社科', '人文社科'),
    ('安泰经济与管理学院', '安泰经济与管理学院'),
    ('凯原法学院', '凯原法学院'),
    ('外国语学院', '外国语学院'),
    ('人文学院', '人文学院'),
    ('马克思主义学院', '马克思主义学院'),
    ('国际与公共事务学院', '国际与公共事务学院'),
    ('媒体与传播学院', '媒体与传播学院'),
    ('设计学院', '设计学院'),
    ('体育系', '体育系'),
    ('上海高级金融学院', '上海高级金融学院'),
    ('国际化办学', '国际化办学'),
    ('上海交大密西根学院', '上海交大密西根学院'),
    ('巴黎卓越工程师学院', '巴黎卓越工程师学院'),
    ('上海交大-南加州大学文化创意产业学院', '上海交大-南加州大学文化创意产业学院'),
    ('中欧国际工商学院', '中欧国际工商学院'),
    ('中英国际低碳学院', '中英国际低碳学院'),
    ('交叉学科', '交叉学科'),
    ('致远学院', '致远学院'),
    ('智慧能源创新学院', '智慧能源创新学院'),
    ('教育学院', '教育学院'),
    ('溥渊未来技术学院', '溥渊未来技术学院'),
    ('人工智能学院', '人工智能学院'),
    ('心理学院', '心理学院'),
    ('研究院·基础研究', '研究院·基础研究'),
    ('系统生物医学研究院', '系统生物医学研究院'),
    ('自然科学研究院', '自然科学研究院'),
    ('海洋研究院', '海洋研究院'),
    ('李政道研究所', '李政道研究所'),
    ('中国法与社会研究院', '中国法与社会研究院'),
    ('变革性分子前沿科学中心', '变革性分子前沿科学中心'),
    ('张江高等研究院', '张江高等研究院'),
    ('研究院·应用基础研究', '研究院·应用基础研究'),
    ('能源研究院', '能源研究院'),
    ('空天科学技术研究院', '空天科学技术研究院'),
    ('汽车工程研究院', '汽车工程研究院'),
    ('航空发动机研究院', '航空发动机研究院'),
    ('燃气轮机研究院', '燃气轮机研究院'),
    ('上海智能制造研究院', '上海智能制造研究院'),
    ('医疗机器人研究院', '医疗机器人研究院'),
    ('医学影像先进技术研究院', '医学影像先进技术研究院'),
    ('人工智能研究院', '人工智能研究院'),
    ('三亚崖州湾深海科技研究院', '三亚崖州湾深海科技研究院'),
    ('元知机器人研究院', '元知机器人研究院'),
    ('研究院·综合交叉', '研究院·综合交叉'),
    ('碳中和发展研究院', '碳中和发展研究院'),
    ('Bio-X研究院', 'Bio-X研究院'),
    ('Med-X研究院', 'Med-X研究院'),
    ('转化医学研究院', '转化医学研究院'),
    ('个性化医学研究院', '个性化医学研究院'),
    ('董浩云航运与物流研究院（中美物流研究院）', '董浩云航运与物流研究院（中美物流研究院）'),
    ('新农村发展研究院（农业与生物学院）', '新农村发展研究院（农业与生物学院）')
]

activity_ids = []  # 保存已插入的活动 ID
student_ids = []  # 保存已插入的志愿者 ID
volunteer_phones = []  # 保存已插入的志愿者手机号
organizer_ids = []  # 保存已插入的组织者 ID


def random_date():
    # 生成去年今天到今年今天之间的随机日期
    start_date = datetime.date.today() - datetime.timedelta(days=365)
    return start_date + datetime.timedelta(days=random.randint(0, 365))


def create_random_volunteer():
    student_id = f"522{random.randint(100000000, 999999999):09d}"  # 以522开头的12位学号
    while student_id in student_ids:
        student_id = f"522{random.randint(100000000, 999999999):09d}"
    name = f"Volunteer{student_id}"
    school = random.choice([choice[0] for choice in SCHOOL_CHOICES])  # 随机选择学校
    major = f"Major{random.randint(1, 10)}"
    email = f"{student_id}@sjtu.edu.cn"
    phone = f"138{random.randint(10000000, 99999999)}"  # 假设手机号
    while phone in volunteer_phones:
        phone = f"138{random.randint(10000000, 99999999)}"

    # 生成随机密码（6位数字）
    password = f"{random.randint(100000, 999999)}"

    # 生成申请日期在去年今天到今年今天之间
    application_date = random_date()

    labor_hours = random.randint(0, 100)
    # TODO 调整偏好 float & randint
    type_preference = random.randint(0, 5)
    duration_preference = random.randint(0, 5)

    return (student_id, name, school, major, email, phone, password, application_date, labor_hours, type_preference,
            duration_preference)


def create_random_organizer():
    organizer_id = f"{random.randint(100000, 999999)}"  # 六位随机数字作为 ID
    while organizer_id in organizer_ids:
        organizer_id = f"{random.randint(100000, 999999)}"
    organizer_name = f"Organizer{organizer_id}"
    account = f"account_{organizer_name}"

    # 生成随机密码（6位数字）
    password = f"{random.randint(100000, 999999)}"

    application_date = datetime.date.today()

    return (organizer_id, organizer_name, account, password, application_date)


def create_random_activity(organizer_id):
    activity_id = f"{random.randint(100000, 999999)}"  # 六位随机数字作为 ID
    while activity_id in activity_ids:
        activity_id = f"{random.randint(100000, 999999)}"
    activity_name = f"Activity{activity_id}"
    activity_description = "This is a test activity description."
    activity_tags = random.choice(['讲坛讲座', '志愿公益', '劳动教育', '文体活动', '实习实践', '学习培训', '科创活动'])

    activity_image_path = "path/to/image.jpg"
    application_requirements = "No specific requirements."

    # 随机生成开始时间在去年到今年之间
    application_start_time = random_date()
    application_end_time = application_start_time + datetime.timedelta(days=random.randint(1, 10))
    activity_start_time = application_end_time + datetime.timedelta(days=1)
    activity_end_time = activity_start_time + datetime.timedelta(days=random.randint(1, 10))

    estimated_volunteer_hours = random.randint(1, 10)

    # 随机生成地址、联系人姓名和电话
    activity_locations = ['Location A', 'Location B', 'Location C', 'Location D']
    activity_location = random.choice(activity_locations)

    contact_names = ['Alice', 'Bob', 'Charlie', 'David']
    contact_name = random.choice(contact_names)

    contact_phones = ['13812345678', '13823456789', '13834567890', '13845678901']
    contact_phone = random.choice(contact_phones)

    accepted_volunteers = random.randint(1, 50)
    labor_hours = random.randint(1, 10)
    sutuo = "Some notes."
    notes = "Additional notes."

    return (
    activity_id, activity_name, activity_description, activity_tags, activity_image_path, application_requirements,
    application_start_time, application_end_time, activity_start_time, activity_end_time, estimated_volunteer_hours,
    activity_location, contact_name, contact_phone, organizer_id, accepted_volunteers, labor_hours, sutuo, notes)


def insert_data():
    # 连接到数据库
    db = pymysql.connect(**db_config)
    print("Connection successful.")
    try:
        cursor = db.cursor()

        # 插入随机志愿者
        for i in range(50):
            volunteer_data = create_random_volunteer()
            student_ids.append(volunteer_data[0])
            volunteer_phones.append(volunteer_data[5])
            cursor.execute("INSERT INTO api_volunteer (student_id, name, school, major, email, phone, password, application_date, labor_hours, type_preference, duration_preference) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", volunteer_data)

        # 插入随机组织者
        for i in range(10):
            organizer_data = create_random_organizer()
            organizer_ids.append(organizer_data[0])
            cursor.execute("INSERT INTO api_organizer (organizer_id, organizer_name, account, password, application_date) VALUES (%s, %s, %s, %s, %s)", organizer_data)
            db.commit()  # 在这里提交，确保组织者 ID 正确
            organizer_id = organizer_data[0]  # 获取组织者 ID

            # 插入随机活动
            for j in range(random.randint(1, 5)):
                activity_data = create_random_activity(organizer_id)  # 使用组织者 ID
                activity_ids.append(activity_data[0])
                cursor.execute("INSERT INTO api_activity (activity_id, activity_name, activity_description, activity_tags, activity_image_path, application_requirements, application_start_time, application_end_time, activity_start_time, activity_end_time, estimated_volunteer_hours, activity_location, contact_name, contact_phone, organizer_id, accepted_volunteers, labor_hours, sutuo, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", activity_data)
                db.commit()

        print("Data inserted successfully.")

    except MySQLError as e:
        print(f"Error: {e}")

    finally:
        if db:
            cursor.close()
            db.close()


if __name__ == "__main__":
    insert_data()
