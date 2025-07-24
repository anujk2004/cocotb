module dut(input a,b,output y);

assign y= a ^ b;


initial begin 
    $dumpfile("dut.vcd");
    $dumpvars;
end
endmodule