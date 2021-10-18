pkill flask
pkill node
ps -ef | grep hazzle_worker | grep -v grep | awk '{print $2}' | xargs sudo kill
cd monitor
./stop-monitor-all.sh
