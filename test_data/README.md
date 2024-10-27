## test_data
- README.md
- add_base_data.py
- add_data.py
### add_base_data.py
```shell
python ./add_base_data.py
```
该文件用于添加基础数据，即表`api_activity`，
`api_organizer`，
`api_volunteer`

生成50名志愿者，10名组织者，每个组织者随机发布1-5个活动。
注意其中的`api_activity`表的生成依赖于`api_organizer`表。

### add_data.py
```shell
python ./add_data.py
```
该文件用于添加相关功能表的数据，即表`api_activitystatus`, 
`api_activityapplication`，
`api_volunteeractivity`,
`api_organizeractivity`

每个`api_activitystatus`表的数据对应一个活动的状态，包括`未开始`，`招募中`，`已招满`， `进行中`，`已结束`， `已取消`
为每个活动随机插入 1 到 5 个申请者，每个申请者随机报名 1 到 3 个活动。

