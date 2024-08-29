变舵偏批量任务计算脚本须知：

1. 运行该脚本需要装有python3环境（检查：linux环境命令行输入python；windows环境cmd命令行输入python，没有python会有相应错误提示）

2. 所需模型放入文件夹model中（包括需要变化的模型和后续需要一起生成网格并计算的模型）
注：！！！如需更换一批模型进行操作，请先手动删除掉model文件夹中的所有模型（保留model文件夹）

3. 当前仅支持stl模型

4. 配置参数存放于xml文件夹中，包括duopian.xml,gongkuang.xml,mode.xml
duopian.xml控制批量模型变化的相关参数，可以增加、减少配置项（不可改变格式，如加入制表符、修改匹配名字等）
gongkuang.xm控制流场计算参数变更，同样需要严格按照格式输入，参数可为空
！！！mode.xml控制计算方式，包括cpu和gpu两种方式，如果gpu select-value值设置为1，则直接使用gpu计算；如果gpu select-value值设置为0，则依据cpu cores-value的值作为并行核数进行cpu计算

5. 任务列表存放于workdir中，名为task1....taskn，包含生成好的网格、结果、变化后的模型、对应参数配置等

6. 后续批量修改的网格、解算参数都是基于初始配置文件的，存放于tool中，如果需要进行其他参数配置调整需手动修改其中内容（后续很多地方读值都是字符匹配，谨慎修改避免修改中出错）

7. 多任务结果表格存放于result中

8. 使用脚本！！！windows环境在Maker文件夹使用cmd命令输入：./venv/Scripts/python.exe run.py    
                           linux环境Maker文件夹使用命令行输入：./venv/Scripts/python run.py 