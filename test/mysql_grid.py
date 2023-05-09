import pymysql
import subprocess
import time
import psutil

#  192.168.101.2
#  192.168.184.1
# host = "localhost"
host = "192.168.101.2"
port = 3306
user = "testuser"
passwd = "123456"
db = "autotest"
charset = "utf8"

# 连接数据库
db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)

# 创建游标
cur = db.cursor()

# 查询id为1、3、5、7的path值
sql = "SELECT path FROM grid_test WHERE id IN (1, 2, 5, 7)"
cur.execute(sql)

# 获取查询结果
result = cur.fetchall()

# 关闭游标和数据库连接
cur.close()
db.close()

# 将查询结果存入列表
path_list = [row[0] for row in result]

# 每次执行的时间限制（单位秒）
# timelimit = 10

# 遍历path列表，依次执行解算程序
for path in path_list:
    # 取出path地址中匹配的文件夹id
    i = int(path.split('/')[-1])
    try:
        # 开始执行程序
        start_time = time.time()

        p = subprocess.Popen(
            ['D:/test_list/pigrid/PiGrid_APPV2.1.2.260.exe'], cwd=path,
            stdout=subprocess.PIPE)
        while True:
            # 实时输出后台信息
            output = p.stdout.readline()
            if output == b'' and p.poll() is not None:
                break
            if output:
                print(output.strip())
        success = True
    except Exception as e:
        print('第 %d 次执行异常 ：%s' % (i, e))
        success = False

    # 获取耗时及性能峰值
    end_time = time.time()
    duration = end_time - start_time
    process = psutil.Process()
    peak_memory_usage = process.memory_info().peak_wset

    # 将监控到的信息输出到指定结果文件夹中

    # 根据算例id创建结果文件夹，记录结果信息
    if success:
        with open('D:/test_list/result/grid/%d.txt' % i, 'w') as f:
            f.write('网格id %d 执行成功，耗时：%f秒，性能峰值：%fKB' % (i, duration, peak_memory_usage))
    else:
        with open('D:/test_list/result/grid/%d.txt' % i, 'w') as f:
            f.write('网格id %d 执行失败' % i)

    # 直接存入result.txt中
    # if success:
    #     with open('D:/test_list/result/result.txt', 'w') as f:
    #         f.write('算例id %d 执行成功，耗时：%f秒，性能峰值：%fKB' % (i, duration, peak_memory_usage)+'\n')
    # else:
    #     with open('D:/test_list/result/result.txt', 'w') as f:
    #         f.write('算例id %d 执行失败' % i+'\n')








