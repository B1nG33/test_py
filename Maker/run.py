import subprocess
import time
import re
import ast
import shutil
import glob
import pandas as pd
import os
from Readxml import parse_duo_pian_xml
from Readxml import parse_gongkuang_xml
from Readxml import select_mode_xml
from trans import rotate_stl_model


#  读取变舵偏xml文件
duopianxml_file = 'xml/duopian.xml'
part_info, data_rows = parse_duo_pian_xml(duopianxml_file)


# 遍历模型文件夹
model_dir = 'model'
stl_path_list = []
for root, dirs, files in os.walk(model_dir):
    for file in files:
        if file.endswith('.stl'):
            stl_file_path = os.path.join(root, file)
            stl_path_list.append(stl_file_path)

stl_list = [os.path.basename(path) for path in stl_path_list]

# 定义一个新的空字典来存储结果
new_dic = {}

unchangelist = []
# 遍历stl_list
for stl_file in stl_list:
    # 检查当前stl_file是否存在于part_info的键中
    if stl_file in part_info.keys():
        # 如果存在，获取对应的键值对
        model_data = part_info[stl_file]

        # 创建一个新的字典条目，将模型路径添加到'model_path'
        new_entry = {'model_path': stl_path_list[stl_list.index(stl_file)]}

        # 添加'start_vector'和'end_vector'到新字典中
        new_entry.update({'Start Vector': model_data['Start Vector'],
                          'End Vector': model_data['End Vector']})

        # 将新条目添加到new_dic中
        new_dic[stl_file] = new_entry
    else:
        unchangelist.append(stl_file)

# 转换为列表
new_list = list(new_dic.values())


trans_list = []

# 遍历data_rows
for row in data_rows:
    x = data_rows.index(row)
    # 对于new_list中的每个字典
    for i, item in enumerate(new_list):
        # 创建一个新的字典
        temp_dict = {'angle_degrees': row[i], 'transdir': x}
        # 更新原有的字典，添加新的键值对
        temp_dict.update(item)
        # 将更新后的字典添加到trans_list中
        trans_list.append(temp_dict)


#  模型变换
for item in trans_list:
    model_path = item['model_path']
    start_vec = eval(item['Start Vector'])
    end_vec = eval(item['End Vector'])
    angle_degrees = int(item['angle_degrees'])
    transdir = int(item['transdir'])


#  执行批量模型变化
    rs = rotate_stl_model(model_path, start_vec, end_vec, angle_degrees, transdir)


model_path = 'model'
new_model_path = 'model/new_model'

#   移动未变化模型
def copy_to_subfolders(src_list, src_path, dest_path):
    for filename in src_list:
        source_file = os.path.join(src_path, filename)
        if os.path.isfile(source_file):
            # 遍历dest_path以及所有子文件夹
            for dest_folder in [dest_path] + [os.path.join(dest_path, d) for d in os.listdir(dest_path) if os.path.isdir(os.path.join(dest_path, d))]:
                target_file = os.path.join(dest_folder, filename)

                shutil.copy2(source_file, target_file)

copy_to_subfolders(unchangelist, model_path, new_model_path)

# 读取工况参数xml文件
results = parse_gongkuang_xml("xml/gongkuang.xml")



def generate_sequence(a):
    j, k, l = a
    b = []  # 初始化空列表来存储结果
    while j < k:
        b.append(j)
        j += l  # 每次迭代增加z
        if j >= k:
            b.append(k)
            break  # 如果超过y，则跳出循环

    return b


MACH_list = []
AOA_list = []
AOS_list = []
PT_list = []

