module waveform(

    input wire a,
    input wire b,
    output wire y
);
    
    // Instantiate the or_gate module
    or_gate or_gate (
        .a(a),
        .b(b),
        .y(y)
    );

initial begin 
    $dumpfile("waveform.vcd");
    $dumpvars;
end
endmodule