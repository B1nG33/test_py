import os
import shutil

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
# src_file = r'D:/test_list/grid_test/1/grid.ini'
# dst_folder = r'D:/test_list/grid_test'
# # 创建目标文件夹
# # if not os.path.exists(dst_folder):
# #     os.makedirs(dst_folder)
# # 复制文件到目标文件夹中的1-1000个文件夹中
# for i in range(2, 801):
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

# for i in range(94, 125):
#     folder_name = f"{i}"
#     folder_path = os.path.join("D:/test_list/grid_test", folder_name)
#     if os.path.exists(folder_path):
#         for file_name in os.listdir(folder_path):
#             file_path = os.path.join(folder_path, file_name)
#             if os.path.isfile(file_path) and file_name.endswith(".ini"):
#                 with open(file_path, "r") as f:
#                     content = f.read()
#                     content = content.replace("../../model/oneraM6_new.stl", "../../model/NEWJY_GUAZAI.stl")
#                     with open(file_path, "w") as f:
#                         f.write(content)


'''
  打印出结果文件中的最后一行，可用作统计查看算例中的最后一行结果并输出到其他地方
'''

#  显示文件夹中文件结果最后一行

# folders = ['1', '2']
# for folder in folders:
#     path = os.path.join("D:/test_list/example", folder, "check", "Verbose", "monitor_force.txt")
#     with open(path, "r")as file:
#         lines = file.readline()
#         print(lines[-1])


'''
   批量删除文件夹列表path_list中的文件
'''

# # 列表输入
#
# p = [1, 2, 3, 6]
#
# path_list = [f'D:/test_list/example/{item}' for item in p]
#
# for path in path_list:
#     if os.path.exists(os.path.join(path, 'piflow_verify.txt')):
#         os.remove(os.path.join(path, 'piflow_verify.txt'))
#
#     if os.path.exists(os.path.join(path, 'pub_key')):
#         os.remove(os.path.join(path, 'pub_key'))
#
#     if os.path.exists(os.path.join(path, 'restartFlowFile.dat')):
#         os.remove(os.path.join(path, 'restartFlowFile.dat'))
#
#     if os.path.exists(os.path.join(path, 'signaturefile_verify')):
#         os.remove(os.path.join(path, 'signaturefile_verify'))
#     if os.path.exists(os.path.join(path, 'check')):
#         shutil.rmtree(os.path.join(path, 'check'))


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
 提取结果文件到result
'''

# # 定义读取文件内容的函数
# def read_file(file_path):
#     with open(file_path, 'r') as f:
#         return f.read()
#
# # 获取grid文件夹路径
# grid_path = 'd:/test_list/result/grid'
#
# # 获取result文件夹路径
# result_path = 'd:/test_list/result'
#
# # 遍历grid文件夹下所有txt文件，并将内容写入result.txt文件中
# with open(os.path.join(result_path, 'result.txt'), 'w') as result_file:
#     for file_name in os.listdir(grid_path):
#         if file_name.endswith('.txt'):
#             file_path = os.path.join(grid_path, file_name)
#             file_content = read_file(file_path)
#             result_file.write(file_content+"\n\n")


'''
获取性能
'''
# # 获取进程ID
# pid = 1234
#
# # 获取进程对象
# p = psutil.Process(pid)
#
# # 获取进程的CPU峰值
# cpu_peak = p.cpu_percent(interval=1)
#
# # 获取进程的内存峰值
# mem_peak = p.memory_info().peak / 1024 / 1024
#
# print("CPU Peak: {}%".format(cpu_peak))
# print("Memory Peak: {}MB".format(mem_peak))


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


@include








