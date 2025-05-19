import re
import csv
 
def parse_log_file(log_file_path, csv_file_path):
    # 正则表达式用于提取所需的字段
    pattern = re.compile(
        r'step:(\d+).*?'
        r'response_length/mean:([\d.]+).*?'
        r'response_length/max:([\d.]+).*?'
        r'response_length/min:([\d.]+).*?'
        r'timing_s/gen:([\d.]+).*?'
        r'timing_s/old_log_prob:([\d.]+).*?'
        r'timing_s/ref:([\d.]+).*?'
        r'timing_s/adv:([\d.]+).*?'
        r'timing_s/update_actor:([\d.]+).*?'
        r'timing_s/step:([\d.]+)'
    )
 
    # 用于存储解析后的数据
    data = []
 
    # 读取日志文件
    with open(log_file_path, 'r') as file:
        for line in file:
            match = pattern.search(line)
            if match:
                global_step = int(match.group(1))
                response_length_mean = int(float(match.group(2)))
                response_length_max = int(float(match.group(3)))
                response_length_min = int(float(match.group(4)))
                timing_gen = round(float(match.group(5)), 4)
                timing_old_log_prob = round(float(match.group(6)), 4)
                timing_ref = round(float(match.group(7)), 4)
                timing_adv = round(float(match.group(8)), 4)
                timing_update_actor = round(float(match.group(9)), 4)
                timing_step = round(float(match.group(10)), 4)
 
                # 将数据添加到列表中
                data.append({
                    "global_step": global_step,
                    "response_length_mean": response_length_mean,
                    "response_length_max": response_length_max,
                    "response_length_min": response_length_min,
                    "timing_gen": timing_gen,
                    "timing_old_log_prob": timing_old_log_prob,
                    "timing_ref": timing_ref,
                    "timing_adv": timing_adv,
                    "timing_update_actor": timing_update_actor,
                    "timing_step": timing_step
                })
 
    # 写入CSV文件
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = [
            "global_step", "response_length_mean", "response_length_max", "response_length_min",
            "timing_gen", "timing_old_log_prob", "timing_ref", "timing_adv",
            "timing_update_actor", "timing_step"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    import sys, os
    if len(sys.argv) != 2:
        print("Usage: python script.py <log_file_path>")
        print("Example: python script.py /path/to/your/logfile.log")
        sys.exit(1)
 
    log_file_path = sys.argv[1]
    
    # 验证输入文件存在性
    if not os.path.exists(log_file_path):
        print(f"Error: Input file {log_file_path} not found")
        sys.exit(1)
 
    # 生成输出路径（保持同目录，替换扩展名）
    log_dir = os.path.dirname(log_file_path)
    log_base = "verl_output"
    csv_file_path = os.path.join(log_dir, f"{log_base}.csv")
 
    try:
        parse_log_file(log_file_path, csv_file_path)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)
