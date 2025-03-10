from Conveyer import Conveyer
from ConveyerDataBank import ConveyerDataBank
import argparse

parser = argparse.ArgumentParser()
parser.add_argument( '-H', '--host', type = str, default = '127.0.0.1:502', help = 'ip:port' )

args = parser.parse_args()

arm = Conveyer( args.host )
armDataBank = ConveyerDataBank( arm )
arm.startServer( armDataBank )