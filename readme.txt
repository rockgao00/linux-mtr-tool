1����װmtr
git clone https://github.com/traviscross/mtr.git
cd mtr
./bootstrap.sh && ./configure && make
make install

ͨ��mtr 8.8.8.8���Թ��ܿ���

2��������ؽű�
sudo mkdir -p /data/mtr
sudo vim /data/mtr/mtrlog.sh
--------------------------
#!/bin/bash

# Ŀ������
TARGET="8.8.8.8"
LOG_DIR="/var/log/mtr"
mkdir -p "$LOG_DIR"

# ������������־
LOG_FILE="$LOG_DIR/mtr_$(date +'%Y-%m-%d').log"

while true; do
    stdbuf -oL /usr/bin/mtr -r -c 10 "$TARGET" >> "$LOG_FILE" 2>&1
    sleep 1   # ÿ1���¼һ��
done
----------------------------

3����Ȩ�ű��ļ���������־�ļ�·����
sudo chmod 777 /data/mtr/mtrlog.sh
sudo mkdir -p /var/log/mtr
sudo chown $USER:$USER /var/log/mtr

4��������ط���
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

5���ָ���־
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
sudo logrotate -d /etc/logrotate.d/mtr   # ģ��ִ��
sudo logrotate -f /etc/logrotate.d/mtr   # ǿ��ִ��һ��

6��ͨ���ű�����ĳһ�����־
./analyze_day_mtr.py /var/log/mtr/mtr-2025-08-26.log

7��ͨ���ű��������е���־
./analyze_all_mtr.py


