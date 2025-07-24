SIM ?= icarus
TOPLEVEL_LANG ?= verilog
#VERILOG_SOURCES  +=$(PWD) ../rtl/and_gate.v
#VERILOG_SOURCES  +=$(PWD) ../wrapper/waveform.v
VERILOG_SOURCES  +=$(PWD) ../wrapper/ifc_test.v
VERILOG_SOURCES  +=$(PWD) ../rtl/ifc_and.v
VERILOG_SOURCES  +=$(PWD) ../rtl/FIFO1.v
VERILOG_SOURCES  +=$(PWD) ../rtl/FIFO2.v
VERILOG_SOURCES  +=$(PWD) ../rtl/ff.v
# all : or ifc


# or: 
# 	rm -rf  sim_build
# 	$(MAKE) sim MODULE=ortest TOPLEVEL=waveform

ifc:
	rm -rf  sim_build
	$(MAKE) sim MODULE=andtest TOPLEVEL=ifc_test

include $(shell cocotb-config --makefiles)/Makefile.sim