import math
import subprocess
import os

x = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5]

for i in x:

    a = [i * 3.1415926]
    y = [50 / i for i in a]
    b = []
    for num in y:
        b.append(1 - num * math.sin(5 * 3.1415926 / 180))
    c = [math.cos(5 * 3.1415926 / 180) * i for i in y]

    value1 = (0, a[0], 0)
    value2 = (b[0], 0, c[0])

    os.chdir('G:/MRF/test')

    with open('config_yy.cfg', 'r') as f:
        content = f.read()
    content = content.replace('ROTATING_FRAME_ANG_VEL=(0.0,0.942,0.0)', 'ROTATING_FRAME_ANG_VEL=' + str(value1))
    content = content.replace('ROTATING_FRAME_REF_PT=(1.0,0.0,53.052)', 'ROTATING_FRAME_REF_PT=' + str(value2))
    content = content.replace('CHECK_DIR_NAME=check', 'CHECK_DIR_NAME=check' + str(i))

    with open('config_yy.cfg', 'w') as f:
        f.write(content)

    #  Gpu解算
    # p = subprocess.Popen([G:/MRF/solver/PF_AppCudaV2.1.2.247.exe'], cwd='G:/MRF/test', stdout=subprocess.PIPE)

    #  cpu多核并行
    p = subprocess.Popen(
        ['G:/MRF/msMPI/MPIEXEC/mpiexec.exe', '-n', '8', 'G:/MRF/solver/PF_AppV2.1.2.247.exe'], cwd='G:/MRF/test', stdout=subprocess.PIPE)

    while True:
        # 实时输出后台信息
        output = p.stdout.readline()
        if output == b'' and p.poll() is not None:
            break
        if output:
            print(output.strip())
    success = True
    os.chdir('G:/MRF/test')

    with open('config_yy.cfg', 'r') as f:
        content = f.read()
    content = content.replace('ROTATING_FRAME_ANG_VEL=' + str(value1), 'ROTATING_FRAME_ANG_VEL=(0.0,0.942,0.0)')
    content = content.replace('ROTATING_FRAME_REF_PT=' + str(value2), 'ROTATING_FRAME_REF_PT=(1.0,0.0,53.052)')
    content = content.replace('CHECK_DIR_NAME=check' + str(i), 'CHECK_DIR_NAME=check')

    with open('config_yy.cfg', 'w') as f:
        f.write(content)







