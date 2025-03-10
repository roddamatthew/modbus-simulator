from pyModbusTCP.server import DataBank
import numpy as np
import time

class BasinDataBank( DataBank ):
    ''' DataBank to advertise the basin's state '''

    def __init__( self, basin ):
        self.basin = basin
        super().__init__( virtual_mode = True )
    
    def get_holding_registers( self, address, number = 1, srv_info = None ):
        '''
        Called whenever a Modbus read registers packet is received.
        
        Simulate 5 registers:
        0: Timer for plating
        1: Plating fluid pH
        2: Plating fluid level
        3: Plating fluid temperature
        4: Timer for rinsing
        '''
        registers = {}

        if self.basin.startTime:
            registers[0] = time.time() - self.basin.startTime
            registers[0] = int( registers[0] * 1000 ) # Convert to milliseconds
        else:
            registers[0] = self.basin.timerLimit
        
        # Simulate sensor readings with a small amount of noise
        registers[1] = int( self.basin.pH * 100 + np.random.normal( 0, 1 ) )
        registers[2] = int( self.basin.fluidLevel * 100 + np.random.normal( 0, 1 ) )
        if self.basin.basinFilled: registers[2] = int( registers[2] * 1.1 ) # Increase fluid level a little when the basin is occupied
        registers[3] = int( self.basin.temp * 100 + np.random.normal( 0, 1 ) )

        if self.basin.rinseTime:
            registers[4] = time.time() - self.basin.rinseTime
            registers[4] = int( registers[4] * 1000 ) # Convert to milliseconds
        else:
            registers[4] = self.basin.rinseLimit
        
        print( registers )
        
        try:
            return [registers[a] for a in range( address, address + number )]
        except KeyError:
            return
    
    def set_coils(self, address, bit_list, srv_info=None):
        '''
        Called whenever a Modbus set coils is recieved
        Simulate two coils, each showing whether a basin is filled
        When a basin is filled, start a timer to communicate when it should empty
        Zeroth coil is whether the basin is filled
        First coil is whether rinse basin is filled
        '''
        
        for i, bit in enumerate(bit_list):
            coil_address = address + i
            
            if coil_address > 1: break # Only simulating the first two registers
            if coil_address == 0: self.basin.basinFilled = bit
            if coil_address == 1: self.basin.rinseFilled = bit

        if self.basin.basinFilled: self.basin.startTimer()
        if self.basin.rinseFilled: self.basin.rinseTimer()
        return True
    
    def get_coils( self, address, number = 1, srv_info=None):
        coils = {a: False for a in range(address, address + number)}

        if 0 in coils and self.basin.basinFilled: coils[0] = True
        if 1 in coils and self.basin.rinseFilled: coils[1] = True
        return [coils[a] for a in range( address, address + number )]