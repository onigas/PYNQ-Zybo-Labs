# Lab07: 32-bit packed AXI4-Stream threshold FPGA accelerator with AXI DMA.
# Board: Digilent Zybo LEGACY (Zynq-7010; xc7z010clg400-1), Vivado 2022.2.
# Vivado Tcl Console: source {C:/path/to/Lab07/hardware/build_lab07.tcl}
# New Vivado project; NEVER overwrite working Lab06 overlays.

set script_dir [file normalize [file dirname [info script]]]
set outdir [file normalize [file join $script_dir build]]
create_project lab07_dma_threshold $outdir -part xc7z010clg400-1 -force
set_property target_language Verilog [current_project]
set legacy_board ""
foreach bp [get_board_parts -quiet *zybo*] {
    set n [string tolower $bp]
    if {![string match *z7* $n] && ![string match *zybo-z7* $n]} {
        set legacy_board $bp
        break
    }
}
if {$legacy_board eq ""} {
    error "Install Digilent ORIGINAL zybo board preset (not zybo-z7-10), restart Vivado and rerun."
}
puts "Selected board preset: $legacy_board"
set_property board_part $legacy_board [current_project]
add_files -norecurse [file join $script_dir rtl threshold_axis.v]
update_compile_order -fileset sources_1

create_bd_design design_1
set ps [create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 ps7_0]
apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 \
    -config {make_external "FIXED_IO, DDR" apply_board_preset "1" Master "Disable" Slave "Disable"} $ps
set_property -dict [list \
    CONFIG.PCW_USE_M_AXI_GP0 {1} \
    CONFIG.PCW_USE_S_AXI_HP0 {1} \
    CONFIG.PCW_EN_CLK0_PORT {1} \
    CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {100.0}] $ps

set rst [create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset:5.0 reset_0]
set_property CONFIG.C_EXT_RESET_HIGH {0} $rst
set locked [create_bd_cell -type ip -vlnv xilinx.com:ip:xlconstant:1.1 clock_locked_0]
set_property -dict [list CONFIG.CONST_VAL {1} CONFIG.CONST_WIDTH {1}] $locked
connect_bd_net [get_bd_pins clock_locked_0/dout] [get_bd_pins reset_0/dcm_locked]

set ctrl_ic [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_interconnect:2.1 control_interconnect]
set_property -dict [list CONFIG.NUM_SI {1} CONFIG.NUM_MI {2}] $ctrl_ic
set data_ic [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_interconnect:2.1 ddr_interconnect]
set_property -dict [list CONFIG.NUM_SI {2} CONFIG.NUM_MI {1}] $data_ic

set dma [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_dma:7.1 axi_dma_0]
set_property -dict [list \
    CONFIG.c_include_sg {0} \
    CONFIG.c_include_mm2s {1} \
    CONFIG.c_include_s2mm {1} \
    CONFIG.c_m_axi_mm2s_data_width {32} \
    CONFIG.c_m_axi_s2mm_data_width {32} \
    CONFIG.c_m_axis_mm2s_tdata_width {32} \
    CONFIG.c_s_axis_s2mm_tdata_width {32} \
    CONFIG.c_include_mm2s_dre {0} \
    CONFIG.c_include_s2mm_dre {0} \
    CONFIG.c_sg_length_width {23} \
    CONFIG.c_mm2s_burst_size {16} \
    CONFIG.c_s2mm_burst_size {16}] $dma

set gpio [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 threshold_gpio]
set_property -dict [list CONFIG.C_GPIO_WIDTH {8} CONFIG.C_ALL_OUTPUTS {1}] $gpio
set core [create_bd_cell -type module -reference threshold_axis threshold_axis_0]

foreach pin {threshold_axis_0/S_AXIS threshold_axis_0/M_AXIS} {
    if {[llength [get_bd_intf_pins -quiet $pin]] != 1} {
        error "Cannot find AXIS module interface $pin: inspect RTL X_INTERFACE_INFO annotations."
    }
}
connect_bd_intf_net [get_bd_intf_pins ps7_0/M_AXI_GP0] [get_bd_intf_pins control_interconnect/S00_AXI]
connect_bd_intf_net [get_bd_intf_pins control_interconnect/M00_AXI] [get_bd_intf_pins axi_dma_0/S_AXI_LITE]
connect_bd_intf_net [get_bd_intf_pins control_interconnect/M01_AXI] [get_bd_intf_pins threshold_gpio/S_AXI]

