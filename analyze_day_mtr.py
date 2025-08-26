#!/usr/bin/env python3
import re
import sys

def analyze_last_hops(file_path):#定义处理函数，读取输入的文件
    hop_line = re.compile(
        r"^\s*\d+\.\|--\s+([^\s]+)\s+(\d+\.\d+)%\s+\d+\s+[\d\.]+\s+([\d\.]+)\s+[\d\.]+\s+([\d\.]+)"
    )

    last_hops = []

    with open(file_path, "r", encoding="utf-8") as f:#读取文件赋予给对象f
        current_time = None
        current_last_hop = None

        for line in f:
            line = line.strip()
            if line.startswith("Start:"):
                # 遇到新探测，保存上一条探测的最后一跳
                if current_last_hop:
                    last_hops.append(current_last_hop)
                current_time = line.split("Start:")[1].strip()
                current_last_hop = None
            else:
                m = hop_line.match(line)
                if m:
                    # 每遇到一跳，就覆盖 current_last_hop
                    current_last_hop = {
                        "time": current_time,
                        "host": m.group(1),
                        "loss": float(m.group(2)),
                        "avg": float(m.group(3)),
                        "wrst": float(m.group(4))
                    }

        # 保存最后一条探测的最后一跳
        if current_last_hop:
            last_hops.append(current_last_hop)

    # 统计分析
    total = len(last_hops)
    loss_count = sum(1 for hop in last_hops if hop["loss"] > 0)
    max_loss = max((hop["loss"] for hop in last_hops), default=0)
    avg_loss = sum(hop["loss"] for hop in last_hops) / total if total > 0 else 0
    avg_rtt = sum(hop["avg"] for hop in last_hops) / total if total > 0 else 0
    max_rtt = max((hop["wrst"] for hop in last_hops), default=0)

    print("=== 最后一跳丢包统计 ===")
    print(f"总探测次数: {total}")
    print(f"丢包次数: {loss_count}")
    print(f"丢包比例: {avg_loss:.2f}%")
    print(f"最大丢包率: {max_loss:.2f}%")
    print(f"平均延迟: {avg_rtt:.2f} ms")
    print(f"最大延迟: {max_rtt:.2f} ms")

    print("\n=== 丢包详情 ===")
    for hop in last_hops:
        if hop["loss"] > 0:
            print(f"{hop['time']} | {hop['host']} | 丢包率: {hop['loss']}% | 平均延迟: {hop['avg']} ms | 最大延迟: {hop['wrst']} ms")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 analyze_last_hops.py /var/log/mtr/mtr-2025-08-26.log")
        sys.exit(1)

    analyze_last_hops(sys.argv[1])
