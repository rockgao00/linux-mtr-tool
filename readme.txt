1、安装mtr
git clone https://github.com/traviscross/mtr.git
cd mtr
./bootstrap.sh && ./configure && make
make install

通过mtr 8.8.8.8测试功能可用

2、创建监控脚本
sudo mkdir -p /data/mtr
sudo vim /data/mtr/mtrlog.sh
--------------------------
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
----------------------------

3、赋权脚本文件并创建日志文件路径：
sudo chmod 777 /data/mtr/mtrlog.sh
sudo mkdir -p /var/log/mtr
sudo chown $USER:$USER /var/log/mtr

4、创建监控服务
sudo vim /etc/systemd/system/mtr_daily.service
------------------------------
[Unit]
Description=Daily Continuous MTR Monitoring
After=network.target

[Service]
Type=simple
ExecStart=/data/mtr/mtrlog.sh
Restart=always
User=root

[Install]
WantedBy=multi-user.target
-----------------------------------
sudo systemctl daemon-reload
sudo systemctl start mtr_daily.service
sudo systemctl enable mtr_daily.service
sudo systemctl status mtr_daily.service

5、分割日志
sudo vim /etc/logrotate.d/mtr
--------------
/var/log/mtr/*.log {
    daily
    missingok
    rotate 60
    compress
    delaycompress
    notifempty
    copytruncate
}
-----------------
sudo logrotate -d /etc/logrotate.d/mtr   # 模拟执行
sudo logrotate -f /etc/logrotate.d/mtr   # 强制执行一次

6、通过脚本分析某一天的日志
./analyze_day_mtr.py /var/log/mtr/mtr-2025-08-26.log

7、通过脚本分析所有的日志
./analyze_all_mtr.py


