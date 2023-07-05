import numpy as np
import matplotlib.pyplot as plt

# 读取数据
with open('datafile.txt', 'r') as f:
    data = [float(line.strip()) for line in f]

counts = {}
for d in data:
    if d not in counts:
        counts[d] = 1
    else:
        counts[d] += 1

# # 绘制条形图
x = list(counts.keys())
y = list(counts.values())
print(x, y)
plt.barh(list(counts.keys()), list(counts.values()))
plt.ylabel('Float Value')
plt.xlabel('Count')
plt.title('Occurrences of Float Values in data.txt')
plt.show()


# # 读取数据
# with open('datafile.txt', 'r') as f:
#     data = [float(line.strip()) for line in f]
#
# # 统计每个浮点数在数据中出现的次数
# counts = {}
# for d in data:
#     if d not in counts:
#         counts[d] = 1
#     else:
#         counts[d] += 1
#
# # 将字典按照值排序
# sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
#
# # 输出每个x对应的y值
# with open('test.txt', 'w') as f:
#     for item in sorted_counts:
#         f.write(f"{item[0]}: {item[1]}\n")
