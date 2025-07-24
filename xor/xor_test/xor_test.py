import cocotb
from cocotb.triggers import Timer, RisingEdge

@cocotb.test()
async def andtest(dut):
    a= (0, 0, 1, 1)
    b= (0, 1, 0, 1)
    y= (0, 1, 1, 0)

    for i in range(4):
        dut.a.value = a[i]
        dut.b.value = b[i]
        await Timer(1, units='ns')
        assert dut.y.value == y[i], f"Test failed at iteration {i}: expected {y[i]}, got {dut.y.value}"
    print("Test passed successfully!")