# 遍历元组
for i, item in enumerate(results):
    # 判断 a, c, e 是否是非空字符串
    if i in [0, 2, 4] and item != '':
        if i == 0:  # 如果是a，直接添加到x
            MACH_list = generate_sequence(ast.literal_eval(item))
        elif i == 2:  # 同理，如果是c，添加到y
            AOA_list = generate_sequence(ast.literal_eval(item))
        else:
            AOS_list = generate_sequence(ast.literal_eval(item))

    # 判断 b, d, f 是否是非布尔值False
    elif i in [1, 3, 5] and not isinstance(item, bool):
        if i == 1:  # 对于b，添加到x
            for value in item:
                MACH_list.append(value)
        elif i == 3:
            for value in item:
                AOA_list.append(value)
        else:
            for value in item:
                AOS_list.append(value)

    # 判断 g 是否为空列表
    elif i == 6 and item:
        for value in item:
            PT_list.append(value)

config_list = []

if not MACH_list and not AOA_list and not AOS_list and not PT_list:
    print("工况列表为空，请添加配置")

elif not AOA_list and not AOS_list and not PT_list and MACH_list:
    for a in MACH_list:
        config_list.append(['mach', a])

elif not PT_list and not AOS_list and not MACH_list and AOA_list:
    for b in AOA_list:
        config_list.append(['aoa', b])

elif not PT_list and not AOA_list and not MACH_list and AOS_list:
    for c in AOS_list:
        config_list.append(['aos', c])

elif not MACH_list and not AOA_list and not AOS_list and PT_list:
    for d in PT_list:
        config_list.append(['pt', d])

elif not MACH_list and AOA_list and AOS_list and PT_list:
    for b in AOA_list:
        for c in AOS_list:
            for d in PT_list:
                config_list.append(['aoa', b, 'aos', c, 'pt', d])

elif not PT_list and AOA_list and AOS_list and MACH_list:
    for a in MACH_list:
        for b in AOA_list:
            for c in AOS_list:
                config_list.append(['mach', a, 'aoa', b, 'aos', c])

elif not AOA_list and MACH_list and AOS_list and PT_list:
    for a in MACH_list:
        for c in AOS_list:
            for d in PT_list:
                config_list.append(['mach', a, 'aos', c, 'pt', d])

elif not AOS_list and MACH_list and AOA_list and PT_list:
    for a in MACH_list:
        for b in AOA_list:
            for d in PT_list:
                config_list.append(['mach', a, 'aoa', b, 'pt', d])

elif not MACH_list and not AOA_list and AOS_list and PT_list:
    for c in AOS_list:
        for d in PT_list:
            config_list.append(['aos', c, 'pt', d])

elif not MACH_list and not AOS_list and PT_list and AOA_list:
    for b in AOA_list:
        for d in PT_list:
            config_list.append(['aoa', b, 'pt', d])

elif not MACH_list and not PT_list and AOS_list and AOA_list:
    for b in AOA_list:
        for c in AOS_list:
            config_list.append(['aoa', b, 'aos', c])

elif not AOA_list and not AOS_list and MACH_list and PT_list:
    for a in MACH_list:
        for d in PT_list:
            config_list.append(['mach', a, 'pt', d])

elif not AOA_list and not PT_list and MACH_list and AOS_list:
    for a in MACH_list:
        for c in AOS_list:
            config_list.append(['mach', a, 'aos', c])

elif not AOS_list and not PT_list and MACH_list and AOA_list:
    for a in MACH_list:
        for b in AOA_list:
            config_list.append(['mach', a, 'aoa', b])

else:
    for a in MACH_list:
        for b in AOA_list:
            for c in AOS_list:
                for d in PT_list:
                    config_list.append(['mach', a, 'aoa', b, 'aos', c, 'pt', d])


# 批量生成工况集

