#kevin_timer

* 定时提醒
* human input

完成一个单机可用的系统

##使用：
1. python timer.py 10:00 todo
2. python alert.py  # loop

###时间输入方式
1. 相对时间
* 5m                5分钟后
* 5                 5分钟后
* 3d                3天后
* 3day              3天后
2. 指定日期
* 11-01
* 2014-11-01
* 11-01 8:00
* 11-01 8am
3. 指定时间（如果已过了今天的时间，会自动设置成第二天的）
* 8:00
* 8am/pm


##系统说明：
1. 使用watch.txt存储任务


##TODO
6. todo事件和done事件可以查询
5. alert窗体delay的时间可输入
4. 存储改成sqliteDB




