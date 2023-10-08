import pymysql
import os

# host = "localhost"

host = "192.168.101.2"
port = 3306
user = "root"
passwd = "123456"
db = "autotest"
charset = "utf8"

# 连接数据库
db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)

# 创建游标
cur = db.cursor()

# 参数值替换
#
sql = "UPDATE config SET value = 'RUNGE_KUTTA_EXPLICIT' WHERE name = 'TIME_EVOLUTE_MODE'"

sql1 = "UPDATE config SET value = '5' WHERE name = 'LUSGS_SWEEPS'"

sql2 = "UPDATE config SET value = '1' WHERE name = 'MACH_NUMBER'"

sql3 = "UPDATE config SET value = '0' WHERE name = 'AOA'"

sql4 = "UPDATE config SET value = '0' WHERE name = 'AOS'"

sql5 = "UPDATE config SET value = '2.1' WHERE name = 'CFL_NUMBER'"

sql6 = "UPDATE config SET value = '3000' WHERE name = 'EXT_ITER'"

sql7 = "UPDATE config SET value = 'NONE' WHERE name = 'PRECONDITION_MODE'"

sql8 = "UPDATE config SET value = 'CENT_JST' WHERE name = 'SPACE_CONV_SCHEMA'"

sql9 = "UPDATE config SET value = '2' WHERE name = 'MG_NUM_LEVELS'"

cur.execute(sql)

db.commit()

# 关闭游标和数据库连接
cur.close()
db.close()