count = 0
for main_config in config_list:
    count += 1
    config_file_path = os.path.join(f'configdir', f'config_yy{count}.cfg')

    if not os.path.exists(config_file_path):
        with open(config_file_path, 'w') as f:
            pass
    with open('tool/config_yy.cfg', 'r') as f:
        content = f.read()

    for index, item in enumerate(main_config):
        if item == 'mach':
            a = main_config[index + 1]
            content = content.replace('MACH_NUMBER=2', 'MACH_NUMBER=' + str(a))
        elif item == 'aoa':
            b = main_config[index + 1]
            content = content.replace('AOA=10', 'AOA=' + str(b))
        elif item == 'aos':
            c = main_config[index + 1]
            content = content.replace('AOA=10', 'AOA=' + str(c))
        elif item == 'pt':
            pt_dict = main_config[index + 1]
            p = pt_dict.get('p')
            t = pt_dict.get('t')
            x = str(p) if p is not None else 'None'
            y = str(t) if t is not None else 'None'
            content = content.replace('FREESTREAM_PRESSURE=10147.68', 'FREESTREAM_PRESSURE=' + str(x))
            content = content.replace('FREESTREAM_TEMPERATURE=188.33', 'FREESTREAM_TEMPERATURE=' + str(y))


    with open(config_file_path, "w") as f:
        f.write(content)
    f.close()

#  生成任务集
configdir = 'configdir'
model_path = 'model/new_model'
workdir = 'workdir'

file_list = os.listdir(configdir)
a = len([name for name in file_list if os.path.isfile(os.path.join(configdir, name))])
b = len([name for name in os.listdir(model_path) if os.path.isdir(os.path.join(model_path, name))])

n = a * b

path = r"workdir"

for i in range(1, n+1):
    folder_name = 'task'+str(i)
    folder_path = os.path.join(path, folder_name)
    if os.path.exists(folder_path):  # 检查路径是否存在
        shutil.rmtree(folder_path)  # 如果存在则删除
        os.makedirs(folder_path)
    else:
        os.makedirs(folder_path)


#  复制grid文件到任务集
src_file = r'tool/grid.ini'
dst_folder = r'workdir'

for i in range(n):
    dst_path = os.path.join(dst_folder, 'task'+str(i+1))
    dst_file = os.path.join(dst_path, os.path.basename(src_file))
    with open(src_file, 'rb') as fsrc, open(dst_file, 'wb') as fdst:
        fdst.write(fsrc.read())

#  复制license文件到任务集
src_file = r'tool/license'
dst_folder = r'workdir'

for i in range(n):
    dst_path = os.path.join(dst_folder, 'task'+str(i+1))
    dst_file = os.path.join(dst_path, os.path.basename(src_file))
    with open(src_file, 'rb') as fsrc, open(dst_file, 'wb') as fdst:
        fdst.write(fsrc.read())


# 获取当前配置文件夹路径
config_dir = 'configdir'

# 创建新文件的目标路径
new_file_prefix = 'config_yy'

if b > 1:
    for i in range(1, n-a+1):
        source_file = f'{config_dir}/config_yy{i}.cfg'
        target_file = f'{config_dir}/{new_file_prefix}{a+i}.cfg'

    # 如果源文件存在，复制并更新文件名
        if os.path.isfile(source_file):
            shutil.copy2(source_file, target_file)

for i in range(1, n + 1):
    src_file = f'{configdir}/config_yy{i}.cfg'
    dst_folder = f'{workdir}/task{i}'

    # 将文件复制到对应的task文件夹
    dst_file = os.path.join(dst_folder, os.path.basename(src_file))
    shutil.move(src_file, dst_file)


workdir = 'workdir'

# 遍历工作目录及其子目录
for root, dirs, files in os.walk(workdir):
    for file_name in files:
        # 检查文件名是否匹配模式
        if file_name.startswith('config_yy') and file_name.endswith('.cfg'):
            old_file_path = os.path.join(root, file_name)
            new_file_path = os.path.join(root, 'config_yy.cfg')

            shutil.move(old_file_path, new_file_path)


if a > 1:
    for i in range(1, n-b+1):
        source_file = f'model/new_model/{i}'
        target_file = f'model/new_model/{b+i}'

    # 如果源文件存在，复制并更新文件名
        if os.path.isdir(source_file):
            shutil.copytree(source_file, target_file)

for i in range(1, n + 1):
    src_file = f'model/new_model/{i}'
    dst_folder = f'workdir/task{i}'

    # 将文件复制到对应的task文件夹
    dst_file = os.path.join(dst_folder, os.path.basename(src_file))
    shutil.move(src_file, dst_file)

