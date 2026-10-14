\`timescale 1ns / 1ps
module tb_threshold_axis;
    reg aclk = 0;
    always #5 aclk = ~aclk;   // 100 MHz
    reg aresetn = 0;
    reg [7:0] threshold = 8'd128;
    reg [31:0] s_axis_tdata = 0;
    reg [3:0] s_axis_tkeep = 4'hF;
    reg s_axis_tvalid = 0;
    wire s_axis_tready;
    reg s_axis_tlast = 0;
    wire [31:0] m_axis_tdata;
    wire [3:0] m_axis_tkeep;
    wire m_axis_tvalid;
    reg m_axis_tready = 0;
    wire m_axis_tlast;
    integer i;
    integer consumed = 0;
    integer cycle = 0;
    integer watchdog = 0;
    reg [31:0] expected;

    threshold_axis dut (
        .aclk(aclk), .aresetn(aresetn), .threshold(threshold),
        .s_axis_tdata(s_axis_tdata), .s_axis_tkeep(s_axis_tkeep),
        .s_axis_tvalid(s_axis_tvalid), .s_axis_tready(s_axis_tready),
        .s_axis_tlast(s_axis_tlast),
        .m_axis_tdata(m_axis_tdata), .m_axis_tkeep(m_axis_tkeep),
        .m_axis_tvalid(m_axis_tvalid), .m_axis_tready(m_axis_tready),
        .m_axis_tlast(m_axis_tlast)
    );

    function [31:0] src_word;
        input integer index;
        integer k;
        reg [31:0] word;
        begin
            word = 0;
            for (k=0; k<4; k=k+1)
                word[8*k +: 8] = (index*4+k)*7;
            src_word = word;
        end
    endfunction
    function [31:0] mask_word;
        input [31:0] src;
        input [7:0] t;
        integer k;
        reg [31:0] word;
        begin
            word = 0;
            for (k=0; k<4; k=k+1)
                word[8*k +: 8] = (src[8*k +: 8] >= t) ? 8'hFF : 8'h00;
            mask_word = word;
        end
    endfunction

    always @(negedge aclk) begin
        cycle = cycle + 1;
        // Ready drops regularly, exercising output buffering/backpressure.
        m_axis_tready = (cycle % 7 != 0) && (cycle % 7 != 1);
    end
    always @(posedge aclk) begin
        if (aresetn && m_axis_tvalid && m_axis_tready) begin
            expected = mask_word(src_word(consumed), threshold);
            if (m_axis_tdata !== expected || m_axis_tkeep !== 4'hF ||
                    m_axis_tlast !== (consumed == 31)) begin
                $display("FAIL: beat %0d expected %h got %h keep=%h last=%b",
                         consumed, expected, m_axis_tdata, m_axis_tkeep, m_axis_tlast);
                $fatal(1);
            end
            consumed = consumed + 1;
        end
    end
    initial begin
        repeat (5) @(negedge aclk);
        aresetn = 1;
        for (i=0; i<32; i=i+1) begin
            @(negedge aclk);
            s_axis_tvalid = 1;
            s_axis_tdata = src_word(i);
            s_axis_tlast = (i==31);
            @(posedge aclk);
            while (!s_axis_tready) @(posedge aclk);
        end
        @(negedge aclk);
        s_axis_tvalid = 0;
        s_axis_tlast = 0;
        while (consumed < 32 && watchdog < 100) begin
            @(negedge aclk);
            watchdog = watchdog + 1;
        end
        if (consumed != 32) $fatal(1, "Timeout: consumed %0d of 32", consumed);
        $display("PASS: 32 streaming beats, 128 pixels, TLAST and backpressure");
        $finish;
    end
endmodule
