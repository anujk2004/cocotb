module waves(
    input wire a,
    input wire b,
    output wire y
);

    // Instantiate the xor_rtl module
    xor_rtl xor_rtl (
        .a(a),
        .b(b),
        .y(y)
    );

    initial begin 
        $dumpfile("waves.vcd");
        $dumpvars;
    end
endmodule