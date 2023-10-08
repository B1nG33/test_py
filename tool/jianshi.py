import time
import psutil
import nvidia_smi

def monitor_performance(process_name, output_file):
    # 初始化NVIDIA管理库
    nvidia_smi.nvmlInit()

    # 获取指定进程的PID
    pid = None
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            pid = proc.info['pid']
            break

    if pid is None:
        print("未找到进程: ", process_name)
        return

    # 获取进程对象
    process = psutil.Process(pid)

    # 初始化性能数据
    max_memory_usage = 0
    max_cpu_usage = 0
    max_gpu_usage = 0

    # 打开输出文件
    with open(output_file, 'w') as file:
        while process.is_running():
            try:
                # 获取进程的内存占用
                memory_info = process.memory_info()
                memory_usage = memory_info.rss / (1024 * 1024)  # 转换为MB

                # 更新内存占用峰值
                if memory_usage > max_memory_usage:
                    max_memory_usage = memory_usage

                # 获取GPU使用情况
                handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
                utilization = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
                gpu_usage = utilization.gpu

                # 更新GPU使用情况峰值
                if gpu_usage > max_gpu_usage:
                    max_gpu_usage = gpu_usage

                # 获取CPU使用情况
                cpu_usage = psutil.cpu_percent()

                # 更新CPU使用情况峰值
                if cpu_usage > max_cpu_usage:
                    max_cpu_usage = cpu_usage

                # 打印性能数据并写入文件
                file.write(f"内存占用峰值: {max_memory_usage}MB\n")
                file.write(f"CPU使用情况峰值: {max_cpu_usage}%\n")
                file.write(f"GPU使用情况峰值: {max_gpu_usage}%\n")
                file.write("\n")

                # 等待一秒钟再继续采集数据
                time.sleep(1)

            except KeyboardInterrupt:
                break

    # 释放NVIDIA管理库资源
    nvidia_smi.nvmlShutdown()

# 示例用法
process_name = "piflow.exe"
output_file = "性能检测.txt"
monitor_performance(process_name, output_file)
