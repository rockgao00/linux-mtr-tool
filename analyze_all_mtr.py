#!/usr/bin/env python3
import os
import subprocess

# MTR 日志文件夹绝对路径
mtr_folder = '/var/log/mtr'
# 分析脚本绝对路径
analyze_script = os.path.abspath('./analyze_day_mtr.py')

# 输出结果文件（脚本当前路径下）
output_file = os.path.join(os.getcwd(), 'mtr_analysis_results.txt')

with open(output_file, 'w') as out_f:
    # 遍历所有 .log 文件
    for filename in os.listdir(mtr_folder):
        if filename.endswith('.log'):
            filepath = os.path.join(mtr_folder, filename)
            out_f.write(f"=== 分析文件: {filepath} ===\n")
            print(f"分析文件: {filepath}")

            # 调用分析脚本
            result = subprocess.run(
                ['python3', analyze_script, filepath],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True  # Python 3.6 中代替 text=True
            )

            # 写入分析结果
            out_f.write(result.stdout)
            if result.stderr:
                out_f.write("\n=== 错误信息 ===\n")
                out_f.write(result.stderr)
            out_f.write("\n\n")

print(f"所有分析结果已保存到: {output_file}")
