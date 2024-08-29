import xml.etree.ElementTree as ET

def parse_duo_pian_xml(duopianxml_path):

    tree1 = ET.parse(duopianxml_path)
    root1 = tree1.getroot()

    start_line = 8
    duopianxml_content = duopianxml_path[duopianxml_path.find('\n') * (start_line - 1):]

    part_data = {}
    part_list = root1.findall('PartList/PartItem')
    for part_item in part_list:
        filename = part_item.get('filename')
        if filename in part_data:
            part_data[filename]['name'] = part_item.get('name')
            part_data[filename]['Start Vector'] = part_item.get('start_vec')
            part_data[filename]['End Vector'] = part_item.get('end_vec')
        else:
            part_data[filename] = {'Name': part_item.get('name'), 'Filename': filename, 'Start Vector': part_item.get('start_vec'), 'End Vector': part_item.get('end_vec')}


    # 获取元素及其文本内容
    trans_items = root1.find('TransItemList').text.split('\n')

    # 分割每一行的数据
    data_list = [line.split() for line in trans_items]
    # 删除空列表
    data_lists = [row for row in data_list if row]

    # 返回处理后的数据
    return part_data, data_lists

def parse_gongkuang_xml(gongkuang_path):
    # 解析XML文件
    tree2 = ET.parse(gongkuang_path)
    root2 = tree2.getroot()

    start_line = 9
    gongkuangxml = gongkuang_path[gongkuang_path.rfind('\n') * (start_line - 1):]  # 提取从某行开始的XML内容

    def get_float_list(node_name, attribute_name):
        value = root2.find(node_name).get(attribute_name)
        if not value or value.strip() == "":
            return False
        else:
            return [float(val) for val in value.split(',')]

    # 提取Mach, AOA, AOS的相关值
    mach_range_value = root2.find('Mach').get('range-value')
    single_mach_values = get_float_list('Mach', 'single-value-list')

    aoa_range_value = root2.find('AOA').get('range-value')
    single_aoa_values = get_float_list('AOA', 'single-value-list')

    aos_range_value = root2.find('AOS').get('range-value')
    single_aos_values = get_float_list('AOS', 'single-value-list')

    # 提取PT列表
    pt_list = []
    for pt in root2.findall('.//PTlist/PT'):  # 遍历PTlist下的所有PT元素
        pt_dict = {'p': float(pt.get('p')), 't': float(pt.get('t'))}  # 创建字典
        pt_list.append(pt_dict)

    # 返回所有需要的结果
    return mach_range_value, single_mach_values, aoa_range_value, single_aoa_values, aos_range_value, single_aos_values, pt_list

def select_mode_xml(mode_path):
    tree3 = ET.parse(mode_path)
    root3 = tree3.getroot()
    o = root3.find('Cpu').get('Cores-value')
    t = root3.find('Gpu').get('Select-value')
    return o, t

