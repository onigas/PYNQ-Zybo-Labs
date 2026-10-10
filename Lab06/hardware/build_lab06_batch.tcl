# Vivado 2022.2, Digilent original Zybo board, xc7z010clg400-1.
# New project: does NOT modify the working lab06.bit / lab06.hwh overlay.
# Vivado Tcl Console: source {C:/path/to/Lab06/hardware/build_lab06_batch.tcl}

set script_dir [file normalize [file dirname [info script]]]
set outdir [file normalize [file join $script_dir build_batch]]
file mkdir $outdir
create_project lab06_batch $outdir -part xc7z010clg400-1 -force
set_property target_language Verilog [current_project]

# Use the exact same legacy Zybo PS7 board preset as in build_lab06.tcl.
set legacy_board ""
foreach bp [get_board_parts -quiet *zybo*] {
    set n [string tolower $bp]
    if {![string match *z7* $n] && ![string match *zybo-z7* $n]} {
        set legacy_board $bp
        break
    }
}
if {$legacy_board eq ""} {
    error "Original Zybo board files missing. Install the legacy Digilent zybo board files, not zybo-z7-10."
}
puts "Using board: $legacy_board"
set_property board_part $legacy_board [current_project]
add_files -norecurse [file join $script_dir rtl batch_mac.v]
update_compile_order -fileset sources_1

create_bd_design design_1
set ps [create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 ps7_0]
apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 \
    -config {make_external "FIXED_IO, DDR" apply_board_preset "1" Master "Disable" Slave "Disable"} $ps
set_property -dict [list CONFIG.PCW_USE_M_AXI_GP0 {1} CONFIG.PCW_EN_CLK0_PORT {1} CONFIG.PCW_FPGA0_PERIPHERAL_FREQMHZ {100.0}] $ps

set rst [create_bd_cell -type ip -vlnv xilinx.com:ip:proc_sys_reset:5.0 reset_0]
set_property -dict [list CONFIG.C_EXT_RESET_HIGH {0}] $rst
set locked [create_bd_cell -type ip -vlnv xilinx.com:ip:xlconstant:1.1 clock_locked_0]
set_property -dict [list CONFIG.CONST_VAL {1} CONFIG.CONST_WIDTH {1}] $locked
connect_bd_net [get_bd_pins clock_locked_0/dout] [get_bd_pins reset_0/dcm_locked]

set ic [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_interconnect:2.1 axi_interconnect_0]
set_property -dict [list CONFIG.NUM_SI {1} CONFIG.NUM_MI {3}] $ic

# control_gpio ch1: N[31:0] output; ch2: START[0] output.
set ctrl [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 control_gpio]
set_property -dict [list CONFIG.C_GPIO_WIDTH {32} CONFIG.C_ALL_OUTPUTS {1} \
    CONFIG.C_IS_DUAL {1} CONFIG.C_GPIO2_WIDTH {1} CONFIG.C_ALL_OUTPUTS_2 {1}] $ctrl

# results_gpio ch1: Y[31:0] input; ch2: CYCLES[31:0] input.
set results [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 results_gpio]
set_property -dict [list CONFIG.C_GPIO_WIDTH {32} CONFIG.C_ALL_INPUTS {1} \
    CONFIG.C_IS_DUAL {1} CONFIG.C_GPIO2_WIDTH {32} CONFIG.C_ALL_INPUTS_2 {1}] $results

# status_gpio ch1: {BUSY, DONE} input (bits 1 and 0 respectively).
set flags [create_bd_cell -type ip -vlnv xilinx.com:ip:axi_gpio:2.0 status_gpio]
set_property -dict [list CONFIG.C_GPIO_WIDTH {2} CONFIG.C_ALL_INPUTS {1}] $flags

set mac [create_bd_cell -type module -reference batch_mac batch_mac_0]

connect_bd_intf_net [get_bd_intf_pins ps7_0/M_AXI_GP0] [get_bd_intf_pins axi_interconnect_0/S00_AXI]
connect_bd_intf_net [get_bd_intf_pins axi_interconnect_0/M00_AXI] [get_bd_intf_pins control_gpio/S_AXI]
connect_bd_intf_net [get_bd_intf_pins axi_interconnect_0/M01_AXI] [get_bd_intf_pins results_gpio/S_AXI]
connect_bd_intf_net [get_bd_intf_pins axi_interconnect_0/M02_AXI] [get_bd_intf_pins status_gpio/S_AXI]

