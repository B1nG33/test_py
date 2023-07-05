import subprocess
import time
import shutil
import os
import numpy as np
# 取 id = 1-100 的整数 生成列表
p = [i for i in range(1, 751)]
# p = [1, 2, 4]

# a = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
# e=[-10,-5,0,5,10,15]
# f=[-10,-5,0,5,10,15]

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



    for b in np.arange(0.5, 6, 1):
        for g in range(-10,20,5):
            for h in range(-10,20,5):

                os.chdir(path)

                with open('config_yy.cfg', 'r') as f:
                    content = f.read()
                content = content.replace('MACH_NUMBER=2.5', 'MACH_NUMBER=' + str(b))
                content = content.replace('AOA=0', 'AOA=' + str(g))
                content = content.replace('AOS=0', 'AOS=' + str(h))
                content = content.replace('CHECK_DIR_NAME=check', 'CHECK_DIR_NAME=check' + str(b) +str(g)+str(h) )

                with open('config_yy.cfg', "w") as f:
                    f.write(content)


                 # Gpu解算
                # p = subprocess.Popen(['D:/ceshi/solver/PF_AppCudaV2.1.2.247.exe'], cwd=path, stdout=subprocess.PIPE)
                #
                #  # cpu多核并行
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
                content = content.replace('MACH_NUMBER=' + str(b), 'MACH_NUMBER=4.95')
                content = content.replace('AOA=' + str(g), 'AOA=0')
                content = content.replace('AOS=' + str(h), 'AOS=0')

                content = content.replace('CHECK_DIR_NAME=check' + str(b) +str(g)+str(h), 'CHECK_DIR_NAME=check')


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