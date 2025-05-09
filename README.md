# Simple Modbus Simulator
Simulation of a simple electroplating industrial process to learn about Modbus! By default, the simulation includes 8 basins and one conveyer arm that moves items between the basins after some duration. By default the simulator uses the loopback interface, but could be edited to interact with real PLCs.

# Run the Simulator
First, add IP addresses of the hosts to your loopback interface with 

    `setup-network.sh`

By default this will add 5 hosts to your loopback interface (127.0.1.1-127.0.1.5). These changes can be reverted once you're done with 

    `revert-network.sh`



Then run the simulator and visualizer with

    `python3 main.py`

Optionally, include `-host {ip}` to choose a specific IP for the main server. This allows integrating with other Modbus testing tools.

Note that if port 502 is used, the script will require sudo, so you can run it with

    `sudo {path-to-venv}/bin/python3 main.py`

## Requirements
See `requirements.txt`.

If running with WSL, remember to install `python-tk` to allow matplotlib interactive plotting.