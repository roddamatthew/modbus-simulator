from pyModbusTCP.server import DataBank
from pyModbusTCP.utils import encode_ieee, long_list_to_word

class ConveyerDataBank( DataBank ):
    def __init__( self, conveyer ):
        self.conveyer = conveyer
        super().__init__( virtual_mode = True )
    
    def get_holding_registers( self, address, number = 1, srv_info = None ):
        registers = {}

        floats = [ self.conveyer.x_pos, self.conveyer.y_pos ]
        b32_l = [encode_ieee(f) for f in floats]
        b16_l = long_list_to_word(b32_l)
        registers = { i: b16_l[i] for i in range( len( b16_l ) ) }

        try:
            return [registers[a] for a in range( address, address + number )]
        except KeyError:
            return
    
    def set_coils( self, address, bit_list, srv_info = None ):
        try:
            for i, bit in enumerate( bit_list ):
                self.conveyer.coils[address + i] = bit
            return True
        except:
            return None
    
    def get_coils(self, address, number, srv_info = None):
        coils = {a: False for a in range(address, address + number)}
        
        for i in range(len(self.conveyer.coils)):
            if i in coils: coils[i] = self.conveyer.coils[i]
        
        return [coils[a] for a in range( address, address + number )]