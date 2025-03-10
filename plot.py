import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import decode_ieee, word_list_to_long
from time import sleep

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
        port = 5020,
        auto_open = True,
        auto_close = False,
    ))

fig, axes = plt.subplots(ncols = len(clients), nrows = 2, figsize = (12, 6))

history = {c.host: {'registers': [], 'coils': []} for c in clients }

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
        axes[0,i].plot(history[c.host]['registers'][-200:])
        axes[1,i].plot(history[c.host]['coils'][-200:])

        axes[0,i].set_ylabel('Register Value')
        axes[1,i].set_ylabel('Coil Value')
        axes[1,i].set_xlabel('Time')
    fig.tight_layout()
    return

clients[0].write_single_coil( 0, True )
ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
