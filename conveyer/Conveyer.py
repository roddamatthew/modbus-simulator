from pyModbusTCP.server import ModbusServer
from pyModbusTCP.client import ModbusClient
import numpy as np
from threading import Thread
from time import sleep

class Conveyer():
    ''' 
    Conveyer arm for rack plating process
    Arm simulates moving racks between basins
    Advertises its state with a ModbusTCPServer
    '''

    def __init__( self, host: str ):
        self.host = host
        self.n_basins = 4
        self.coils = [ False ] * ( self.n_basins * 2 + 2 )
        self.x_pos = 2.2
        self.y_pos = 2.2
        self.speed = 0.4 # m/s
        self.sim_rate = 1000 # step size
        self.sim_speed = 1 / 1000 # Wait time (s)

        self.basin_locations = np.linspace( 0, 12, ( self.n_basins * 2 + 2 ) ) + np.random.normal( 0, 0.01, size = ( self.n_basins * 2 + 2 ) )
        self.basin_locations[0] = 0.26


    def startServer( self, databank ):
        # Start a thread to handle movement of the arm
        self.movementThread = Thread( target = self.movementControlLoop )
        self.movementThread.daemon = True
        self.movementThread.start()

        self.server = ModbusServer(
            host = self.host.split( ':' )[0],
            port = int( self.host.split( ':' )[1] ),
            data_bank = databank,
        )
        self.server.start()
    
    def movementControlLoop( self ):
        while( True ):
            # Check for a set coil, prioritizing nearby basins
            distances = self.basin_locations - self.x_pos
            coils = [ i for _, i in sorted( zip( distances[:-1], range( len( distances ) )[:-1] ) ) ]
            for ind in coils:
                if self.coils[ind] == True and self.coils[ind + 1] == False:
                    self.move( ind )
                    self.pickup( ind )
                    self.move( ind + 1 )
                    self.dropoff( ind + 1 )
                    break
            sleep( self.sim_speed )
        
    def move( self, target_basin ):
        target_position = self.basin_locations[target_basin]
        self.moveCoordinates( target_position, self.y_pos )
    
    def moveCoordinates( self, x, y ):
        xdir = x - self.x_pos
        if xdir != 0: xdir /= abs( xdir )

        ydir = y - self.y_pos
        if ydir != 0: ydir /= abs( ydir )

        while abs( self.x_pos - x ) > 0.01 or abs( self.y_pos - y ) > 0.01:
            if abs( self.y_pos - y ) > 0.01:
                self.y_pos += self.speed * ydir / self.sim_rate
            if abs( self.x_pos - x ) > 0.01:
                self.x_pos += self.speed * xdir / self.sim_rate
            sleep( self.sim_speed )
        
    def dropoff( self, ind ):
        self.moveCoordinates( self.basin_locations[ind], 0.7 )
        
        # Message the basin that its now full
        self.messageBasin( ind, True )

        self.moveCoordinates( self.basin_locations[ind], 0.6 )
        self.moveCoordinates( self.basin_locations[ind] - 0.1, 0.6 )
        self.moveCoordinates( self.x_pos, 2.2 )

    def pickup( self, ind ):
        # Move slightly to the side and lower
        self.moveCoordinates( self.basin_locations[ind] - 0.1, 0.6 )
        self.moveCoordinates( self.basin_locations[ind], self.y_pos )
        self.moveCoordinates( self.x_pos, 0.7 )
        
        # Message the basin that its now empty
        self.messageBasin( ind, False )
        self.coils[ind] = False
        
        self.moveCoordinates( self.x_pos, 2.2 )
    
    def messageBasin( self, ind, val ):
        if ind >= len( self.coils ) - 2: return
        # Message a basin that its now full/empty
        hosts = [
            '127.0.1.2',
            '127.0.1.3',
            '127.0.1.4',
            '127.0.1.5',
        ]

        c = ModbusClient( 
            host = hosts[( ind - 1 )// 2],
            port = 502,
            auto_open = True,
            auto_close = False,
        )
        c.write_single_coil( ( ind + 1 ) % 2, val )

        