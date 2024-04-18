import pandas as pd
import os
import subprocess
import time
import shutil

# 读取excel表
xls = pd.ExcelFile('批处理配置表.xls')

# 读取sheet1
df1 = pd.read_excel(xls, 'Grid')

p = len(df1) - 2

for i in range(1, p+1):
    folder_name = str(i)
    os.mkdir(folder_name)

 # 复制license到文件夹

    source_file = 'license'
    target_folder = 'i'

    shutil.copy(source_file, target_folder)


 # 读取x.txt文件内容
    with open('grid.ini', 'r') as file:
        x_content = file.read()

 # 遍历表格的每一列
    for column in df1.columns:
 # 获取当前列的第一行字符串
        column_header = df1[column][0]

    # 在x.txt中查找对应的字符串
        start_index = x_content.find(column_header)

    # 如果找到了对应的字符串
        if start_index != -1:
        # 获取当前列的数据
            column_data = df1[column][2:]

        # 遍历当前列的每一行数据
            for i, value in enumerate(column_data):
        # 如果当前行有值
                if pd.notnull(value):
        # 将x.txt对应字符串后的值替换为当前行的值
                    end_index = x_content.find('\n', start_index)
                    x_content = x_content[:start_index] + value + x_content[end_index:]

    # 更新x.txt文件内容
        with open('i/grid.ini', 'w') as file:
            file.write(x_content)


for path in i:

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
