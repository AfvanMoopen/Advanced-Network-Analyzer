name=${1:-localhost}
broker=${2:-localhost}
sudo python3 hazzle_worker.py --name $name --broker $broker
