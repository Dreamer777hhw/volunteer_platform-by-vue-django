## test_data
- README.md
- db_config.json
- data_clear.py
- add_base_data.py
- add_data.py

### db_config.json
```json
{
    // 根据实际需要填入用户名、密码及数据库名称
    "user": "root", 
    "password": "passwd", 
    "host": "localhost",
    "port": 3306,
    "database": "volunteer_management"
}
```

### data_clear.py
```shell
python ./data_clear.py
```
该文件用于清空数据库中七表内容。
  
### add_base_data.py
```shell
python ./add_base_data.py
```
该文件用于添加基础数据，即表`api_activity`，
`api_organizer`，
`api_volunteer`

生成200名志愿者，20名组织者，每个组织者随机发布1-30个活动。
注意其中的`api_activity`表的生成依赖于`api_organizer`表。

### add_data.py
```shell
python ./add_data.py
```
该文件用于添加相关功能表的数据，即表`api_activitystatus`，`api_activityapplication`，
`api_volunteeractivity`，
`api_organizeractivity`



