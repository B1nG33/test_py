import os
import shutil
import glob
import fileinput

'''
  导入数据库数据
'''

#  # 批量导入数据库数据
# for i in range(2, 838):
#     sql = "INSERT INTO example (id, class, path) VALUES (%s, %s, %s)"
#     cur.execute(sql, (i, 'hypersonic', 'D:/test_list/example/'+str(i)))
# db.commit()
# cur.close()
# db.close()


'''  
  在指定路径创建名为x的 x个空文件夹  
'''

# path = r"D:\test_list\grid_test"
# # 指定路径
# n = 800
# # 新建文件夹数量
# for i in range(1, n+1):
#     folder_name = str(i)
#     folder_path = os.path.join(path, folder_name)
#     os.makedirs(folder_path)


'''
  将目标文件复制到指定路径下的名为x...y的全部文件夹中
'''

# # 定义源文件路径和目标文件夹路径
# src_file = r'D:/whq/config_yy.cfg'
# dst_folder = r'D:/whq'

# # # 复制文件到目标文件夹中的1-1000个文件夹中
# for i in range(1, 751):
#     dst_path = os.path.join(dst_folder, str(i))
#     if not os.path.exists(dst_path):
#         os.makedirs(dst_path)
#     dst_file = os.path.join(dst_path, os.path.basename(src_file))
#     with open(src_file, 'rb') as fsrc, open(dst_file, 'wb') as fdst:
#         fdst.write(fsrc.read())


'''
  替换目标文件夹中的某文件为指定路径下的某文件：（1-10）    i+10   （10-20）
'''

# 复制文件到指定文件夹

# src_dir = "D:/test_list/grid_test/"
# dst_dir = "D:/test_list/grid_test/"
# for i in range(1, 32):
#     src_path = os.path.join(src_dir, str(i), "grid.ini")
#     dst_path = os.path.join(dst_dir, str(i+93), "grid.ini")
#     shutil.copy(src_path, dst_path)


'''
  批量将名为x..y的文件夹中指定文件z.txt中的某个值n替换成m
'''

# 批量替换配置文件中的参数值

# for i in range(1, 751):
#     folder_name = f"{i}"
#     folder_path = os.path.join("D:/whq", folder_name)
#     if os.path.exists(folder_path):
#         for file_name in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, file_name)
#             if os.path.isfile(file_path) and file_name.endswith(".ini"):
#                 with open(file_path, "r") as f:
#                     content = f.read()
#                     content = content.replace("ModelName             D:\\MAKER\PIFLOW\\Project\\test1\\Grid\\stlgroup.plt", f"ModelName             {folder_name}.stl")
#                     with open(file_path, "w") as f:
#                         f.write(content)


'''
   批量删除文件夹列表path_list中的非空文件夹
'''

# p = [1, 2, 5, 7]
# p = [i for i in range(1, 146)]
#
# path = [f'D:/test_list/grid_test/{item}' for item in p]
#
# for folder in path:
#     model_folder = os.path.join(folder, 'Model')
#     log_folder = os.path.join(folder, 'MeshDebug')
#     test_folder = os.path.join(folder, 'LogInfo')
#     mesh_folder = os.path.join(folder, 'Mesh')
#
#     if os.path.exists(model_folder):
#         shutil.rmtree(model_folder)
#     if os.path.exists(log_folder):
#         shutil.rmtree(log_folder)
#     if os.path.exists(test_folder):
#         shutil.rmtree(test_folder)
#     if os.path.exists(mesh_folder):
#         shutil.rmtree(mesh_folder)


'''
修改check文件夹名
'''

# # 定义文件夹路径
# folder_path = 'D:/test'
#
# # 遍历文件夹中的所有文件和文件夹
# for root, dirs, files in os.walk(folder_path):
#     for dir_name in dirs:
#         # 判断文件夹名是否为check
#         if dir_name == 'check':
#             # 构造新的文件夹名
#             new_dir_name = 'check1'
#             # 获取文件夹的完整路径
#             dir_path = os.path.join(root, dir_name)
#             # 构造新的文件夹的完整路径
#             new_dir_path = os.path.join(root, new_dir_name)
#             # 重命名文件夹
#             os.rename(dir_path, new_dir_path)

