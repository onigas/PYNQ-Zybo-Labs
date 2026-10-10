`timescale 1 ns / 1 ps
// Combinational unsigned multiply-accumulate: Y = A*B + C.
// A,B: 8-bit unsigned; C: 16-bit unsigned; Y: 32-bit unsigned.
module mac8 (
    input  wire [7:0]  a,
    input  wire [7:0]  b,
    input  wire [15:0] c,
    output wire [31:0] y
);
    assign y = ({24'b0, a} * {24'b0, b}) + {16'b0, c};
endmodule
