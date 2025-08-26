#!/bin/bash

# 目标主机
TARGET="8.8.8.8"
LOG_DIR="/var/log/mtr"
mkdir -p "$LOG_DIR"

# 按日期命名日志
LOG_FILE="$LOG_DIR/mtr_$(date +'%Y-%m-%d').log"

while true; do
    stdbuf -oL /usr/bin/mtr -r -c 10 "$TARGET" >> "$LOG_FILE" 2>&1
    sleep 1   # 每1秒记录一次
done
