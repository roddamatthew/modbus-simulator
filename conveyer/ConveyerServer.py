from .Conveyer import Conveyer
from .ConveyerDataBank import ConveyerDataBank
import argparse

def startConveyerServer(host='127.0.1:502'):
    arm = Conveyer( host )
    armDataBank = ConveyerDataBank( arm )
    arm.startServer( armDataBank )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument( '-H', '--host', type = str, default = '127.0.0.1:502', help = 'ip:port' )
    args = parser.parse_args()
    
    startConveyerServer(args.host)