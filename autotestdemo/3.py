import xlrd
import shutil


# 读取xls表格
def read_xls(file_path, sheet_name):
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_name(sheet_name)
    return sheet


# 替换grid.ini中的值
def replace_grid_values(sheet, grid_file_path):
    with open(grid_file_path, 'r') as f:
        lines = f.readlines()

    # 获取第一行的列名
    column_names = sheet.row_values(0)

    for i in range(2, sheet.nrows):
        row_values = sheet.row_values(i)
        for j in range(len(column_names)):
            if row_values[j] != '':
                lines[j] = lines[j].replace(column_names[j], str(row_values[j]))

    # 将替换后的内容写入新的grid.txt文件
    with open('grid.ini', 'w') as f:
        f.writelines(lines)


# 替换config.txt中的值
def replace_config_values(sheet, config_file_path):
    with open(config_file_path, 'r') as f:
        lines = f.readlines()

    # 获取第一行的列名
    column_names = sheet.row_values(0)

    for i in range(2, sheet.nrows):
        row_values = sheet.row_values(i)
        for j in range(len(column_names)):
            if row_values[j] != '':
                lines[j] = lines[j].replace(column_names[j], str(row_values[j]))

    # 将替换后的内容写入新的config.txt文件
    with open('config.txt', 'w') as f:
        f.writelines(lines)


# 移动文件
def move_file(file_path, new_folder):
    shutil.move(file_path, new_folder)


# 主函数
def main():
    # 读取Grid表格
    grid_sheet = read_xls('批处理配置表.xls', 'Grid')
    replace_grid_values(grid_sheet, 'grid.ini')

    # 读取Config表格
    config_sheet = read_xls('批处理配置表.xls', 'Config')
    replace_config_values(config_sheet, 'config.cfg')

    # 移动文件夹
    move_file('grid.ini', '1')
    move_file('config.cfg', '1')


if __name__ == '__main__':
    main()