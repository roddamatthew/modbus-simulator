# Simple Modbus Simulator
Simulation of a simple electroplating industrial process to learn about Modbus! By default, the simulation includes 8 basins and one conveyer arm that moves items between the basins after some duration. By default the simulator uses the loopback interface, but could be edited to interact with real PLCs.

# Run the Simulator
First, add IP addresses of the hosts to your loopback interface with `setup-network.sh`. By default this will add 5 hosts to your loopback interface (127.0.1.1-127.0.1.5). These changes can be reverted once you're done with `revert-network.sh`.

Then run the simulator with `start-sim.sh`, and finally visualize the process state with `python3 plot.py`. Note, the plotting script also sends a Modbus request to kick off the process.

## Requirements
See `requirements.txt`.
