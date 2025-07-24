import cocotb 
from cocotb.triggers import Timer , RisingEdge , ReadOnly, NextTimeStep, FallingEdge
from cocotb_bus.drivers import BusDriver
from cocotb_coverage.coverage import CoverCross, CoverPoint, coverage_db
from cocotb_bus.monitors  import BusMonitor
import os
import random
def sb_fn(actual_value):
    #global expected_value
    assert actual_value == expected_value.pop(0) , "scoreboard matching failed"


@CoverPoint("top.a" , 
           xf = lambda x,y:x ,
           bins=[0,1])

@CoverPoint("top.b" , 
           xf = lambda x,y:y ,
           bins=[0,1])

@CoverCross("top.cross.ab",
            items=["top.a", "top.b"])
def ab_cover(a,b):
    pass    

@CoverPoint("top.prot.a.current",
            xf = lambda x: x['current'],
            bins =['idle' , 'RDY' ,'TXN'])

@CoverPoint("top.prot.a.previous",
            xf = lambda x: x['previous'],
            bins =['idle' , 'RDY' ,'TXN'])
@CoverCross("top.cross.a_prot.cross",
            items=["top.prot.a.previous", "top.prot.a.current"],
            ign_bins=[('RDY','idle')])
def a_prot_cover(txn):
    pass
@cocotb.test()
async def andtest(dut):
    global expected_value
   
    expected_value=[]
    dut.RST_N.value = 1 
    await Timer(1,units='ns')
    dut.RST_N.value = 0
    await Timer(1, units='ns')
    dut.RST_N.value = 1

    adrv = InputDriver(dut, 'a' , dut.CLK)
    IOmonitor(dut , 'a' , dut.CLK , callback=a_prot_cover)
    bdrv = InputDriver(dut, 'b' , dut.CLK)
    OutputDriver(dut, 'y' , dut.CLK , sb_fn) 
    for i in range(20):
        a = random.randint(0 , 1)
        b = random.randint(0,1)
        expected_value.append(a&b)
        adrv.append(a)
        bdrv.append(b)
        ab_cover(a,b)
    while len(expected_value) > 0:
        await(Timer(2, units= 'ns'))

    coverage_db.report_coverage(cocotb.log.info , bins=True)
    coverage_file = os.path.join(
        os.getenv('RESULT_PATH' ,"./"),'coverage.xml')
    coverage_db.export_to_xml(filename=coverage_file)


class InputDriver(BusDriver):
    _signals =['rdy' , 'en' , 'data']

    def __init__(self,dut, name , clk):
        BusDriver.__init__(self, dut,name,clk)
        self.bus.en.value =0
        self.clk = clk
       

    async def _driver_send(self, value, sync = True):
        for i in range (random.randint(0,20)):
            await RisingEdge(self.clk)

        if self.bus.rdy.value != 1:
            await RisingEdge(self.bus.rdy)
        self.bus.en.value = 1
        self.bus.data.value = value
        await ReadOnly()
        await RisingEdge(self.clk)
        self.bus.en.value = 0
        await NextTimeStep()



class IOmonitor(BusMonitor):
    _signals=['rdy' ,'en' , 'data']

    async def _monitor_recv(self):
        fallingedge = FallingEdge(self.clock)
        rdonly = ReadOnly()
        phases = {
            0: 'idle',
            1: 'RDY',
            3: 'TXN'
        }
        prev = 'idle'
        while True:
            await fallingedge
            await rdonly
            txn = (self.bus.en.value << 1) | self.bus.rdy.value
            self._recv({'previous': prev , 'current': phases[txn]})
            prev = phases[txn]

class OutputDriver(BusDriver):
    _signals =['rdy' , 'en' , 'data']

    def __init__(self,dut, name , clk, sb_callback):
        BusDriver.__init__(self, dut,name,clk)
        self.bus.en.value =0
        self.clk = clk
        self.callback= sb_callback
        self.append(0)
    async def _driver_send(self, value, sync = True):
        for i in range (random.randint(0,20)):
            await RisingEdge(self.clk)
        while True:
            if self.bus.rdy.value != 1:
                await RisingEdge(self.bus.rdy)
            self.bus.en.value = 1
        # self.bus.data = value
            await ReadOnly()
            self.callback(self.bus.data.value)
            await RisingEdge(self.clk)
            self.bus.en.value = 0
            await NextTimeStep()
            #self.bus.en.value = 0