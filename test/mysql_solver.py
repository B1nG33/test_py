import pymysql
import subprocess
import time
import psutil


# host = "localhost"

host = "192.168.101.7"
port = 3306
user = "testuser"
passwd = "123456"
db = "autotest"
charset = "utf8"

# 连接数据库
db = pymysql.Connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)

# 创建游标
cur = db.cursor()

# 数据库检索方式可加

# # 查询id = 1-100的path
# sql = "SELECT path FROM example WHERE id BETWEEN 1 AND 100"

# # 查询 class = low/subsonic/transonic/supersonic/hypersonic 的path
# sql = "SELECT path FROM example WHERE class='low'"

# 查询id为1、3、5、7的path值

sql = "SELECT path FROM example WHERE id IN (1, 2, 5, 7)"

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
        # 记录开始时间
        start_time = time.time()

        #  单核解算
        # p = subprocess.Popen(['D:/test_list/solver/PF_AppV2.1.2.194.exe'], cwd=path, stdout=subprocess.PIPE)

        #  Gpu解算
        # p = subprocess.Popen(['D:/test_list/solver/PF_AppCudaV2.1.2.240.exe'], cwd=path, stdout=subprocess.PIPE)

        #  cpu多核并行
        p = subprocess.Popen(
            ['D:/test_list/msMPI/MPIEXEC/mpiexec.exe', '-n', '8', 'D:/test_list/solver/PF_AppV2.1.2.240.exe'], cwd=path,
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
        with open('D:/test_list/result/solver/%d.txt' % i, 'w') as f:
            f.write('算例id %d 执行成功，耗时：%f秒，性能峰值：%fKB' % (i, duration, peak_memory_usage))
    else:
        with open('D:/test_list/result/solver/%d.txt' % i, 'w') as f:
            f.write('算例id %d 执行失败' % i)

    # 直接存入result.txt中
    # if success:
    #     with open('D:/test_list/result/result.txt', 'w') as f:
    #         f.write('算例id %d 执行成功，耗时：%f秒，性能峰值：%fKB' % (i, duration, peak_memory_usage)+'\n')
    # else:
    #     with open('D:/test_list/result/result.txt', 'w') as f:
    #         f.write('算例id %d 执行失败' % i+'\n')