connect_bd_intf_net [get_bd_intf_pins axi_dma_0/M_AXI_MM2S] [get_bd_intf_pins ddr_interconnect/S00_AXI]
connect_bd_intf_net [get_bd_intf_pins axi_dma_0/M_AXI_S2MM] [get_bd_intf_pins ddr_interconnect/S01_AXI]
connect_bd_intf_net [get_bd_intf_pins ddr_interconnect/M00_AXI] [get_bd_intf_pins ps7_0/S_AXI_HP0]

connect_bd_intf_net [get_bd_intf_pins axi_dma_0/M_AXIS_MM2S] [get_bd_intf_pins threshold_axis_0/S_AXIS]
connect_bd_intf_net [get_bd_intf_pins threshold_axis_0/M_AXIS] [get_bd_intf_pins axi_dma_0/S_AXIS_S2MM]
connect_bd_net [get_bd_pins threshold_gpio/gpio_io_o] [get_bd_pins threshold_axis_0/threshold]

connect_bd_net [get_bd_pins ps7_0/FCLK_CLK0] \
    [get_bd_pins ps7_0/M_AXI_GP0_ACLK] [get_bd_pins ps7_0/S_AXI_HP0_ACLK] \
    [get_bd_pins reset_0/slowest_sync_clk] \
    [get_bd_pins control_interconnect/ACLK] [get_bd_pins control_interconnect/S00_ACLK] \
    [get_bd_pins control_interconnect/M00_ACLK] [get_bd_pins control_interconnect/M01_ACLK] \
    [get_bd_pins ddr_interconnect/ACLK] [get_bd_pins ddr_interconnect/S00_ACLK] \
    [get_bd_pins ddr_interconnect/S01_ACLK] [get_bd_pins ddr_interconnect/M00_ACLK] \
    [get_bd_pins axi_dma_0/s_axi_lite_aclk] \
    [get_bd_pins axi_dma_0/m_axi_mm2s_aclk] \
    [get_bd_pins axi_dma_0/m_axi_s2mm_aclk] \
    [get_bd_pins threshold_gpio/s_axi_aclk] [get_bd_pins threshold_axis_0/aclk]
connect_bd_net [get_bd_pins ps7_0/FCLK_RESET0_N] [get_bd_pins reset_0/ext_reset_in]
connect_bd_net [get_bd_pins reset_0/interconnect_aresetn] \
    [get_bd_pins control_interconnect/ARESETN] [get_bd_pins ddr_interconnect/ARESETN]
connect_bd_net [get_bd_pins reset_0/peripheral_aresetn] \
    [get_bd_pins control_interconnect/S00_ARESETN] \
    [get_bd_pins control_interconnect/M00_ARESETN] [get_bd_pins control_interconnect/M01_ARESETN] \
    [get_bd_pins ddr_interconnect/S00_ARESETN] [get_bd_pins ddr_interconnect/S01_ARESETN] \
    [get_bd_pins ddr_interconnect/M00_ARESETN] \
    [get_bd_pins axi_dma_0/axi_resetn] \
    [get_bd_pins threshold_gpio/s_axi_aresetn] [get_bd_pins threshold_axis_0/aresetn]

assign_bd_address
validate_bd_design
save_bd_design
set bd [get_files -quiet */design_1.bd]
if {[llength $bd] != 1} {error "Block design file missing."}
generate_target all $bd
make_wrapper -files $bd -top
set wrapper [glob -nocomplain [file join $outdir lab07_dma_threshold.gen sources_1 bd design_1 hdl design_1_wrapper.v]]
if {[llength $wrapper] != 1} {error "HDL wrapper missing; inspect make_wrapper output."}
add_files -norecurse [lindex $wrapper 0]
set_property top design_1_wrapper [current_fileset]
update_compile_order -fileset sources_1
puts "Block design validated; launching Vivado implementation..."
launch_runs impl_1 -to_step write_bitstream -jobs 4
wait_on_run impl_1
if {[get_property STATUS [get_runs impl_1]] ne "write_bitstream Complete!"} {
    error "Implementation failed; check Vivado messages and report_timing_summary."
}
set bits [glob -nocomplain [file join $outdir lab07_dma_threshold.runs impl_1 design_1_wrapper.bit]]
set hwhs [glob -nocomplain [file join $outdir lab07_dma_threshold.gen sources_1 bd design_1 hw_handoff design_1.hwh]]
if {[llength $bits] != 1 || [llength $hwhs] != 1} {
    error "Missing bitstream or HWH; inspect the generated Vivado folders."
}
file mkdir [file join $script_dir output]
file copy -force [lindex $bits 0] [file join $script_dir output lab07.bit]
file copy -force [lindex $hwhs 0] [file join $script_dir output lab07.hwh]
puts "SUCCESS: hardware/output/lab07.bit and hardware/output/lab07.hwh"
puts "IMPORTANT: Confirm timing closure (WNS >= 0) before testing on Zybo."
