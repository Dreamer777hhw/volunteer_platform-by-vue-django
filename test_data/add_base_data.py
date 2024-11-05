# 添加数据于表：api_volunteer, api_organizer, api_activity

import random
import datetime
import pymysql
from pymysql import MySQLError
import json
import lorem

with open('db_config.json', 'r') as f:
    db_config = json.load(f)

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

# 随机五十个专业
MAJOR_CHOICES = [
    "信息安全", "软件工程", "计算机科学与技术", "网络工程", "物联网工程",
    "电子信息工程", "电子科学与技术", "通信工程", "自动化", "智能科学与技术",
    "机械工程", "机械设计制造及其自动化", "材料成型及控制工程", "工业设计", "过程装备与控制工程",
    "船舶与海洋工程", "交通运输", "飞行器设计与工程", "飞行器制造工程", "飞行器动力工程",
    "口腔医学", "临床医学", "基础医学", "药学", "护理学",
    "公共卫生与预防医学", "中医学", "中西医结合", "药物制剂", "药物分析",
    "量子力学", "电动力学", "热力学", "光学", "原子物理",
    "核物理", "凝聚态物理", "生物物理", "地球物理学", "天体物理学",
    "地质学", "地球化学", "地球物理学", "地理信息科学", "地球与空间科学",
    "华文文学", "英语", "日语", "法语", "德语",
]

# 五十个姓
LAST_NAMES = [
    "赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈",
    "褚", "卫", "蒋", "沈", "韩", "杨", "朱", "秦", "尤", "许",
    "何", "吕", "施", "张", "孔", "曹", "严", "华", "金", "魏",
    "陶", "姜", "戚", "谢", "邹", "喻", "柏", "水", "窦", "章",
    "云", "苏", "潘", "葛", "奚", "范", "彭", "郎", "鲁", "韦"
]

# 五十个名
FIRST_NAMES = [
    "伟", "芳", "娜", "敏", "静", "丽", "强", "磊", "军", "洋",
    "勇", "艳", "杰", "娟", "涛", "明", "超", "秀英", "霞", "平",
    "刚", "桂英", "庆", "琳", "飞", "红", "宇", "欣", "建", "兰",
    "春", "梅", "琳", "丽", "丹", "丽娟",  "晓", "燕", "宇", "宁",
    "浩然", "子轩", "梓涵", "思源", "雨泽", "烨磊", "智宸", "正豪", "昊然", "明杰"
]

# 三十个组织名
ORGANIZER_NAMES = [
    "学生会", "团委", "青年志愿者协会", "社会实践中心", "学生社团联合会",
    "学生发展指导中心", "学生就业指导中心", "学生创业指导中心", "学生心理健康中心", "学生体育中心",
    "船舶海洋与建筑工程学院", "机械与动力工程学院", "电子信息与电气工程学院", "集成电路学院", "材料科学与工程学院",
    "环境科学与工程学院", "生物医学工程学院", "航空航天学院", "数学科学学院", "物理与天文学院",
    "化学化工学院", "海洋学院", "生命科学技术学院", "农业与生物学院", "医学院",
    "药学院", "人文学院", "外国语学院", "马克思主义学院", "国际与公共事务学院",
]

ACTIVITY_TAGS = [
    "讲坛讲座", "志愿公益", "劳动教育", "文体活动", "实习实践", "学习培训", "科创活动"
]

ACTIVITY_LOCATIONS = [
    '闵行校区', '徐汇校区', '卢湾校区', '黄浦校区', '浦东校区', '嘉定校区', 
    '第一餐饮大厅', '第二餐饮大厅', '第三餐饮大厅', '第四餐饮大厅', '第五餐饮大厅', '第六餐饮大厅', 
    '电院', '机械楼', '船院', '航院', '材料楼', '环境楼', '生医楼', '理科楼', '法学院', '安泰楼', 
    '外国语学院', '人文楼', '马院', '国际学院', '媒体楼', '设计楼', '体育馆', '致远楼', '智能楼',
]

CONTACTS = [
    ['张三', '13812345678'], ['李四', '13887654321'], ['王五', '13823456789'], ['赵六', '13898765432'], ['钱七', '13834567890'],
    ['孙八', '13876543210'], ['周九', '13845678901'], ['吴十', '13854321098'], ['郑十一', '13865432109'], ['王十二', '13843210987'],
    ['冯十三', '13832109876'], ['陈十四', '13821098765'], ['褚十五', '13810987654'], ['卫十六', '13809876543'], ['蒋十七', '13898765432']
]

