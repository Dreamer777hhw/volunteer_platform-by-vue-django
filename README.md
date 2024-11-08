# Volunteer Management System

这是一个志愿者管理系统，旨在为志愿活动的组织者和参与者提供一个高效的管理平台。该系统使用 Django 作为后端框架，Vue.js 作为前端框架，MySQL 作为数据库。实现了以下的功能。

## 特性

- 志愿者注册与管理
- 组织者注册与管理
- 活动创建、更新和删除
- 活动申请与审核
- 活动状态跟踪
- 志愿者参与记录
- 个性化活动推荐

## 技术栈

- **后端**：Django, Django REST Framework
- **前端**：Vue.js
- **数据库**：MySQL

## 安装与运行

### 前提条件

确保你已安装以下软件：

- Python 3.x
- MySQL
- Node.js 和 npm

### 后端设置

1. 克隆项目：

   ```bash
   git clone git@codehub.devcloud.cn-north-4.huaweicloud.com:d7297926f9a44be9acb939e179bddb8c/volunteer_management.git
   cd volunteer_management
2. 创建并激活虚拟环境：

    ```bash
    python -m venv venv
    source venv/bin/activate  # 在Windows 上使venv\Scripts\activate
3. 安装依赖：
   
    ```bash
    pip install django djangorestframework mysqlclient django-cors-headers
4. 配置数据库：在 volunteer_management/settings.py 中配置数据库连接：

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
5. 运行数据库迁移：

    ```bash
    python manage.py makemigrations
    python manage.py migrate
6. 启动 Django 开发服务器：

    ```bash
    python manage.py runserver
### 前端搭建

1. 环境要求
   - Node.js (建议使用 LTS 版本)
   - npm (Node 包管理器，随 Node.js 一起安装)
2. 安装依赖

    ```bash
    # 在frontend文件夹内
    npm install
3. 运行开发服务器

    ```bash
    npm run serve

### 数据插入

1. 用户数据可以直接使用注册，或者参考文件夹`test_data`实现自动化插入。
2. 组织者不能注册，必须使用`test_data`中的`add_base_data.py`实现插入，默认密码是`123456`。
3. 活动需要以组织者的视角进行创建和修改。
