import time
import json
from time import sleep

from src import SPIESP32 as SPI
from src import (
    CAN,
    CAN_CLOCK,
    CAN_SPEED,
    ERROR,
    
)

can = CAN(SPI(cs=27))

def connect_mcp2515():
    # Initialization
    # Configuration
    if can.reset() != ERROR.ERROR_OK:
        #print("Can not reset for MCP2515")
        return '0xAA'
    if can.setBitrate(CAN_SPEED.CAN_500KBPS, CAN_CLOCK.MCP_8MHZ) != ERROR.ERROR_OK:
        #print("Can not set bitrate for MCP2515")
        return '0xBB'
    can.setFilterMask(1,False,0x7ff)
    can.setFilter(0,False,0x329)
    can.setFilter(1,False,0x545)
    can.setFilterMask(2,False,0x7ff)
    can.setFilter(0,False,0x329)
    can.setFilter(1,False,0x545)

    if can.setNormalMode() != ERROR.ERROR_OK:
        #print("Can not set normal mode for MCP2515")
        return '0xDD'
    #print('Connection to MCP2515 successfully')
    return '0xFF'

#print(connect_mcp2515())

def __parse_frame():
    error,_frame = can.readMessage()
    if error == ERROR.ERROR_OK:
        __parsed_data = []
        for __element in str(_frame).split(' '):
            if len(__element)>0:
                __parsed_data.append(__element.strip('[]'))
        return __parsed_data

def create_data_list():
    __data = __parse_frame()
    if __data:
        __data_array = {}
        __elem_aray = {}
        for _i in range(0,len(__data)-2):
            __elem_aray.update({f'B{_i}':f'0x{__data[_i+2]}'})
        __data_array.update({__data[0]:__elem_aray})
        return __data_array
    




        

    
    