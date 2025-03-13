import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import decode_ieee, word_list_to_long
from basin.BasinServer import startBasinServer
from conveyer.ConveyerServer import startConveyerServer
from multiprocessing import Process
from collections import deque

def animate(i):
    for i, c in enumerate(clients):
        registers = c.read_holding_registers(0, 5)
        coils = c.read_coils(0,8)

        if i == 0: 
            l = c.read_holding_registers(0, 4)
            l = word_list_to_long( l )
            registers = [ decode_ieee(float) for float in l ]
        
        history[c.host]['registers'].append( registers )
        history[c.host]['coils'].append( coils )

        # Plot formatting
        axes[0,i].clear()
        axes[1,i].clear()

        axes[0,i].set_title(f'{c.host}')
        axes[0,i].plot(list(history[c.host]['registers'])[-200:])
        axes[1,i].plot(list(history[c.host]['coils'])[-200:])

        axes[0,i].set_ylabel('Register Value')
        axes[1,i].set_ylabel('Coil Value')
        axes[1,i].set_xlabel('Time')
    fig.tight_layout()
    return

if __name__ == '__main__':
    # # First, spawn a bunch of processes for the different devices
    servers = [
        Process(
            target = startConveyerServer,
            kwargs = {'host': '127.0.1.1:502'},
        ),
        Process(
            target = startBasinServer,
            kwargs = {'host': '127.0.1.2:502', 'target': '127.0.1.1:502', 'timer': 5000, 'coil_addr': 1},
        ),
        Process(
            target = startBasinServer,
            kwargs = {'host': '127.0.1.3:502', 'target': '127.0.1.1:502', 'timer': 10000, 'coil_addr': 3},
        ),
        Process(
            target = startBasinServer,
            kwargs = {'host': '127.0.1.4:502', 'target': '127.0.1.1:502', 'timer': 10000, 'coil_addr': 5},
        ),
        Process(
            target = startBasinServer,
            kwargs = {'host': '127.0.1.5:502', 'target': '127.0.1.1:502', 'timer': 5000, 'coil_addr': 7},
        ),
    ]

    [p.start() for p in servers]

    hosts = [
        '127.0.1.1', # Conveyer
        '127.0.1.2', # Basin
        '127.0.1.3', # Basin
        '127.0.1.4', # Basin
        '127.0.1.5', # Basin
    ]

    clients = []
    for host in hosts:
        clients.append(ModbusClient(
            host = host,
            port = 502,
            auto_open = True,
            auto_close = False,
        ))

    fig, axes = plt.subplots(
        ncols = len(clients),
        nrows = 2,
        figsize = (12, 6)
    )

    history = {c.host: {'registers': deque(maxlen = 200), 'coils': deque(maxlen = 200)} for c in clients }

    clients[0].write_single_coil( 0, True )
    ani = animation.FuncAnimation(fig, animate, interval=100)
    plt.show()
