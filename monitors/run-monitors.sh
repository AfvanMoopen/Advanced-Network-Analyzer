hazzle=${1:-localhost:5001}
sudo python3 host_monitor.py --hazzle $hazzle &
sudo python3 host_portscan.py --hazzle $hazzle &
python3 device_monitor.py --hazzle $hazzle &
python3 service_monitor.py --hazzle $hazzle &
