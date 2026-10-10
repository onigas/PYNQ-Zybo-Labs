`timescale 1ns/1ps
module tb_batch_mac;
    reg clk = 0;
    always #5 clk = ~clk; // 100 MHz
    reg resetn = 0;
    reg start = 0;
    reg [31:0] n_ops = 0;
    wire [31:0] y;
    wire [31:0] cycles;
    wire [1:0] status;
    integer errors = 0;
    integer i;
    reg [7:0] a;
    reg [7:0] b;
    reg [15:0] c;
    reg [31:0] expected;

    batch_mac dut(.clk(clk), .resetn(resetn), .start(start),
                  .n_ops(n_ops), .y(y), .cycles(cycles), .status(status));

    task run_case;
        input integer n;
        integer watchdog;
        begin
            expected = 0;
            a = 0; b = 0; c = 0;
            for (i = 0; i < n; i = i + 1) begin
                expected = expected + (a * b) + c;
                a = a + 8'd17;
                b = b + 8'd53;
                c = c + 16'd997;
            end
            @(negedge clk);
            n_ops = n;
            start = 0;
            @(negedge clk);
            start = 1;
            @(negedge clk);
            start = 0;
            watchdog = 0;
            while ((status[0] !== 1'b1) && watchdog < n + 20) begin
                @(negedge clk);
                watchdog = watchdog + 1;
            end
            if (status[0] !== 1'b1 || status[1] !== 1'b0 ||
                cycles !== n || y !== expected) begin
                $display("FAIL: N=%0d got y=%0d, cycles=%0d, status=%b; expected y=%0d",
                         n, y, cycles, status, expected);
                errors = errors + 1;
            end else begin
                $display("PASS: N=%0d cycles=%0d sum=%0d", n, cycles, y);
            end
        end
    endtask

    initial begin
        repeat (4) @(negedge clk);
        resetn = 1;
        run_case(0);
        run_case(1);
        run_case(2);
        run_case(7);
        run_case(100);
        run_case(4096);
        run_case(100000);
        if (errors != 0) begin
            $display("FAIL: %0d mismatches", errors);
            $fatal(1);
        end
        $display("PASS: all batch MAC RTL tests");
        $finish;
    end
endmodule
