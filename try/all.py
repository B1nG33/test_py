import subprocess
import time

# 取 id = 1-100 的整数 生成列表
# p = [i for i in range(1, 101)]

p = [1, 2, 4]

path_list = [f'D:/test_list/grid_test/{item}' for item in p]


# 遍历path列表，依次执行解算程序
for path in path_list:
    # 取出path地址中匹配的文件夹id
    i = int(path.split('/')[-1])
    try:
        # 开始执行程序
        start_time = time.time()

        G = subprocess.Popen(
            ['D:/test_list/pigrid/PiGrid_APPV2.1.2.260.exe'], cwd=path,
            stdout=subprocess.PIPE)

        while True:
            # 实时输出后台信息
            output = G.stdout.readline()
            if output == b'' and G.poll() is not None:
                break
            if output:
                print(output.strip())
        success = True

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

