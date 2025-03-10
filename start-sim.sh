python3 basin/BasinServer.py -H 127.0.1.2:5020 -t 127.0.1.1:5020 -c 5000 -b 1 &
python3 basin/BasinServer.py -H 127.0.1.3:5020 -t 127.0.1.1:5020 -c 10000 -b 3 &
python3 basin/BasinServer.py -H 127.0.1.4:5020 -t 127.0.1.1:5020 -c 5000 -b 5 &
python3 basin/BasinServer.py -H 127.0.1.5:5020 -t 127.0.1.1:5020 -c 5000 -b 7 &
python3 conveyer/ConveyerServer.py -H 127.0.1.1:5020