dir_path = 'model/new_model'
if os.path.exists(dir_path):
    shutil.rmtree(dir_path)

workdir = "workdir"

# 遍历workdir下的所有 task 文件夹
for i in range(1, n + 1):  # 假设 n 代表文件夹数量
    task_folder_path = os.path.join(workdir, f"task{i}")

    if os.path.isdir(task_folder_path):
        # 检查 task{i} 下是否存在子文件夹 {i}
        inner_dir_path = os.path.join(task_folder_path, str(i))
        if os.path.isdir(inner_dir_path):
            # 移动子文件夹 {i} 中的所有文件到 task{i} 目录
            for filename in os.listdir(inner_dir_path):
                src_file_path = os.path.join(inner_dir_path, filename)
                dst_file_path = os.path.join(task_folder_path, filename)
                shutil.move(src_file_path, dst_file_path)

            # 删除空的子文件夹 {i}
            if not os.listdir(inner_dir_path):
                shutil.rmtree(inner_dir_path)

# 定义工作目录和目标文件名格式
workdir = "workdir"
grid_file_template = "grid.ini"
model_name_format = "ModelName                 {}"

# 对于每个task文件夹
for i in range(1, n + 1):
    task_folder_path = os.path.join(workdir, f"task{i}")

    # 搜索该文件夹内的.stl文件
    stl_files = glob.glob(os.path.join(task_folder_path, "*.stl"))

    if stl_files:
        # 打开grid.txt文件并追加模式
        with open(os.path.join(task_folder_path, grid_file_template), 'a', newline='') as grid_file:
            # 为每个找到的.stl文件添加一行
            for file in stl_files:
                model_name = model_name_format.format(os.path.basename(file)[:-4])  # 去掉文件后缀
                grid_file.write(model_name + ".stl\n")

#  查看任务列表
def find_task_folders(workdir):
    task_list = []
    for root, dirs, files in os.walk(workdir):
        for dir_name in dirs:
            if 'task' in dir_name:
                task_list.append(os.path.join(root, dir_name))
    return task_list

workdir = 'workdir'
task_list = find_task_folders(workdir)

#  选择计算方式
select_mode_tuple = select_mode_xml('xml/mode.xml')
select_mode_list = list(select_mode_tuple)
x = select_mode_list[0]
y = select_mode_list[1]

with open('result/result.txt', 'w') as file:
    # 使用 truncate() 方法清空文件内容
    file.truncate()

# 批量进行生成网格并计算
for path in task_list:
    # 取出path地址中匹配的文件夹id
    s = path.replace('\t', '\\')
    match1 = re.search(r'\d+', s)
    i = int(match1.group())

    try:
        # 开始执行程序
        start_time = time.time()

        G = subprocess.Popen(
            ['tool/PiGrid_APPV2.1.2.355.exe'], cwd=path,
            stdout=subprocess.PIPE)

        while True:
            # 实时输出后台信息
            output = G.stdout.readline()
            if output == b'' and G.poll() is not None:
                break
            if output:
                print(output.strip())
        success = True

        if int(y) == 0 and int(x) > 1:

            #  cpu多核并行
            p = subprocess.Popen(
                ['mpiexec.exe', '-n', f'{x}', 'tool/PF_AppV2.1.2.247.exe'], cwd=path,
                stdout=subprocess.PIPE)

            while True:
                # 实时输出后台信息
                output = p.stdout.readline()
                if output == b'' and p.poll() is not None:
                    break
                if output:
                    print(output.strip())
            success = True

        elif int(y) == 0 and int(x) == 1:

            # 单核解算
            p = subprocess.Popen(['tool/PF_AppV2.1.2.247.exe'], cwd=path, stdout=subprocess.PIPE)

            while True:
                # 实时输出后台信息
                output = p.stdout.readline()
                if output == b'' and p.poll() is not None:
                    break
                if output:
                    print(output.strip())
            success = True

        else:

            #  Gpu解算
            p = subprocess.Popen(['tool/PF_AppCudaV2.1.2.356.exe'], cwd=path, stdout=subprocess.PIPE)

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