'''
对比两组列表，通过设定误差来输出校验结果
'''
# def verify(list1, list2, tolerance):
#     """
#     对比两个列表中的数值，如果误差小于tolerance则输出‘验证通过’，否则输出‘验证失败’
#     """
#     for i in range(len(list1)):
#         if abs(list1[i] - list2[i]) >= tolerance:
#             print("验证失败")
#             return
#     print("验证通过")


'''
linux环境运行windows执行程序
'''

## wine /path/to/your/exe/file.exe

'''
提取结果
'''

# folders = glob.glob('D:/test_list/example/**/check', recursive=True)
#
# for folder in folders:
#     x_path = os.path.join(folder, 'Verbose', 'monitor_force.txt')
#     y_path = os.path.join(folder, 'Verbose', 'monitor_forceMoment.txt')
#     path = str(folder.split('/')[-1])
#     print(path)
#     path1 = path.split('\\')[-2]
#
#     with open(x_path, 'r') as f1, open(y_path, 'r') as f2:
#         x_last_line = f1.readlines()[-1].strip()
#         y_last_line = f2.readlines()[-1].strip()
#         print(x_last_line)
#     with open('D:/test_list/result/result.txt', 'a') as f:
#         f.write(path1 + '\n' + x_last_line + '\n')
#         f.write('\n' + y_last_line + '\n' + '\n')
#         f.close()


# # # 1. 获取所有名为1-100的txt文件
# files = []
# for filename in os.listdir("D:/whq"):
#     if filename.endswith(".stl") and filename.split(".")[0] in map(str, range(1, 751)):
#         files.append(filename)
# # #
# # # 2. 创建同名的1-100文件夹
# # # for i in range(1, 1001):
# # #     os.makedirs(f"D:/whq/{i}", exist_ok=True)
# #
# # 3. 移动txt文件到同名的文件夹中
# for filename in files:
#     src_path = f"D:/whq/{filename}"
#     dst_path = f"D:/whq/{filename.split('.')[0]}/{filename}"
#     shutil.move(src_path, dst_path)


# path = r'D:/whq'  # 文件夹路径
#
# folders = os.listdir(path)  # 获取文件夹中所有文件夹的名字
#
# for folder in folders:
#     folder_path = os.path.join(path, folder)  # 获取当前文件夹的完整路径
#     if not os.path.isdir(folder_path):  # 如果不是文件夹，跳过
#         continue
#     grid_path = os.path.join(folder_path, 'grid.ini')  # 获取文件的路径
#     if not os.path.isfile(grid_path):  # 如果x.txt文件不存在，跳过
#         continue
#     with open(grid_path, 'r') as f:
#         lines = f.readlines()
#     with open(grid_path, 'w') as f:
#         for line in lines:
#             if 'ModelName             D:\MAKER\PIFLOW\Project\test1\Grid\stlgroup.plt' in line:
#                 line = line.replace('ModelName             D:\MAKER\PIFLOW\Project\test1\Grid\stlgroup.plt', f'ModelName             {folder}.stl')
#             f.write(line)

'''
查找没有Mesh的算例
'''
# dir_path = r"F:\test"
# for i in range(1, 6):  # 遍历 1-5 的文件夹
#     dir_name = str(i)
#     dir_full_path = os.path.join(dir_path, dir_name)
#
#     if os.path.isdir(dir_full_path):
#         has_mesh_dir = False  # 标记是否存在名为Mesh的文件夹
#         for sub_dir_name in os.listdir(dir_full_path):
#             sub_dir_full_path = os.path.join(dir_full_path, sub_dir_name)
#             if os.path.isdir(sub_dir_full_path) and sub_dir_name == "Mesh":
#                 has_mesh_dir = True
#                 break  # 如果存在名为Mesh的文件夹，则不用继续查找
#
#         if not has_mesh_dir:
#             print(dir_full_path)  # 如果不存在名为Mesh的文件夹，则输出该文件夹路径


'''
查找算例结果数据
'''

# num = input("请输入想要查看的算例编号：")
# with open("算例结果.txt", "r") as f:
#     contents = f.readlines()
# for i, line in enumerate(contents):
#     if num in line.strip() and line.strip() == num:
#         line1 = contents[i+1].strip()
#         line2 = contents[i+3].strip()
#         print("找到如下结果" + "\n" + "force为：" + line1)
#         print("forceMoment为：" + line2)














