import numpy as np
import trimesh
import os

def rotate_stl_model(model_path, start_vec, end_vec, A, transdir):

# 加载stl模型
    mesh = trimesh.load(model_path)
    modelname = os.path.basename(model_path)
    model_name = modelname.replace(".stl", "")


# 定义旋转轴起点和终点坐标，以及旋转角度 (单位可能是度)
    center = start_vec
    rotation_axis_start = np.array(start_vec)
    rotation_axis_end = np.array(end_vec)  # 如果终点坐标与起点相同，则表示绕该点旋转

    rotation_axis = rotation_axis_end - rotation_axis_start
    rotation_axis /= np.linalg.norm(rotation_axis)

# 将角度转换为弧度
    angle_radians = A * np.pi / 180.0

# 计算旋转矩阵
    rotation_matrix = trimesh.transformations.rotation_matrix(angle_radians, rotation_axis, point=center)

# 应用旋转到模型
    model_rotated = mesh.apply_transform(rotation_matrix)


# 保存旋转后的模型到新文件y.stl
    output_path = f'model/new_model/{transdir+1}/{model_name}_rotated_{A}.stl'

# 创建目录，如果不存在
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    model_rotated.export(output_path)
    return model_rotated

rs = rotate_stl_model('model/duo1.stl', (3.5,0.0,0.0), (3.5,1.0,1.0), 10, 0)