# 123456的hash值
PASSWORD = "pbkdf2_sha256$600000$D76fcVISds0eTkY3K71i9F$uQl/PbaGMoJ/ktyS6hpUkE2U7KmyBb9nmwLgzJqevrQ="

activity_ids = []  # 保存已插入的活动 ID
student_ids = []  # 保存已插入的志愿者 ID
organizer_ids = []  # 保存已插入的组织者 ID

def random_date(n = -1, m = 1):
    # 生成n年前今天到m年后今天之间的随机日期
    start_date = datetime.date.today().replace(year=datetime.date.today().year + n)
    end_date = datetime.date.today().replace(year=datetime.date.today().year + m)
    return start_date + (end_date - start_date) * random.random()

def random_name():
    return random.choice(LAST_NAMES) + random.choice(FIRST_NAMES)

def create_random_volunteer():
    student_id = f"522{random.randint(100000000, 999999999):09d}"  # 以522开头的12位学号
    while student_id in student_ids:
        student_id = f"522{random.randint(100000000, 999999999):09d}"
    name = random_name()
    school = random.choice([choice[0] for choice in SCHOOL_CHOICES])  # 随机选择学院
    major = random.choice(MAJOR_CHOICES)  # 随机选择专业
    email = f"{student_id}@sjtu.edu.cn"
    phone = f"138{random.randint(10000000, 99999999)}"  # 假设手机号
    
    password = PASSWORD

    # 生成申请日期在去年今天到今年今天之间
    application_date = random_date(-1, 0)

    labor_hours = random.randint(0, 100)
    # 调整偏好值
    type_preference = random.randint(0, 5)
    duration_preference = random.randint(0, 5)

    token = ''

    token_expiration = datetime.date.today() + datetime.timedelta(days=1000)

    return (student_id, name, school, major, email, phone, password, application_date, labor_hours, type_preference,
            duration_preference, token, token_expiration)


def create_random_organizer():
    organizer_id = f"{random.randint(100000, 999999)}"  # 六位随机数字作为 ID
    while organizer_id in organizer_ids:
        organizer_id = f"{random.randint(100000, 999999)}"
    organizer_name = random.choice(ORGANIZER_NAMES)
    account = organizer_name

    # 生成随机密码（6位数字）
    password = PASSWORD

    application_date = random_date(-1, 0)

    token = ''

    token_expiration = datetime.date.today() + datetime.timedelta(days=1000)

    return (organizer_id, organizer_name, account, password, application_date, token, token_expiration)


def create_random_activity(organizer_id):
    activity_tags = random.choice(['讲坛讲座', '志愿公益', '劳动教育', '文体活动', '实习实践', '学习培训', '科创活动'])
    activity_id = f"{random.randint(100000, 999999)}"  # 六位随机数字作为 ID
    while activity_id in activity_ids:
        activity_id = f"{random.randint(100000, 999999)}"
    activity_name = f"{activity_tags}-{activity_id}"
    # 使用 Lorem Ipsum 生成随机描述
    activity_description = lorem.sentence()

    activity_image_path = f"/activity-images/activity{random.randint(1,30)}.png"
    application_requirements = lorem.sentence()

    application_start_time = random_date(-1, 1)
    application_end_time = application_start_time + datetime.timedelta(days=random.randint(1, 10))
    activity_start_time = application_end_time + datetime.timedelta(days=10)
    activity_end_time = activity_start_time + datetime.timedelta(days=random.randint(1, 10))

    estimated_volunteer_hours = random.randint(1, 10)

    # 随机生成地址、联系人姓名和电话
    activity_location = random.choice(ACTIVITY_LOCATIONS)

    [contact_name, contact_phone] = random.choice(CONTACTS)

    accepted_volunteers = random.randint(30, 50)
    labor_hours = random.randint(1, 5)
    sutuo = lorem.sentence()
    notes = lorem.sentence()

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
        for i in range(200):
            volunteer_data = create_random_volunteer()
            student_ids.append(volunteer_data[0])
            cursor.execute("INSERT INTO api_volunteer (student_id, name, school, major, email, phone, password, application_date, labor_hours, type_preference, duration_preference, token, token_expiration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", volunteer_data)

        # 插入随机组织者
        for i in range(10):
            organizer_data = create_random_organizer()
            organizer_ids.append(organizer_data[0])
            cursor.execute("INSERT INTO api_organizer (organizer_id, organizer_name, account, password, application_date, token, token_expiration) VALUES (%s, %s, %s, %s, %s, %s, %s)", organizer_data)
            db.commit()  # 在这里提交，确保组织者 ID 正确
            organizer_id = organizer_data[0]  # 获取组织者 ID

            # 插入随机活动
            for j in range(random.randint(1, 10)):
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
