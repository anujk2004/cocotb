SIM ?= icarus
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES  +=$(PWD) ../rtl/or_gate.v
VERILOG_SOURCES  +=$(PWD) ../wrapper/waveform.v
MODULE = ortest
TOPLEVEL = waveform
include $(shell cocotb-config --makefiles)/Makefile.sim