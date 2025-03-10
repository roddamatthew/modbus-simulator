from pyModbusTCP.client import ModbusClient
from pyModbusTCP.server import ModbusServer
from threading import Timer
import time
from time import sleep

class Basin():
    '''
    Basin to be used in rack plating process
    Basin has a number of sensors that broadcast state
    Basin has a simulated chemical within it
    Basin also has a timer that starts when a rack is placed within it
    After the timer expires, message the Conveyer to remove this rack
    '''

    def __init__( self, timerLimit: int, host: str, targetHost: str, targetCoil: int, pH = 7., temp = 60., fluidLevel = 1 ):
        # Networking params
        self.host = host
        self.targetHost = ModbusClient( # Address to message when timer expires
            host = targetHost.split( ':' )[0],
            port = int( targetHost.split( ':' )[1] ),
            auto_open = True,
        )
        self.targetCoil = targetCoil
        self.server = None
        
        # Timer params
        self.timerLimit = timerLimit # Milliseconds
        self.rinseLimit = 5000 # Milliseconds
        self.startTime = None
        self.rinseTime = None

        # Fake statuses
        self.basinFilled = False # Every PLC is connectd to a basin
        self.rinseFilled = False # And a second water basin for rinsing

        # Fake sensor readings
        self.pH = pH
        self.temp = temp # Celsius
        self.fluidLevel = fluidLevel
    
    def startServer( self, databank ):
        self.server = ModbusServer(
            host = self.host.split( ':' )[0],
            port = int( self.host.split( ':' )[1] ),
            data_bank = databank,
        )
        self.server.start()
    
    def startTimer( self ):
        if self.startTime: return
        
        self.startTime = time.time()
        t = Timer( self.timerLimit / 1000, self.timerExpired ) # Convert back to seconds
        t.start()
    
    def timerExpired( self ):
        self.startTime = None
        while self.basinFilled:
            self.targetHost.write_single_coil( self.targetCoil, True )
            sleep( 0.01 )
    
    def rinseTimer( self ):
        if self.rinseTime: return

        self.rinseTime = time.time()
        t = Timer( self.rinseLimit / 1000, self.rinseExpired )
        t.start()
    
    def rinseExpired( self ):
        self.rinseTime = None
        while self.rinseFilled:
            self.targetHost.write_single_coil( self.targetCoil + 1, True )
            sleep( 0.01 )