#  获取工况信息
    with open(f'{path}/config_yy.cfg', 'r') as file:
        content = file.read()
        # 使用正则表达式查找'MACH='后的变量名
        match2 = re.search(r'MACH_NUMBER=([-+]?\d+(\.\d+)?)', content)  # '\w+' 匹配字母、数字和下划线
    if match2:
        m = match2.group(1)  # group(1) 获取第一个括号内的内容，即变量名
    mach = m

    match2 = re.search(r'AOA=([-+]?\d+(\.\d+)?)', content)  # '\w+' 匹配字母、数字和下划线
    if match2:
        o = match2.group(1)  # group(1) 获取第一个括号内的内容，即变量名
    aoa = o

    match2 = re.search(r'AOS=([-+]?\d+(\.\d+)?)', content)  # '\w+' 匹配字母、数字和下划线
    if match2:
        z = match2.group(1)  # group(1) 获取第一个括号内的内容，即变量名
    aos = z

    match2 = re.search(r'FREESTREAM_PRESSURE=([-+]?\d+(\.\d+)?)', content)  # '\w+' 匹配字母、数字和下划线
    if match2:
        j = match2.group(1)  # group(1) 获取第一个括号内的内容，即变量名
    pressure = j

    match2 = re.search(r'FREESTREAM_TEMPERATURE=([-+]?\d+(\.\d+)?)', content)  # '\w+' 匹配字母、数字和下划线
    if match2:
        l = match2.group(1)  # group(1) 获取第一个括号内的内容，即变量名
    temperature = l

#  获取变舵偏信息
    stl_files = glob.glob(os.path.join(path, '*rotated*.stl'))
    change = []
    for file in stl_files:
        # 获取文件名
        base_name = os.path.basename(file)

        # 提取旋转后的数字部分（假设旋转数值在字符串中间）
        al = base_name.split('_rotated_')
        num = al[1]
        rotation_number = num[:num.index('.stl')]

        change.append([al[0], f"旋转{rotation_number}度"])


  # 获取结果数据
    x_path = os.path.join(path, 'check', 'Verbose', 'monitor_force.txt')
    y_path = os.path.join(path, 'check',  'Verbose', 'monitor_forceMoment.txt')

    with open(x_path, 'r') as f1, open(y_path, 'r') as f2:
        monitor_force = f1.readlines()[-1].strip()
        monitor_forceMoment = f2.readlines()[-1].strip()

  # # 写入结果数据列表
  #
  #   def write_to_excel(data_list, file_path, sheet_name, start_row):
  #       df = pd.DataFrame({'Column': data_list}, index=range(start_row, start_row + len(data_list)))
  #
  #       # 写入新的Excel文件并保存到results目录下
  #       output_file = os.path.join('result', f'tool_{os.path.basename(file_path)}_updated.xlsx')
  #       with pd.ExcelWriter(output_file) as writer:
  #           df.to_excel(writer, sheet_name=sheet_name, index=False)
  #
  #       # 将原文件复制回原位置，保留原文件
  #       shutil.copy(file_path, file_path)


    data_list = ['mach:', mach, 'aoa:', aoa,'aos:', aos, 'pressure:', pressure, 'temperature:',temperature, 'modelchange:', change, 'monitor_force:', monitor_force, 'monitor_forceMoment:', monitor_forceMoment]
    # file_path = 'tool/result.xlsx'
    # sheet_name = 'Sheet1'
    # start_row = 3
    #
    # write_to_excel(data_list, file_path, sheet_name, start_row)
    file_path = "result/result.txt"

    # 打开文件，如果文件不存在则创建，模式为写入('w')
    with open(file_path, 'r+') as file:
        content = file.read()

        file.seek(0)
        file.write(content)

        file.write('\n')
        for item in data_list:
            file.write(str(item) + '\t')

    file.close()
