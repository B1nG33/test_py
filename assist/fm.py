import subprocess
import time
import shutil
import os

# 取 id = 1-100 的整数 生成列表
p = [i for i in range(1, 751)]
# p = [1, 2, 4]

a = [2.5, 2.7, 2.9, 3.1, 3.3, 3.5, 3.7, 3.9, 4.1, 4.4, 4.6, 4.8, 5.0]

path_list = [f'D:/ceshi/example/{item}' for item in p]

# 遍历path列表，依次执行解算程序
for path in path_list:
    # 取出path地址中匹配的文件夹id
    i = int(path.split('/')[-1])
    print(path)

    G = subprocess.Popen(
        ['D:/ceshi/pigrid/PiGrid_APPV2.1.2.288.exe'], cwd=path,
        stdout=subprocess.PIPE)

    while True:
        # 实时输出后台信息
        output = G.stdout.readline()
        if output == b'' and G.poll() is not None:
            break
        if output:
            print(output.strip())
    success = True

    for b in a:

        os.chdir(path)

        with open('config_yy.cfg', 'r') as f:
            content = f.read()
        content = content.replace('MACH_NUMBER=2.5', 'MACH_NUMBER=' + str(b))
        content = content.replace('CHECK_DIR_NAME=check', 'CHECK_DIR_NAME=check' + str(b))

        with open('config_yy.cfg', "w") as f:
            f.write(content)


        #  Gpu解算
        # p = subprocess.Popen(['D:/ceshi/solver/PF_AppCudaV2.1.2.247.exe'], cwd=path, stdout=subprocess.PIPE)

        #  cpu多核并行
        p = subprocess.Popen(
            ['D:/ceshi/MPIEXEC/mpiexec.exe', '-n', '8', 'D:/ceshi/solver/PF_AppV2.1.2.247.exe'], cwd=path,
            stdout=subprocess.PIPE)

        while True:
            # 实时输出后台信息
            output = p.stdout.readline()
            if output == b'' and p.poll() is not None:
                break
            if output:
                print(output.strip())
        success = True

        os.chdir(path)

        with open('config_yy.cfg', 'r') as f:
            content = f.read()
        content = content.replace('MACH_NUMBER=' + str(b), 'MACH_NUMBER=2.5')
        content = content.replace('CHECK_DIR_NAME=check' + str(b), 'CHECK_DIR_NAME=check')

        with open('config_yy.cfg', "w") as f:
            f.write(content)

    model_folder = os.path.join(path, 'Model')
    if os.path.exists(model_folder):
        shutil.rmtree(model_folder)

    log_folder = os.path.join(path, 'LogInfo')
    if os.path.exists(log_folder):
        shutil.rmtree(log_folder)

    dbug_folder = os.path.join(path, 'MeshDebug')
    if os.path.exists(dbug_folder):
        shutil.rmtree(dbug_folder)

    mesh_folder = os.path.join(path, 'Mesh')
    if os.path.exists(mesh_folder):
        shutil.rmtree(mesh_folder)