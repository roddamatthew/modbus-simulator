from Basin import Basin
from BasinDataBank import BasinDataBank
from threading import Thread
import argparse

parser = argparse.ArgumentParser()
parser.add_argument( '-H', '--host', type = str, default = '127.0.0.1:5021', help = 'ip:port' )
parser.add_argument( '-t', '--target', type = str, default = '127.0.0.1:5022', help = 'ip:port' )
parser.add_argument( '-c', '--clock', type = int, default = '3000', help = 'time in milliseconds' )
parser.add_argument( '-b', '--bit', type = int, default = '0', help = 'coil to set after timer expires' )

args = parser.parse_args()

basin = Basin(
    timerLimit = args.clock,
    host = args.host,
    targetHost = args.target,
    targetCoil = args.bit,
)

basin_db = BasinDataBank( basin = basin )

t = Thread( target = basin.startServer, args = [ basin_db ] )
t.start()