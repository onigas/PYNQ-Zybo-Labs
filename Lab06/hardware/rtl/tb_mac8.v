`timescale 1 ns / 1 ps
module tb_mac8;
    reg [7:0] a, b;
    reg [15:0] c;
    wire [31:0] y;
    integer i;
    reg [31:0] expected;
    mac8 dut (.a(a), .b(b), .c(c), .y(y));
    initial begin
        a = 0; b = 0; c = 0; #1;
        if (y !== 0) $fatal(1, "zero test failed");
        a = 255; b = 255; c = 65535; #1;
        if (y !== 130560) $fatal(1, "max test failed: %d", y);
        for (i=0; i<1000; i=i+1) begin
            a = $random; b = $random; c = $random;
            #1;
            expected = a*b+c;
            if (y !== expected)
                $fatal(1, "Mismatch a=%d b=%d c=%d got=%d expected=%d", a,b,c,y,expected);
        end
        $display("PASS: 1002 RTL test vectors");
        $finish;
    end
endmodule
