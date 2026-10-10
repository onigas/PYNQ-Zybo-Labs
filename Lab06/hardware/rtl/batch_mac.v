// Lab06 batch MAC engine for original Digilent Zybo (Zynq-7010).
// Inputs are controlled through AXI GPIO registers connected in Vivado.
// All signals use the 100 MHz PL FCLK0 domain; resetn is active-low.
//
// At each START rising edge (when idle):
//   N = n_ops, A = 0, B = 0, C = 0, SUM = 0, CYCLES = 0.
// For each of N subsequent clock cycles:
//   SUM = (SUM + A*B + C) modulo 2^32
//   A = (A + 17) modulo 256
//   B = (B + 53) modulo 256
//   C = (C + 997) modulo 65536
//   CYCLES = CYCLES + 1
// When finished, DONE stays high until the next START edge.
// STATUS = {BUSY, DONE}; bit 0 = DONE, bit 1 = BUSY.
// Unlike the one-operation MAC in lab06.bit, this RTL executes N
// operations using a single PS command, without N AXI round trips.

module batch_mac (
    input  wire        clk,
    input  wire        resetn,
    input  wire        start,
    input  wire [31:0] n_ops,
    output reg  [31:0] y,
    output reg  [31:0] cycles,
    output wire [1:0]  status
);
    reg        busy;
    reg        done;
    reg        start_prev;
    reg [31:0] remaining;
    reg [7:0]  a;
    reg [7:0]  b;
    reg [15:0] c;

    // The width of the result register determines intentional wraparound.
    wire [15:0] product = a * b;
    wire [31:0] sum_next = y + {16'd0, product} + {16'd0, c};

    assign status = {busy, done};

    always @(posedge clk) begin
        if (!resetn) begin
            y          <= 32'd0;
            cycles     <= 32'd0;
            remaining  <= 32'd0;
            a          <= 8'd0;
            b          <= 8'd0;
            c          <= 16'd0;
            busy       <= 1'b0;
            done       <= 1'b0;
            start_prev <= 1'b0;
        end else begin
            start_prev <= start;
            // Process a start command only on its rising edge, when idle.
            if (start && !start_prev && !busy) begin
                y         <= 32'd0;
                cycles    <= 32'd0;
                remaining <= n_ops;
                a         <= 8'd0;
                b         <= 8'd0;
                c         <= 16'd0;
                busy      <= (n_ops != 32'd0);
                done      <= (n_ops == 32'd0);
            end else if (busy) begin
                y         <= sum_next;
                cycles    <= cycles + 32'd1;
                remaining <= remaining - 32'd1;
                a         <= a + 8'd17;
                b         <= b + 8'd53;
                c         <= c + 16'd997;
                if (remaining == 32'd1) begin
                    busy <= 1'b0;
                    done <= 1'b1;
                end
            end
        end
    end
endmodule
