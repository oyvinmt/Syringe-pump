## Partially adapted from pumpy written by Thomas W. Phillips
## https://github.com/tomwphillips/pumpy
"""
Created on Mon Jun  28 08:14:00 2021
@author: Øyvind Taraldsen
"""
from __future__ import print_function 
import serial
class Chain(serial.Serial):
    """Create Chain object.
    Harvard syringe pumps are daisy chained together in a 'pump chain'
    off a single serial port. A pump address is set on each pump. You
    must first create a chain to which you then add Pump objects.

    Chain is a subclass of serial.Serial. Chain creates a serial.Serial
    instance with the required parameters, flushes input and output
    buffers (found during testing that this fixes a lot of problems) and
    logs creation of the Chain.
    """
    def __init__(self, port):
        serial.Serial.__init__(self,port=port, stopbits=serial.STOPBITS_TWO, parity=serial.PARITY_NONE, timeout=2)
        self.flushOutput()
        self.flushInput()

class Pump:
    """Create Pump object.

    Argument:
        Chain: pump chain

    Optional arguments:
        address: pump address. Default is 0.
        name: used in logging. Default is Pump 11.
    """
    def __init__(self, chain, address=0, name='Pump 11'):
        self.name = name
        self.serialcon = chain
        self.address = '{0:02.0f}'.format(address)
        try:
            self.write('ADDRESS')
            resp = self.read()
            print(resp)
            if int(resp[0:2]) != int(self.address):
                raise PumpError('No response from pump at address %s' %
                                self.address)
        except PumpError:
            self.serialcon.close()
            raise

    def __repr__(self):
        string = ''
        for attr in self.__dict__:
            string += '%s: %s\n' % (attr,self.__dict__[attr]) 
        return string

    def write(self,command):
        self.serialcon.write(str.encode(self.address) + str.encode(command) + b'\r')

    def read(self):
        response = b""
        while True:
            temp = self.serialcon.readline()
            if temp == b'00>':
                break
            response = response + temp
        return response.decode('utf-8')

    def logflowrate(self):
        self.write(self.address+'irate')
        resp = self.read()
        strings = resp.splitlines() 
        flowrate = strings[-1]
        print(strings)
        return flowrate

    def setiflowrate(self, flowrate,unit):
        print(flowrate)
        self.write(self.address+'irate' + " "+ flowrate +" " +unit)

class PumpError(Exception):
    pass