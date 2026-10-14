\`timescale 1ns / 1ps
// AXI4-Stream thresholding, four 8-bit unsigned grayscale pixels per beat.
// P = (pixel >= threshold) ? 255 : 0, for each of the four bytes.
// One-deep elastic register allows arbitrary downstream backpressure.
// TLAST and TKEEP are preserved. No frame-width dependency in FPGA.
// AXI control parameter threshold must remain constant during a transfer.
module threshold_axis (
    (* X_INTERFACE_INFO = "xilinx.com:signal:clock:1.0 aclk CLK" *)
    (* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME aclk, ASSOCIATED_BUSIF S_AXIS:M_AXIS, ASSOCIATED_RESET aresetn, FREQ_HZ 100000000" *)
    input wire aclk,
    (* X_INTERFACE_INFO = "xilinx.com:signal:reset:1.0 aresetn RST" *)
    (* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME aresetn, POLARITY ACTIVE_LOW" *)
    input wire aresetn,
    input wire [7:0] threshold,

    (* X_INTERFACE_INFO = "xilinx.com:interface:axis:1.0 S_AXIS TDATA" *)
    (* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME S_AXIS, TDATA_NUM_BYTES 4, HAS_TKEEP 1, HAS_TLAST 1, HAS_TREADY 1" *)
    input wire [31:0] s_axis_tdata,
    (* X_INTERFACE_INFO = "xilinx.com:interface:axis:1.0 S_AXIS TKEEP" *)
    input wire [3:0] s_axis_tkeep,
    (* X_INTERFACE_INFO = "xilinx.com:interface:axis:1.0 S_AXIS TVALID" *)
    input wire s_axis_tvalid,
    (* X_INTERFACE_INFO = "xilinx.com:interface:axis:1.0 S_AXIS TREADY" *)
    output wire s_axis_tready,
    (* X_INTERFACE_INFO = "xilinx.com:interface:axis:1.0 S_AXIS TLAST" *)
    input wire s_axis_tlast,

    (* X_INTERFACE_INFO = "xilinx.com:interface:axis:1.0 M_AXIS TDATA" *)
    (* X_INTERFACE_PARAMETER = "XIL_INTERFACENAME M_AXIS, TDATA_NUM_BYTES 4, HAS_TKEEP 1, HAS_TLAST 1, HAS_TREADY 1" *)
    output wire [31:0] m_axis_tdata,
    (* X_INTERFACE_INFO = "xilinx.com:interface:axis:1.0 M_AXIS TKEEP" *)
    output wire [3:0] m_axis_tkeep,
    (* X_INTERFACE_INFO = "xilinx.com:interface:axis:1.0 M_AXIS TVALID" *)
    output wire m_axis_tvalid,
    (* X_INTERFACE_INFO = "xilinx.com:interface:axis:1.0 M_AXIS TREADY" *)
    input wire m_axis_tready,
    (* X_INTERFACE_INFO = "xilinx.com:interface:axis:1.0 M_AXIS TLAST" *)
    output wire m_axis_tlast
);
    wire [31:0] thresholded;
    genvar lane;
    generate
        for (lane = 0; lane < 4; lane = lane + 1) begin : g_threshold
            assign thresholded[8*lane +: 8] =
                (s_axis_tdata[8*lane +: 8] >= threshold) ? 8'hFF : 8'h00;
        end
    endgenerate

    reg [31:0] output_data = 32'd0;
    reg [3:0] output_keep = 4'd0;
    reg output_last = 1'b0;
    reg output_valid = 1'b0;

    assign s_axis_tready = !output_valid || m_axis_tready;
    assign m_axis_tvalid = output_valid;
    assign m_axis_tdata = output_data;
    assign m_axis_tkeep = output_keep;
    assign m_axis_tlast = output_last;

    always @(posedge aclk) begin
        if (!aresetn) begin
            output_valid <= 1'b0;
            output_data <= 32'd0;
            output_keep <= 4'd0;
            output_last <= 1'b0;
        end else if (s_axis_tready) begin
            // Consume a new input beat, or mark register empty.
            output_valid <= s_axis_tvalid;
            if (s_axis_tvalid) begin
                output_data <= thresholded;
                output_keep <= s_axis_tkeep;
                output_last <= s_axis_tlast;
            end
        end
    end
endmodule