connect_bd_net [get_bd_pins ps7_0/FCLK_CLK0] [get_bd_pins ps7_0/M_AXI_GP0_ACLK] \
    [get_bd_pins reset_0/slowest_sync_clk] [get_bd_pins batch_mac_0/clk] \
    [get_bd_pins axi_interconnect_0/ACLK] [get_bd_pins axi_interconnect_0/S00_ACLK] \
    [get_bd_pins axi_interconnect_0/M00_ACLK] [get_bd_pins axi_interconnect_0/M01_ACLK] [get_bd_pins axi_interconnect_0/M02_ACLK] \
    [get_bd_pins control_gpio/s_axi_aclk] [get_bd_pins results_gpio/s_axi_aclk] [get_bd_pins status_gpio/s_axi_aclk]
connect_bd_net [get_bd_pins ps7_0/FCLK_RESET0_N] [get_bd_pins reset_0/ext_reset_in]
connect_bd_net [get_bd_pins reset_0/interconnect_aresetn] [get_bd_pins axi_interconnect_0/ARESETN]
connect_bd_net [get_bd_pins reset_0/peripheral_aresetn] \
    [get_bd_pins axi_interconnect_0/S00_ARESETN] \
    [get_bd_pins axi_interconnect_0/M00_ARESETN] [get_bd_pins axi_interconnect_0/M01_ARESETN] [get_bd_pins axi_interconnect_0/M02_ARESETN] \
    [get_bd_pins control_gpio/s_axi_aresetn] [get_bd_pins results_gpio/s_axi_aresetn] \
    [get_bd_pins status_gpio/s_axi_aresetn] [get_bd_pins batch_mac_0/resetn]

connect_bd_net [get_bd_pins control_gpio/gpio_io_o] [get_bd_pins batch_mac_0/n_ops]
connect_bd_net [get_bd_pins control_gpio/gpio2_io_o] [get_bd_pins batch_mac_0/start]
connect_bd_net [get_bd_pins batch_mac_0/y] [get_bd_pins results_gpio/gpio_io_i]
connect_bd_net [get_bd_pins batch_mac_0/cycles] [get_bd_pins results_gpio/gpio2_io_i]
connect_bd_net [get_bd_pins batch_mac_0/status] [get_bd_pins status_gpio/gpio_io_i]

assign_bd_address
validate_bd_design
save_bd_design
set bd [get_files -quiet */design_1.bd]
if {[llength $bd] != 1} { error "Cannot resolve design_1.bd" }
generate_target all $bd
make_wrapper -files $bd -top
add_files -norecurse [glob [file join $outdir lab06_batch.gen sources_1 bd design_1 hdl design_1_wrapper.v]]
set_property top design_1_wrapper [current_fileset]
update_compile_order -fileset sources_1

puts "Block design validated. Building batch accelerator bitstream..."
launch_runs impl_1 -to_step write_bitstream -jobs 4
wait_on_run impl_1
if {[get_property STATUS [get_runs impl_1]] ne "write_bitstream Complete!"} {
    error "Batch accelerator implementation incomplete: inspect Vivado run log."
}
set bits [glob -nocomplain [file join $outdir lab06_batch.runs impl_1 design_1_wrapper.bit]]
set hw_hwh [glob -nocomplain [file join $outdir lab06_batch.gen sources_1 bd design_1 hw_handoff design_1.hwh]]
if {[llength $bits] != 1 || [llength $hw_hwh] != 1} {
    error "Batch bitstream or HWH missing: inspect generated paths in Vivado."
}
file mkdir [file join $script_dir output]
file copy -force [lindex $bits 0] [file join $script_dir output lab06_batch.bit]
file copy -force [lindex $hw_hwh 0] [file join $script_dir output lab06_batch.hwh]
puts "SUCCESS: generated output/lab06_batch.bit and output/lab06_batch.hwh"
puts "Check implementation timing before running the PYNQ experiments."
