from .Basin import Basin
from .BasinDataBank import BasinDataBank
from threading import Thread
import argparse

def startBasinServer(host = '127.0.0.1:502', target = '127.0.0.1:502', timer = 30, coil_addr = 0):
    basin = Basin(
        timerLimit = timer,
        host = host,
        targetHost = target,
        targetCoil = coil_addr,
    )

    basin_db = BasinDataBank( basin = basin )
    t = Thread( target = basin.startServer, args = [ basin_db ] )
    t.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument( '-H', '--host', type = str, default = '127.0.0.1:5021', help = 'ip:port' )
    parser.add_argument( '-t', '--target', type = str, default = '127.0.0.1:5022', help = 'ip:port' )
    parser.add_argument( '-c', '--clock', type = int, default = '3000', help = 'time in milliseconds' )
    parser.add_argument( '-b', '--bit', type = int, default = '0', help = 'coil to set after timer expires' )
    args = parser.parse_args()

    startBasinServer(
        host = args.host,
        target = args.target,
        timer = args.clock,
        coil_addr = args.bit,
    )